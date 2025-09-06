from scholarly import scholarly

USER_ID = "hhNQwfkAAAAJ"  # il tuo ID da Scholar

def main():
    # Recupera autore e pubblicazioni
    author = scholarly.search_author_id(USER_ID)
    author = scholarly.fill(author, sections=["publications"])

    # HTML di base
    html_top = """<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <title>Pubblicazioni - Winston Smith</title>
  <style>
    body {
      font-family: "Segoe UI", Arial, sans-serif;
      max-width: 900px;
      margin: 2rem auto;
      padding: 0 1.5rem;
      background: #f9f9f9;
      color: #333;
    }
    header {
      text-align: center;
      margin-bottom: 2rem;
    }
    h1 {
      font-size: 2.2rem;
      margin-bottom: 0.5rem;
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
      box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .paper-title {
      font-weight: bold;
      font-size: 1.1rem;
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
    <h1>Pubblicazioni di Winston Smith</h1>
    <p class="subtitle">Lista aggiornata automaticamente da Google Scholar</p>
  </header>

  <main>
    <ul class="paper-list">
"""

    html_bottom = """    </ul>
  </main>

  <footer>
    &copy; 2025 Winston Smith – Powered by GitHub Pages &amp; Google Scholar
  </footer>
</body>
</html>"""

    # Costruisci la lista dei paper
    items = []
    for pub in author['publications']:
        title = pub['bib']['title']
        year = pub['bib'].get('pub_year', 'N/A')
        citations = pub.get('num_citations', 0)

        # Link diretto alla pagina Scholar del paper (se disponibile)
        scholar_link = f"https://scholar.google.com/citations?view_op=view_citation&hl=it&user={USER_ID}&citation_for_view={pub['author_id']}"

        item = f"""
      <li>
        <div class="paper-title">
          <a href="{scholar_link}" target="_blank">{title}</a>
        </div>
        <div class="paper-meta">Anno: {year} • Citazioni: {citations}</div>
      </li>
"""
        items.append(item)

    # Scrivi il file completo
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_top + "".join(items) + html_bottom)

if __name__ == "__main__":
    main()
