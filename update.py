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
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  <style>
    :root {
      --bg-color: #fafafa;
      --text-color: #333;
      --card-bg: #fff;
      --header-bg: linear-gradient(135deg, #2c3e50, #3498db);
      --link-hover: #f1c40f;
    }
    [data-theme="dark"] {
      --bg-color: #121212;
      --text-color: #f0f0f0;
      --card-bg: #1e1e1e;
      --header-bg: linear-gradient(135deg, #000, #222);
      --link-hover: #f39c12;
    }
    body { font-family: 'Poppins', sans-serif; max-width: 1100px; margin: 0 auto; background: var(--bg-color); color: var(--text-color); line-height: 1.6; transition: background 0.3s, color 0.3s; }
    header { text-align: center; padding: 2rem 1rem; background: var(--header-bg); color: white; }
    header img { width: 150px; height: 150px; border-radius: 50%; border: 4px solid white; margin-bottom: 1rem; }
    h1 { font-size: 2.6rem; margin-bottom: 0.3rem; }
    p.subtitle { font-size: 1.2rem; color: #eee; margin-bottom: 1rem; }
    .social-links a { margin: 0 0.7rem; font-size: 1.5rem; color: white; text-decoration: none; transition: color 0.3s; }
    .social-links a:hover { color: var(--link-hover); }

    /* Navbar */
    nav { background: #333; padding: 0.8rem; display: flex; justify-content: center; align-items: center; gap: 2rem; position: sticky; top: 0; z-index: 1000; }
    nav a { color: white; text-decoration: none; font-weight: bold; position: relative; font-size: 1rem; }
    nav a::after { content: ""; display: block; height: 2px; background: var(--link-hover); transition: width 0.3s; width: 0; margin: auto; }
    nav a:hover::after { width: 100%; }

    /* Toggle button */
    .theme-toggle { margin-left: auto; cursor: pointer; color: white; font-size: 1.2rem; }

    main { padding: 2rem; }
    h2 { margin-top: 2.5rem; border-bottom: 2px solid #ddd; padding-bottom: 0.4rem; }

    /* Alternating section background */
    section:nth-of-type(even) { background: rgba(0,0,0,0.03); padding: 2rem; border-radius: 12px; }

    /* Papers grid */
    ul.paper-list { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 1rem; padding: 0; list-style: none; }
    ul.paper-list li { background: var(--card-bg); padding: 1rem 1.5rem; border-radius: 10px; box-shadow: 0 3px 8px rgba(0,0,0,0.08); transition: transform 0.2s, box-shadow 0.3s, background 0.3s; }
    ul.paper-list li:hover { transform: translateY(-5px); box-shadow: 0 6px 12px rgba(0,0,0,0.15); }
    .paper-title { font-weight: bold; font-size: 1.05rem; margin-bottom: 0.3rem; color: var(--text-color); }
    .paper-title a { color: inherit; text-decoration: none; }
    .paper-title a:hover { text-decoration: underline; color: #2980b9; }
    .paper-meta { font-size: 0.9rem; color: #888; }

    /* Articles */
    .article-card { background: var(--card-bg); padding: 1.5rem; margin-bottom: 1rem; border-radius: 10px; box-shadow: 0 3px 8px rgba(0,0,0,0.08); transition: transform 0.2s, background 0.3s; }
    .article-card:hover { transform: translateY(-5px); }

    /* Projects */
    .project-card { background: var(--card-bg); padding: 1.5rem; margin-bottom: 1rem; border-radius: 10px; box-shadow: 0 3px 8px rgba(0,0,0,0.08); transition: background 0.3s; }
    .project-card h3 { margin-top: 0; }
    .project-card iframe { width: 100%; height: 315px; max-width: 700px; border-radius: 8px; }

    footer { margin-top: 3rem; padding: 1rem; text-align: center; font-size: 0.85rem; color: #888; border-top: 1px solid #eee; }
  </style>
</head>
<body data-theme="light">
  <header>
    <img src="profile.png" alt="Marco Simoni">
    <h1>Marco Simoni</h1>
    <p class="subtitle">Researcher in AI, LLMs, Reinforcement Learning & Cybersecurity</p>
    <div class="social-links">
      <a href="https://www.linkedin.com/in/marco-simoni-ba1a06242/" target="_blank"><i class="fab fa-linkedin"></i></a>
      <a href="https://github.com/winstonsmith1897" target="_blank"><i class="fab fa-github"></i></a>
      <a href="https://scholar.google.com/citations?user=hhNQwfkAAAAJ&hl=en" target="_blank"><i class="fas fa-graduation-cap"></i></a>
      <a href="https://medium.com/@marco.simoni0711" target="_blank"><i class="fab fa-medium"></i></a>
      <a href="mailto:marco.simoni@iit.cnr.it"><i class="fas fa-envelope"></i></a>
    </div>
  </header>

  <nav>
    <a href="#about">About</a>
    <a href="#papers">Papers</a>
    <a href="#articles">Articles</a>
    <a href="#projects">Projects</a>
    <div class="theme-toggle" onclick="toggleTheme()">
      <i class="fas fa-moon"></i>
    </div>
  </nav>

  <main>
    <section id="about">
      <h2>About Me</h2>
      <p>
        I am a researcher passionate about <b>Large Language Models (LLMs)</b> 
        and their alignment through <b>Reinforcement Learning (RL)</b>. 
        My work explores how advanced RL techniques such as GRPO and GTPO 
        can improve reasoning stability and trustworthiness in LLMs. 
        While I have applied these methods to domains like cybersecurity, 
        my main focus is on pushing the boundaries of <b>AI alignment</b> 
        and building smarter, more reliable models.
      </p>
    </section>

    <section id="papers">
      <h2>Papers</h2>
      <ul class="paper-list">
"""

    html_bottom = """      </ul>
    </section>

    <section id="articles">
      <h2>Articles</h2>
      <div class="article-card">
        <h3><a href="https://medium.com/@marco.simoni0711/gtpo-vs-grpo-a-smarter-path-to-stable-reasoning-llms-3f51bc0b58c1" target="_blank">
          GTPO vs GRPO: A Smarter Path to Stable Reasoning LLMs
        </a></h3>
        <p>
          In this piece I discuss the differences between <b>GRPO</b> and <b>GTPO</b>, 
          two reinforcement learning approaches designed to stabilize and align 
          large language models. Why is <b>alignment</b> crucial for reasoning? 
          Because RL can make LLMs not only more powerful, but also more trustworthy.
        </p>
      </div>
    </section>

    <section id="projects">
      <h2>Projects</h2>

      <div class="project-card">
        <h3>Mixture of RAG Security Experts (MoRSE)</h3>
        <div style="text-align:center; margin: 1rem 0;">
          <iframe 
            src="https://www.youtube.com/embed/nsI1HCUVDSc" 
            title="YouTube video player" 
            frameborder="0" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
            allowfullscreen>
          </iframe>
        </div>
        <p>
          I introduce the first specialised AI chatbot for cybersecurity <b>MoRSE (Mixture of RAGs Security Experts)</b>, 
          which aims to provide comprehensive and complete knowledge about cybersecurity. 
          MoRSE uses two <b>Retrieval Augmented Generation (RAG)</b> systems designed to provide 
          clear, structured, and accurate answers to cybersecurity queries. 
          Unlike traditional <b>Large Language Models (LLMs)</b> that rely on Parametric Knowledge Bases, 
          MoRSE retrieves relevant documents from Non-Parametric Knowledge Bases in response to user queries. 
          It then uses this information to generate accurate answers, improving cybersecurity accuracy and reliability. 
          In addition, MoRSE benefits from real-time updates to its knowledge bases, enabling continuous 
          knowledge enrichment without retraining.
        </p>
      </div>
    </section>
  </main>


  <footer>
    &copy; 2025 Marco Simoni – Powered by GitHub Pages &amp; Google Scholar
  </footer>

  <script>
    function toggleTheme() {
      const body = document.body;
      const toggleIcon = document.querySelector(".theme-toggle i");
      if (body.getAttribute("data-theme") === "light") {
        body.setAttribute("data-theme", "dark");
        toggleIcon.classList.remove("fa-moon");
        toggleIcon.classList.add("fa-sun");
      } else {
        body.setAttribute("data-theme", "light");
        toggleIcon.classList.remove("fa-sun");
        toggleIcon.classList.add("fa-moon");
      }
    }
  </script>
</body>
</html>"""

    items = []
    for pub in author['publications']:
        pub_filled = scholarly.fill(pub)
        title = pub_filled['bib']['title']
        year = pub_filled['bib'].get('pub_year', 'N/A')
        citations = pub_filled.get('num_citations', 0)
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
