import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote

SHOWCASE_DIR = "/root/ai-workspace/test/dashboard/showcase"

def check_breakdown():
    html_files = []
    for root, dirs, files in os.walk(SHOWCASE_DIR):
        if ".agents" in root.split(os.sep):
            continue
        for f in files:
            if f.endswith(".html"):
                html_files.append(os.path.join(root, f))
    html_files.sort()

    categories = {}
    for fpath in html_files:
        rel = os.path.relpath(fpath, SHOWCASE_DIR)
        cat = rel.split(os.sep)[0] if os.sep in rel else 'root'
        categories.setdefault(cat, []).append(fpath)

    for cat, files in sorted(categories.items()):
        print(f"=== Category: {cat} ({len(files)} files) ===")
        for fpath in files:
            rel = os.path.relpath(fpath, SHOWCASE_DIR)
            with open(fpath, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
            links = []
            for tag in soup.find_all(True):
                for attr, val in tag.attrs.items():
                    if attr.lower() in ['href', 'src']:
                        vals = val if isinstance(val, list) else [val]
                        for v in vals:
                            if v and not v.startswith('#') and not urlparse(v).scheme:
                                links.append(v)
            print(f"  {rel}: {len(links)} relative links -> {links[:5]}")

if __name__ == '__main__':
    check_breakdown()
