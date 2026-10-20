import requests
from bs4 import BeautifulSoup
import time
import os

# 多本小說清單： (網址, 書名, 作者)
novels = [
    # 半夏小說
    ("https://www.banxia.la/books/269232.html", "玄學大師只想退圈", "廿亂"),
]

def get_chapter_links(toc_url):
    resp = requests.get(toc_url, headers={"User-Agent": "Mozilla/5.0"})
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'html.parser')
    links = []
    for a in soup.select("div.book-list ul li a"):
        title = a.get('title', a.text).strip()
        href = a['href']
        full_url = requests.compat.urljoin(toc_url, href)
        links.append((title, full_url))
    return links

def fetch_chapter_content(url):
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'html.parser')
    title = soup.find("h1", id="nr_title").get_text(strip=True)
    content_div = soup.find("div", id="nr1")
    for br in content_div.find_all("br"):
        br.replace_with("\n")
    content = content_div.get_text(separator="\n", strip=True)
    return title, content

import time

def save_book_with_hash_navigation(chapters, output_file, html_title):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html_title}</title>
<style>
body {{
    background-color: #1e1e1e;
    color: #f0f0f0;
    font-family: sans-serif;
    font-size: 1rem;
    padding: 1.25rem;
    margin: 0;
}}

.chapter {{
    display: none;
}}

#menu {{
    display: none;
}}

nav {{
    margin: 1rem 0;
    text-align: center;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.5rem;
}}

button {{
    padding: 0.5rem 1rem;
    background: #333;
    color: white;
    border: 1px solid #555;
    cursor: pointer;
    font-size: 1rem;
    border-radius: 0.3rem;
}}

button:hover {{
    background: #555;
}}

a {{
    color: #66ccff;
    text-decoration: none;
}}

a:hover {{
    text-decoration: underline;
}}

pre.content {{
    white-space: pre-wrap;
    line-height: 1.6;
    font-size: 1rem;
}}

@media screen and (max-width: 600px) {{
    body {{
        font-size: 1.1rem;
        padding: 1rem;
    }}

    button {{
        font-size: 1rem;
        padding: 0.6rem 1rem;
    }}

    h2 {{
        font-size: 1.4rem;
    }}

    pre.content {{
        font-size: 1.05rem;
    }}
}}
</style>
<script>
let current = 0;

function showMenu() {{
    document.getElementById('menu').style.display = 'block';
    document.querySelectorAll('.chapter').forEach(ch => ch.style.display = 'none');
    current = 0;
    location.hash = "#0";
    window.scrollTo(0, 0);
}}

function showChapter(index) {{
    const chapters = document.querySelectorAll('.chapter');
    if (index < 1 || index > chapters.length) return;
    document.getElementById('menu').style.display = 'none';
    chapters.forEach(ch => ch.style.display = 'none');
    chapters[index - 1].style.display = 'block';
    current = index;
    location.hash = "#" + index;
    window.scrollTo(0, 0);
}}

function toChapter(index) {{
    if (index === 0) {{
        showMenu();
    }} else {{
        showChapter(index);
    }}
}}

function nextChapter() {{ showChapter(current + 1); }}
function prevChapter() {{ showChapter(current - 1); }}

function changeFontSize(delta) {{
    const contents = document.querySelectorAll('pre.content');
    contents.forEach(el => {{
        let style = window.getComputedStyle(el);
        let size = parseFloat(style.fontSize);
        el.style.fontSize = (size + delta) + 'px';
    }});
}}

function loadFromHash() {{
    const hash = location.hash.replace("#", "");
    const index = parseInt(hash);
    if (!hash || hash === "0" || isNaN(index)) {{
        showMenu();
    }} else {{
        showChapter(index);
    }}
}}

window.addEventListener("hashchange", loadFromHash);
window.addEventListener("DOMContentLoaded", loadFromHash);
</script>
</head>
<body>
<div id="menu">
<h2>📚 目錄</h2>
<ul>
""")

        for i, (title, _) in enumerate(chapters, start=1):
            f.write(f'<li><a href="#{i}">{title}</a></li>\n')

        f.write("""</ul>
</div>
""")

        for idx, (title, url) in enumerate(chapters, start=1):
            print(f"[{idx}/{len(chapters)}] 抓取中：{title}")
            try:
                chapter_title, chapter_content = fetch_chapter_content(url)
                f.write(f'<div id="chapter_{idx}" class="chapter">\n')
                f.write(f"<h2>{chapter_title}</h2>\n")

                nav_buttons = f"""<nav>
<button onclick="prevChapter()" {'disabled' if idx==1 else ''}>⬅️ 上一章</button>
<button onclick="toChapter(0)">📚 目錄</button>
<button onclick="nextChapter()" {'disabled' if idx==len(chapters) else ''}>下一章 ➡️</button>
<button onclick="changeFontSize(2)">A+</button>
<button onclick="changeFontSize(-2)">A-</button>
</nav>
"""

                f.write(nav_buttons)
                f.write(f'<pre class="content">{chapter_content}</pre>\n')
                f.write(nav_buttons)

                f.write("</div>\n")
                time.sleep(0.1)
            except Exception as e:
                print(f"⚠️ 抓取失敗：{title} - {e}")
                continue

        f.write("</body>\n</html>")
    print(f"\n✅ 完成！HTML 檔已產出 → {output_file}")


if __name__ == "__main__":
    base_output_dir = "./Downloads/Novel/Nameko117.github.io/src/"
    os.makedirs(base_output_dir, exist_ok=True)

    for toc_url, book_title, author in novels:
        filename = f"{author}《{book_title}》.html"
        output_filepath = os.path.join(base_output_dir, filename)
        if os.path.exists(output_filepath):
            print(f"跳過，檔案已存在：{filename}")
            continue

        print(f"\n📖 擷取章節列表中：{book_title} by {author} ...")
        chapters = get_chapter_links(toc_url)
        print(f"✅ 共取得 {len(chapters)} 章節。\n")

        save_book_with_hash_navigation(chapters, output_filepath, book_title)
