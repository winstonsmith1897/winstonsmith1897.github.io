#!/usr/bin/env python3
"""Refresh the publication list in index.html from Google Scholar.

Unlike the previous version, this script does **not** regenerate index.html.
It only rewrites the regions delimited by these markers:

    <!-- PAPERS:START -->  ... <!-- PAPERS:END -->
    <!-- STATS:START -->   ... <!-- STATS:END -->
    <!-- UPDATED:START --> ... <!-- UPDATED:END -->

Everything else on the page — layout, projects, articles — is left untouched,
so hand-written changes survive an update.

Presentation details (venue label, canonical URL, filter tags) come from
papers_meta.json rather than from Scholar, whose venue strings are unusable.

Usage:
    python update.py              # fetch and rewrite index.html
    python update.py --dry-run    # fetch and print what would change
    python update.py --from FILE  # use a cached JSON payload instead of Scholar

Exits non-zero without touching index.html if Scholar is unreachable or the
response looks truncated, so a failed run can never publish an empty page.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.request
from datetime import date, timezone, datetime

USER_ID = "hhNQwfkAAAAJ"
INDEX = "index.html"
META = "papers_meta.json"

# A run that returns fewer than this many publications is treated as a
# scraping failure (captcha, rate limit) rather than as a real profile.
MIN_EXPECTED_PUBS = 8

ME_SURNAME = "simoni"
ME_INITIAL = "M"

UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)


# --------------------------------------------------------------------------
# Scholar scraping
# --------------------------------------------------------------------------
def _get(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", "replace")


def _text(fragment: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", fragment)).strip()


def fetch_profile(user_id: str = USER_ID, details: bool = True) -> dict:
    """Scrape the profile page, then each publication page for its author list."""
    page = _get(
        f"https://scholar.google.com/citations?user={user_id}&hl=en&cstart=0&pagesize=100"
    )
    if "captcha" in page.lower() or "unusual traffic" in page.lower():
        raise RuntimeError("Google Scholar served a captcha instead of the profile")

    numbers = re.findall(r'gsc_rsb_std">([\d,]+)</td>', page)
    stats = {}
    if len(numbers) >= 6:
        # The table is (all, recent) x (citations, h-index, i10-index).
        stats = {
            "citations": numbers[0],
            "hindex": numbers[2],
            "i10index": numbers[4],
        }

    pubs = []
    for row in re.findall(r'<tr class="gsc_a_tr">(.*?)</tr>', page, re.S):
        link = re.search(r'<a href="([^"]*)" class="gsc_a_at">(.*?)</a>', row, re.S)
        if not link:
            continue
        cfv = re.search(r"citation_for_view=([^&\"]+)", html.unescape(link.group(1)))
        cites = re.search(r'class="gsc_a_ac[^"]*">([^<]*)</a>', row)
        year = re.search(r'class="gsc_a_h[^"]*">([^<]*)</span>', row)
        gray = re.findall(r'class="gs_gray">(.*?)</div>', row, re.S)
        pubs.append(
            {
                "title": _text(link.group(2)),
                "cfv": cfv.group(1) if cfv else None,
                "authors": _text(gray[0]) if gray else "",
                "citations": int(cites.group(1)) if cites and cites.group(1).strip() else 0,
                "year": year.group(1).strip() if year else "",
            }
        )

    if len(pubs) < MIN_EXPECTED_PUBS:
        raise RuntimeError(
            f"only {len(pubs)} publications parsed (expected at least "
            f"{MIN_EXPECTED_PUBS}) — Scholar probably rate-limited this request"
        )

    if details:
        # The profile table truncates author lists; the detail pages do not.
        for pub in pubs:
            if not pub["cfv"]:
                continue
            try:
                detail = _get(
                    "https://scholar.google.com/citations?view_op=view_citation"
                    f"&hl=en&user={user_id}&citation_for_view={pub['cfv']}"
                )
            except (urllib.error.URLError, OSError) as exc:
                print(f"  warning: no detail for {pub['title'][:50]!r}: {exc}", file=sys.stderr)
                continue
            fields = {
                m.group(1): _text(m.group(2))
                for m in re.finditer(
                    r'<div class="gsc_oci_field">([^<]*)</div>'
                    r'<div class="gsc_oci_value">(.*?)</div>',
                    detail,
                    re.S,
                )
            }
            if fields.get("Authors"):
                pub["authors"] = fields["Authors"]
            url = re.search(r'class="gsc_oci_title_link" href="([^"]+)"', detail)
            if url:
                pub["url"] = html.unescape(url.group(1))
            time.sleep(1.5)  # be polite; Scholar blocks bursts

    return {"stats": stats, "pubs": pubs}


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------
def norm(title: str) -> str:
    """Key used to join Scholar titles with papers_meta.json entries.

    Accents are folded so 'responsabilità' and 'responsabilita' agree.
    """
    folded = unicodedata.normalize("NFKD", title.lower())
    return re.sub(r"[^a-z0-9]", "", folded)


def abbreviate(name: str) -> tuple[str, bool]:
    """'Giulio Rossolini' -> ('G. Rossolini', False). Returns (name, is_me)."""
    name = name.strip()
    star = "*" if name.endswith("*") else ""
    parts = name.rstrip("*").split()
    if not parts:
        return "", False
    surname = parts[-1]
    if len(parts) > 1 and len(surname) == 1:
        # Scholar writes some names surname-last-initial, e.g. "Vinod P".
        return f"{' '.join(parts[:-1])} {surname}.{star}", False
    initials = []
    for part in parts[:-1]:
        if part.isupper() and len(part) <= 3:      # already initials, e.g. "PG"
            initials.append(".".join(part) + ".")
        else:
            initials.append(part[0].upper() + ".")
    short = " ".join(initials + [surname]) + star
    is_me = surname.lower() == ME_SURNAME and (
        not initials or initials[0].startswith(ME_INITIAL)
    )
    return short, is_me


def render_authors(raw: str) -> str:
    out = []
    for name in raw.split(","):
        short, is_me = abbreviate(name)
        if not short:
            continue
        safe = html.escape(short)
        out.append(f'<span class="me">{safe}</span>' if is_me else safe)
    return ", ".join(out)


def render_paper(pub: dict, meta: dict) -> str:
    title = meta.get("title") or pub["title"]
    url = meta.get("url") or pub.get("url") or (
        f"https://scholar.google.com/citations?user={USER_ID}&hl=en"
    )
    venue = meta.get("venue", "Preprint")
    kind = meta.get("kind", "")
    year = pub.get("year", "")
    tags = list(meta.get("tags", []))
    if year:
        tags.append(year)

    css = f" is-{kind}" if kind in ("journal", "conference", "thesis") else ""
    foot = html.escape(meta.get("note", ""))
    if meta.get("code"):
        code = html.escape(meta["code"])
        foot += f' · <a href="{code}" target="_blank" rel="noopener">code</a>'

    return f"""
        <li class="paper" data-tags="{html.escape(' '.join(tags))}">
          <div class="paper-top">
            <span class="venue{css}">{html.escape(venue)}</span>
            <span class="year">{html.escape(year)}</span>
            <span class="cites"><i class="fas fa-quote-right"></i> {pub['citations']}</span>
          </div>
          <h3><a href="{html.escape(url)}" target="_blank" rel="noopener">{html.escape(title)}</a></h3>
          <p class="authors">{render_authors(pub['authors'])}</p>
          <div class="paper-foot">{foot}</div>
        </li>
