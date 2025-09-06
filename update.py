from scholarly import scholarly

USER_ID = "hhNQwfkAAAAJ"  # your Google Scholar ID

def main():
    # Fetch author and publications
    author = scholarly.search_author_id(USER_ID)
    author = scholarly.fill(author, sections=["publications"])

    # HTML header
    html_top = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Winston Smith - Academic Page</title>
  <style>
    body {
      font-family: "Segoe UI", Arial, sans-serif;
      max-width: 950px;
      margin: 2rem auto;
      padding: 0 1.5rem;
      background: #fdfdfd;
      color: #333;
      line-height: 1.6;
    }
    header {
      text-align: center;
      margin-bottom: 3rem;
    }
    h1 {
      font-size: 2.4rem;
      margin-bottom: 0.5rem;
    }
    h2 {
      margin-top: 2.5rem;
      border-bottom: 2px solid #ddd;
      padding-bottom: 0.4rem;
    }
    p.subtitle {
      font-size: 1.1rem;
      color: #555;
    }
    ul.paper-list {
      list-style: none;
      padding: 0;
    }
    ul.paper-list li {
      background: #fff;
      padding: 1rem;
      margin-bottom: 1rem;
      border-radius: 8px;
      box-shadow: 0 2px 5px rgba(0,0,0,0.08);
    }
    .paper-title {
      font-weight: bold;
      font-size: 1.05rem;
      margin-bottom: 0.3rem;
    }
    .paper-meta {
      font-size: 0.9rem;
      color: #666;
    }
    footer {
      margin-top: 3rem;
      text-align: center;
      font-size: 0.85rem;
      color: #888;
    }
  </style>
</head>
<body>
  <header>
    <h1>Winston Smith</h1>
    <p class="subtitle">Academic Page – Automatically updated from Google Scholar</p>
  </header>

  <main>
    <section id="about">
      <h2>About Me</h2>
      <p>
        I am a researcher in Cybersecurity and Artificial Intelligence. 
        My work focuses on malware analysis, knowledge graphs, and the 
        application of large language models to cyber threat intelligence.
      </p>
    </section>

    <section id="papers">
      <h2>Papers</h2>
      <ul class="paper-list">
"""

    # HTML footer
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

    # Build list of papers
    items = []
    for pub in author['publications']:
        title = pub['bib']['title']
        year = pub['bib'].get('pub_year', 'N/A')
        citations = pub.get('num_citations', 0)
        scholar_link = f"https://scholar.google.com/citations?user={USER_ID}&hl=en"

        item = f"""
        <li>
          <div class="paper-title">
            <a href="{scholar_link}" target="_blank">{title}</a>
          </div>
          <div class="paper-meta">Year: {year} • Citations: {citations}</div>
        </li>
"""
        items.append(item)

    # Write final HTML
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_top + "".join(items) + html_bottom)

if __name__ == "__main__":
    main()
