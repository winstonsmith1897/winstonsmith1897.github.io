# winstonsmith1897.github.io

Personal academic page — [winstonsmith1897.github.io](https://winstonsmith1897.github.io/).

Static, no build step: `index.html` carries its own CSS and JS and is served
directly by GitHub Pages.

## Files

| Path | Purpose |
|:--|:--|
| `index.html` | The whole site. Edit it directly. |
| `update.py` | Refreshes the publication list from Google Scholar. |
| `papers_meta.json` | Venue labels, canonical links and filter tags per paper. |
| `videos/*.mp4` | Demo screencasts (`.gif` originals kept as a fallback). |
| `.github/workflows/update.yml` | Weekly attempt to run `update.py` automatically. |

## Updating the publications

```bash
python update.py             # fetch Scholar and rewrite index.html
python update.py --dry-run   # show what would change, write nothing
```

`update.py` needs only the standard library. It **does not regenerate the
page** — it rewrites just the three marked regions:

```html
<!-- PAPERS:START -->  ... the publication cards ...  <!-- PAPERS:END -->
<!-- STATS:START -->   ... citations / h-index ...    <!-- STATS:END -->
<!-- UPDATED:START -->  the "last updated" date       <!-- UPDATED:END -->
```

Everything else — layout, about text, projects, articles — is hand-written and
survives an update. Keep those comments in place or the script will refuse to
run.

> The earlier version of this script rebuilt `index.html` from a template
> embedded in the script itself, so every successful run silently reverted any
> manual edit to the page. That is why it is marker-based now.

### When a paper appears with the wrong venue

Scholar's venue strings are inconsistent, so anything presentational lives in
`papers_meta.json`, keyed by the title lowercased with all punctuation, spaces
and accents removed:

```json
"titanexecutablereasoningforcyberthreatintelligence": {
  "title": "TITAN: Graph-Executable Reasoning for Cyber Threat Intelligence",
  "venue": "arXiv",
  "kind":  "preprint",
  "note":  "arXiv:2510.14670",
  "url":   "https://arxiv.org/abs/2510.14670",
  "code":  "https://github.com/cti-graph-reasoner/TITAN",
  "tags":  ["kg", "security"]
}
```

`kind` is one of `journal`, `conference`, `thesis`, `preprint` and picks the
badge colour. `tags` drives the filter buttons (`rl`, `security`, `kg`); the
year button is added automatically. Set `"hide": true` to keep a Scholar entry
off the page. A publication with no entry here still renders, using Scholar's
own data and a generic badge, and the script prints a note about it.

## About the GitHub Action

The workflow runs weekly, but **Google Scholar usually blocks GitHub-hosted
runners**, which is why the original daily job never produced a single commit.
When Scholar refuses, `update.py` exits non-zero *without writing anything*, so
a failed run is visible in the Actions tab and never damages the live page.

If it keeps failing, just run `python update.py` from a normal network and push
the result.

## Demo videos

The `.mp4` files are h264 conversions of the original GIFs (78 MB → 21 MB).
The page shows a poster image and loads a video only when the visitor clicks
play. To regenerate one after replacing a GIF:

```bash
ffmpeg -i videos/demo1.gif -movflags +faststart -pix_fmt yuv420p \
       -vf "scale='min(1280,iw)':-2:flags=lanczos" \
       -c:v libx264 -crf 33 -preset veryslow -tune animation -an videos/demo1.mp4
ffmpeg -i videos/demo1.gif -vframes 1 -vf "scale='min(900,iw)':-2" -q:v 7 videos/demo1.jpg
```
