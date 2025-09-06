from scholarly import scholarly

USER_ID = "hhNQwfkAAAAJ"  # il tuo ID da Scholar (preso dall'URL)

def main():
    author = scholarly.search_author_id(USER_ID)
    author = scholarly.fill(author, sections=["publications"])

    with open("index.html", "w", encoding="utf-8") as f:
        f.write("<!DOCTYPE html>\n<html lang='it'>\n<head>\n")
        f.write("<meta charset='UTF-8'>\n<title>Pubblicazioni</title>\n</head>\n<body>\n")
        f.write(f"<h1>Pubblicazioni di {author['name']}</h1>\n<ul>\n")

        for pub in author['publications']:
            title = pub['bib']['title']
            year = pub['bib'].get('pub_year', 'N/A')
            citations = pub.get('num_citations', 0)
            f.write(f"<li><b>{title}</b> ({year}) - Citazioni: {citations}</li>\n")

        f.write("</ul>\n</body>\n</html>")

if __name__ == "__main__":
    main()
