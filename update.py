from scholarly import scholarly

USER_ID = "hhNQwfkAAAAJ"  # your Google Scholar ID

def main():
    author = scholarly.search_author_id(USER_ID)
    author = scholarly.fill(author, sections=["publications"])

    html_top = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Marco Simoni - Academic Page</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  <style>
    body {
      font-family: "Segoe UI", Arial, sans-serif;
      max-width: 1000px;
      margin: 0 auto;
      padding: 0;
      background: #fafafa;
      color: #333;
      line-height: 1.6;
    }
    header {
      text-align: center;
      padding: 2rem 1rem;
      background: linear-gradient(135deg, #2c3e50, #3498db);
      color: white;
    }
    header img {
      width: 150px;
      height: 150px;
      border-radius: 50%;
      border: 4px solid white;
      margin-bottom: 1rem;
    }
    h1 {
      font-size: 2.6rem;
      margin-bottom: 0.3rem;
    }
    p.subtitle {
      font-size: 1.2rem;
      color: #eee;
      margin-bottom: 1rem;
    }
    .social-links a {
      margin: 0 0.7rem;
      font-size: 1.5rem;
      color: white;
      text-decoration: none;
    }
    .social-links a:hover {
      color: #f1c40f;
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
      padding: 2rem;
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
      padding: 1rem 1.5rem;
      margin-bottom: 1rem;
      border-radius: 10px;
      box-shadow: 0 3px 8px rgba(0,0,0,0.08);
      transition: transform 0.2s;
    }
    ul.paper-list li:hover {
      transform: scale(1.02);
    }
    .paper-title {
      font-weight: bold;
      font-size: 1.1rem;
      margin-bottom: 0.3rem;
      color: #2c3e50;
    }
    .paper-title a {
      color: inherit;
      text-decoration: none;
    }
    .paper-title a:hover {
      text-decoration: underline;
      color: #2980b9;
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
    <img src="profile.png" alt="Marco Simoni">
    <h1>Marco Simoni</h1>
    <p class="subtitle">Cybersecurity & Artificial Intelligence Researcher</p>
    <div class="social-links">
      <a href="https://www.linkedin.com/in/marco-simoni-ba1a06242/" target="_blank"><i class="fab fa-linkedin"></i></a>
      <a href="https://github.com/winstonsmith1897" target="_blank"><i class="fab fa-github"></i></a>
      <a href="https://scholar.google.com/citations?user=hhNQwfkAAAAJ&hl=en" target="_blank"><i class="fas fa-graduation-cap"></i></a>
    </div>
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

    html_bottom = """      </ul>
    </section>

    <section id="projects">
      <h2>Projects</h2>
      <p>Coming soon...</p>
    </section>
  </main>

  <footer>
    &copy; 2025 Marco Simoni – Powered by GitHub Pages &amp; Google Scholar
  </footer>
</body>
</html>"""

    items = []
    for pub in author['publications']:
        pub_filled = scholarly.fill(pub)
        title = pub_filled['bib']['title']
        year = pub_filled['bib'].get('pub_year', 'N/A')
        citations = pub_filled.get('num_citations', 0)

        # Try to get external link (DOI/arXiv if available)
        url = pub_filled.get("pub_url", f"https://scholar.google.com/citations?user={USER_ID}&hl=en")

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
