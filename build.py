#!/usr/bin/env python3
"""
Збирає сайт з Markdown-файлів у звичайні HTML-сторінки (для Google).

  home.md          -> index.html
  01-block-1x1.md  -> 01-block-1x1.html   (усі файли, що починаються з двох цифр)
  _sidebar.md      -> меню зліва і порядок «Попередній / Наступний»

Запускається автоматично через GitHub Actions після кожної зміни.
Вручну:  pip install markdown-it-py  &&  python build.py
"""
import datetime
import glob
import hashlib
import html
import json
import os
import re

from markdown_it import MarkdownIt

SITE_URL = "https://valik31.github.io/FreeCAD_TASK_UA/"
SITE_NAME = "Уроки FreeCAD українською"
DEFAULT_IMAGE = "block2x4-10.jpg"
ROOT = os.path.dirname(os.path.abspath(__file__))

md = MarkdownIt("commonmark", {"html": True, "typographer": False}).enable(["table", "strikethrough"])


# ---------------------------------------------------------------- helpers
def read(name):
    with open(os.path.join(ROOT, name), encoding="utf-8") as f:
        return f.read()


def write(name, text):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", " ", s)).replace("\xa0", " ")


def squash(s):
    return re.sub(r"\s+", " ", s).strip()


def page_of(md_name):
    """home.md -> index.html, 01-x.md -> 01-x.html"""
    base = os.path.basename(md_name)[:-3]
    return "index.html" if base in ("home", "README") else base + ".html"


def fix_links(h):
    """Посилання з Docsify-формату (#/x, x.md) -> x.html"""
    def repl(m):
        q, url = m.group(1), m.group(2)
        if re.match(r"^(https?:|mailto:|//)", url):
            return m.group(0)
        new = url
        if url in ("#/", "#", "home.md", "README.md", "#/home", "#/README"):
            new = "index.html"
        elif url.startswith("#/"):
            new = url[2:].split("?")[0]
            new = (new[:-3] if new.endswith(".md") else new) + ".html"
        elif url.endswith(".md"):
            new = page_of(url)
        return f"href={q}{new}{q}"
    return re.sub(r'href=(["\'])([^"\']*)\1', repl, h)


def slugify(text):
    s = re.sub(r"[^\w\s-]", "", text.lower(), flags=re.U)
    return re.sub(r"[\s_]+", "-", s).strip("-") or "section"


def add_heading_ids(h):
    used = set()

    def repl(m):
        tag, inner = m.group(1), m.group(2)
        sid = base = slugify(strip_tags(inner))
        i = 2
        while sid in used:
            sid = f"{base}-{i}"
            i += 1
        used.add(sid)
        return f'<{tag} id="{sid}">{inner}</{tag}>'
    return re.sub(r"<(h[23])>(.*?)</\1>", repl, h, flags=re.S)


def enhance(h):
    h = fix_links(h)
    h = add_heading_ids(h)
    # YouTube: ліниве завантаження + назва для доступності
    h = re.sub(r"<iframe (?![^>]*loading=)", '<iframe loading="lazy" title="Відеоурок" ', h)
    # картинки: ліниве завантаження (крім іконок)
    h = re.sub(r'<img (?![^>]*class="ic")(?![^>]*loading=)', '<img loading="lazy" ', h)
    return h


# ---------------------------------------------------------------- sidebar
def build_sidebar():
    side_md = read("_sidebar.md")
    order = []
    for m in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", side_md):
        title, link = m.group(1), m.group(2)
        page = page_of(link) if link.endswith(".md") else link
        order.append((title, page))
    nav = fix_links(md.render(side_md))
    # data-lesson для галочок прогресу
    nav = re.sub(r'href="((\d{2}-[^"/]+)\.html)"', r'href="\1" data-lesson="\2"', nav)
    return nav, order


# ---------------------------------------------------------------- template
TEMPLATE = """<!DOCTYPE html>
<html lang="uk">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}">
  <link rel="icon" type="image/svg+xml" href="favicon.svg">
  <link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">
  <link rel="apple-touch-icon" href="apple-touch-icon.png">
  <meta name="theme-color" content="#c0392b">
  <meta property="og:type" content="{og_type}">
  <meta property="og:locale" content="uk_UA">
  <meta property="og:site_name" content="{site_name}">
  <meta property="og:title" content="{og_title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{image}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Google+Sans:wght@400..700&display=swap">
  <link rel="stylesheet" href="style.css?v={ver}">
  <script type="application/ld+json">{jsonld}</script>
</head>
<body class="{body_class}" data-lesson="{lesson_id}">
  <button class="menu-btn" aria-label="Меню">☰</button>
  <aside class="sidebar">
    <a class="site-name" href="index.html">FreeCAD: уроки</a>
    <div class="search">
      <input type="search" placeholder="Пошук…" aria-label="Пошук по уроках">
      <div class="search-results"></div>
    </div>
    <nav class="sidebar-nav">
{nav}
    </nav>
  </aside>
  <main class="content">
    <article class="markdown-section">
{body}
{done_box}
    </article>
{pager}
  </main>
  <script src="site.js?v={ver}"></script>
</body>
</html>
"""

DONE_BOX = """<div class="done-box">
  <button class="done-btn">Позначити як виконане</button>
  <div class="done-hint">Позначка зберігається в цьому браузері</div>
</div>"""


