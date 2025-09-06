from scholarly import scholarly

USER_ID = "hhNQwfkAAAAJ"  # your Google Scholar ID

def main():
    # Fetch author and publications
    author = scholarly.search_author_id(USER_ID)
    author = scholarly.fill(author, sections=["publications"])

    # HTML header with navbar
    html_top = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Winston Smith - Academic Page</title>
  <style>
    body {
      font-family: "Segoe UI", Arial, sans-serif;
      max-width: 1000px;
      margin: 0 auto;
      padding: 0;
      background: #fdfdfd;
      color: #333;
      line-height: 1.6;
    }
    header {
      text-align: center;
      padding: 2rem 1rem 1rem 1rem;
    }
    h1 {
      font-size: 2.4rem;
      margin-bottom: 0.2rem;
    }
    p.subtitle {
      font-size: 1.1rem;
      color: #555;
    }
    nav {
      background: #333;
      padding: 0.8rem;
      text-align: center;
    }
    nav a {
      color: white;
      text-decoration: none;
      margin: 0 1rem;
      font-weight: bold;
    }
    nav a:hover {
      text-decoration: underline;
    }
    main {
      padding: 1.5rem;
    }
    h2 {
      margin-top: 2.5rem;
      border-bottom: 2px solid #ddd;
      padding-bottom: 0.4rem;
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
      padding: 1rem;
      text-align: center;
      font-size: 0.85rem;
      color: #888;
      border-top: 1px solid #eee;
    }
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