"""


def render_stats(stats: dict, n_pubs: int) -> str:
    cells = [
        (stats.get("citations", "—"), "Citations"),
        (stats.get("hindex", "—"), "h-index"),
        (stats.get("i10index", "—"), "i10-index"),
        (str(n_pubs), "Publications"),
    ]
    items = "\n".join(
        f'        <li class="stat"><b>{html.escape(str(v))}</b><span>{label}</span></li>'
        for v, label in cells
    )
    return f'\n      <ul class="stats">\n{items}\n      </ul>\n      '


def replace_block(page: str, name: str, body: str) -> str:
    pattern = re.compile(
        f"(<!-- {name}:START -->).*?(<!-- {name}:END -->)", re.S
    )
    if not pattern.search(page):
        raise RuntimeError(f"marker <!-- {name}:START --> not found in {INDEX}")
    return pattern.sub(lambda m: m.group(1) + body + m.group(2), page, count=1)


# --------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true", help="do not write index.html")
    ap.add_argument("--from", dest="cache", metavar="FILE",
                    help="read a cached fetch_profile() payload instead of scraping")
    ap.add_argument("--save", metavar="FILE", help="save the scraped payload for reuse")
    ap.add_argument("--no-details", action="store_true",
                    help="skip per-paper pages (faster, truncated author lists)")
    args = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    os.chdir(here)

    with open(META, encoding="utf-8") as fh:
        meta_all = json.load(fh)

    if args.cache:
        with open(args.cache, encoding="utf-8") as fh:
            data = json.load(fh)
    else:
        try:
            data = fetch_profile(details=not args.no_details)
        except Exception as exc:                       # noqa: BLE001 - report and bail
            print(f"error: could not read Google Scholar: {exc}", file=sys.stderr)
            print("index.html was left unchanged.", file=sys.stderr)
            return 1

    if args.save:
        with open(args.save, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=1, ensure_ascii=False)

    pubs, unknown = [], []
    for pub in data["pubs"]:
        meta = meta_all.get(norm(pub["title"]))
        if meta is None:
            unknown.append(pub["title"])
            meta = {}
        elif meta.get("hide"):
            continue
        pubs.append((pub, meta))

    # Newest first; within a year, most cited first.
    pubs.sort(key=lambda p: (int(p[0]["year"] or 0), p[0]["citations"]), reverse=True)

    for title in unknown:
        print(f"note: no entry in {META} for {title!r} — rendered with defaults",
              file=sys.stderr)

    with open(INDEX, encoding="utf-8") as fh:
        page = fh.read()

    body = "".join(render_paper(pub, meta) for pub, meta in pubs)
    updated = page
    updated = replace_block(updated, "PAPERS",
                            f'\n      <ul class="papers" id="paper-list">\n{body}\n      </ul>\n      ')
    updated = replace_block(updated, "STATS", render_stats(data.get("stats", {}), len(pubs)))
    updated = replace_block(
        updated, "UPDATED",
        datetime.now(timezone.utc).strftime("%-d %B %Y") if os.name != "nt"
        else date.today().strftime("%d %B %Y"),
    )

    print(f"{len(pubs)} publications · {data.get('stats', {}).get('citations', '?')} citations")

    if args.dry_run:
        print("dry run: index.html not written")
        return 0
    if updated == page:
        print("index.html already up to date")
        return 0

    with open(INDEX, "w", encoding="utf-8") as fh:
        fh.write(updated)
    print("index.html updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
