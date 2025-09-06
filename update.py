from scholarly import scholarly

USER_ID = "hhNQwfkAAAAJ"  # your Google Scholar ID

def main():
    author = scholarly.search_author_id(USER_ID)
    author = scholarly.fill(author, sections=["publications"])

    html_top = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Winston Smith - Academic Page</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 950px; margin: auto; padding: 0 1rem; background: #fdfdfd; color: #333; }
    header { text-align: center; margin: 2rem 0; }
    nav { background: #333; padding: 0.8rem; text-align: center; }
    nav a { color: white; text-decoration: none; margin: 0 1rem; font-weight: bold; }
    nav a:hover { text-decoration: underline; }
    h1 { margin: 0.2rem 0; }
    h2 { margin-top: 2.5rem; border-bottom: 2px solid #ddd; padding-bottom: 0.3rem; }
    ul.paper-list { list-style: none; padding: 0; }
    ul.paper-list li { background: #fff; padding: 1rem; margin: 1rem 0; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.08); }
    .paper-title { font-weight: bold; font-size: 1.05rem; margin-bottom: 0.3rem; }
    .paper-meta { font-size: 0.9rem; color: #666; }
    footer { text-align: center; margin: 3rem 0 1rem 0; color: #888; font-size: 0.85rem; }
  </style>
</head>
<body>
  <header>
    <h1>Winston Smith</h1>
    <p class="subtitle">Academic Page – Automatically updated from Google Scholar</p>
  </header>

  <nav>
    <a href="#about">About</a>
    <a href="#papers">Papers</a>
    <a href="#projects">Projects</a>
  </nav>

  <main>
    <section id="about">
      <h2>About Me</h2>
      <p>I am a researcher in Cybersecurity and Artificial Intelligence. My work focuses on malware analysis, knowledge graphs, and the application of large language models to cyber threat intelligence.</p>
    </section>

    <section id="papers">
      <h2>Papers</h2>
      <ul class="paper-list">
"""

    html_bottom = """      </ul>
    </section>

    <section id="projects">
      <h2>Projects</h2>
      <p>Coming soon...</p>
    </section>
  </main>

  <footer>
    &copy; 2025 Winston Smith – Powered by GitHub Pages &amp; Google Scholar
  </footer>
</body>
</html>"""

    items = []
    for pub in author['publications']:
        # Fill each publication to get more details
        pub_filled = scholarly.fill(pub)
        title = pub_filled['bib']['title']
        year = pub_filled['bib'].get('pub_year', 'N/A')
        citations = pub_filled.get('num_citations', 0)

        # Try to get DOI / external URL
        url = pub_filled.get("pub_url", None)
        if not url:
            url = f"https://scholar.google.com/citations?user={USER_ID}&hl=en"

        items.append(f"""
        <li>
          <div class="paper-title"><a href="{url}" target="_blank">{title}</a></div>
          <div class="paper-meta">Year: {year} • Citations: {citations}</div>
        </li>
""")

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_top + "".join(items) + html_bottom)

if __name__ == "__main__":
    main()
