import os

def generate_bookshelf_html(books_dir, output_path):
    files = [f for f in os.listdir(books_dir) if f.endswith('html')]
    files.sort()

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8" />
<title>我的書架</title>
<style>
body {
    background: #121212;
    color: #eee;
    font-family: sans-serif;
    padding: 20px;
}
h1 {
    text-align: center;
    margin-bottom: 10px;
}
#search {
    display: block;
    margin: 0 auto 20px auto;
    padding: 10px;
    width: 90%;
    max-width: 500px;
    font-size: 16px;
    border: none;
    border-radius: 5px;
}
ul {
    list-style: none;
    padding: 0;
    max-width: 600px;
    margin: 0 auto;
}
li {
    margin: 10px 0;
    font-size: 18px;
}
a {
    color: #66ccff;
    text-decoration: none;
}
a:hover {
    text-decoration: underline;
}
</style>
</head>
<body>
<h1>📚 我的書架</h1>
<input type="text" id="search" placeholder="🔍 搜尋書名..." onkeyup="filterBooks()" />
<ul id="book-list">
""")

        for file in files:
            book_name = os.path.splitext(file)[0]
            link = f"src/{file}"
            f.write(f'<li><a href="{link}" target="_blank">{book_name}</a></li>\n')

        f.write("""</ul>
<script>
function filterBooks() {
    const input = document.getElementById("search");
    const filter = input.value.toLowerCase();
    const ul = document.getElementById("book-list");
    const li = ul.getElementsByTagName("li");

    for (let i = 0; i < li.length; i++) {
        const a = li[i].getElementsByTagName("a")[0];
        const txtValue = a.textContent || a.innerText;
        if (txtValue.toLowerCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}
</script>
</body>
</html>
""")

if __name__ == "__main__":
    src_dir = "./Downloads/Novel/Nameko117.github.io/src"
    index_html = "./Downloads/Novel/Nameko117.github.io/index.html"
    generate_bookshelf_html(src_dir, index_html)
    print(f"✅ 書架首頁已產生：{index_html}")