def pager_html(order, page):
    pages = [p for _, p in order]
    if page not in pages:
        return ""
    i = pages.index(page)
    prev_ = order[i - 1] if i > 0 else None
    next_ = order[i + 1] if i + 1 < len(order) else None
    parts = ['<nav class="pager">']
    if prev_:
        parts.append(f'<a class="prev" href="{prev_[1]}"><small>← Попередній</small>{html.escape(prev_[0])}</a>')
    else:
        parts.append("<span></span>")
    if next_:
        parts.append(f'<a class="next" href="{next_[1]}"><small>Наступний →</small>{html.escape(next_[0])}</a>')
    parts.append("</nav>")
    return "\n".join(parts)


# ---------------------------------------------------------------- build
def main():
    nav, order = build_sidebar()
    sources = ["home.md"] + sorted(f for f in glob.glob(os.path.join(ROOT, "[0-9][0-9]-*.md")))
    sources = [os.path.basename(s) for s in sources]
    ver = hashlib.md5((read("style.css") + read("site.js")).encode()).hexdigest()[:8]
    search_index, sitemap = [], []
    known = []

    for src in sources:
        page = page_of(src)
        is_home = page == "index.html"
        text = read(src)
        body = enhance(md.render(text))

        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S)
        h1_text = squash(strip_tags(h1.group(1))) if h1 else SITE_NAME

        # опис для Google: «Що навчимося» або перший абзац
        desc = ""
        m = re.search(r"<p>\s*<strong>Що навчимося:</strong>(.*?)</p>", body, re.S)
        if m:
            desc = squash(strip_tags(m.group(1)))
        else:
            for p in re.findall(r"<p>(.*?)</p>", body, re.S):
                t = squash(strip_tags(p))
                if len(t) > 40:
                    desc = t
                    break
        if is_home:
            desc = ("Безкоштовні відеоуроки та покрокові інструкції з 3D-моделювання у FreeCAD "
                    "українською: блок LEGO 1×1, пластинка 1×2, блок 2×4, LEGO-чоловічок.")
        else:
            desc = re.sub(r"\s+([,.;:!?])", r"\1", desc)
            desc = f"{h1_text}: відеоурок і покрокова інструкція FreeCAD українською." + (f" Навчимося {desc}" if desc else "")
        if len(desc) > 200:
            desc = desc[:197].rsplit(" ", 1)[0] + "…"

        img = re.search(r'<img (?![^>]*class="ic")[^>]*src="([^"]+\.(?:jpg|jpeg|png))"', body)
        image = SITE_URL + (img.group(1) if img else DEFAULT_IMAGE)

        url = SITE_URL if is_home else SITE_URL + page
        title = (f"Уроки FreeCAD українською — 3D-моделювання деталей LEGO" if is_home
                 else f"{h1_text} — {SITE_NAME}")
        lesson_id = "" if is_home else page[:-5]

        jsonld = {
            "@context": "https://schema.org",
            "@type": "WebSite" if is_home else "LearningResource",
            "name": h1_text if not is_home else SITE_NAME,
            "url": url,
            "inLanguage": "uk",
            "description": desc,
        }
        if not is_home:
            jsonld["educationalLevel"] = "Старша школа"
            jsonld["learningResourceType"] = "Відеоурок та інструкція"
            jsonld["isPartOf"] = {"@type": "WebSite", "name": SITE_NAME, "url": SITE_URL}

        out = TEMPLATE.format(
            title=html.escape(title), desc=html.escape(desc), url=url, image=image,
            og_type="website" if is_home else "article", og_title=html.escape(title),
            site_name=SITE_NAME, ver=ver, jsonld=json.dumps(jsonld, ensure_ascii=False),
            body_class="home" if is_home else "lesson", lesson_id=lesson_id,
            nav=nav, body=body, done_box="" if is_home else DONE_BOX,
            pager=pager_html(order, page),
        )
        # активний пункт меню
        out = out.replace(f'href="{page}"', f'href="{page}" class="active"', 1) if not is_home else out
        write(page, out)
        known.append(page[:-5])

        search_index.append({
            "url": page, "title": h1_text,
            "text": squash(strip_tags(re.sub(r"<h1.*?</h1>", "", body, flags=re.S))),
        })
        sitemap.append(url)
        print("✓", src, "->", page)

    write("search.json", json.dumps(search_index, ensure_ascii=False))
    today = datetime.date.today().isoformat()
    write("sitemap.xml",
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>\n" for u in sitemap)
          + "</urlset>\n")

    # 404
    write("404.html", TEMPLATE.format(
        title="Сторінку не знайдено — " + SITE_NAME, desc="Сторінку не знайдено", url=SITE_URL,
        image=SITE_URL + DEFAULT_IMAGE, og_type="website", og_title="Сторінку не знайдено",
        site_name=SITE_NAME, ver=ver, jsonld="{}", body_class="notfound", lesson_id="", nav=nav,
        body='<h1>Сторінку не знайдено</h1><p><a href="index.html">← На головну</a></p>',
        done_box="", pager="").replace("<head>", f'<head>\n  <base href="{SITE_URL}">', 1))
    print("✓ search.json, sitemap.xml, 404.html")


if __name__ == "__main__":
    main()
