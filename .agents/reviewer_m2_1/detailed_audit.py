import os
import glob
import re
from html.parser import HTMLParser

showcase_dir = '/root/ai-workspace/test/dashboard/showcase'

class LinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = [] # list of (tag, attr_name, attr_val, line_no)

    def handle_starttag(self, tag, attrs):
        line = self.getpos()[0]
        for name, value in attrs:
            if name in ('href', 'src') and value:
                self.links.append((tag, name, value, line))

# Find all HTML files
html_files = []
for root, dirs, files in os.walk(showcase_dir, followlinks=True):
    if '/.agents' in root or '/.git' in root or '/.gemini' in root:
        continue
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

html_files = sorted(list(set(html_files)))

print(f"Found {len(html_files)} HTML files:")
for f in html_files:
    print("  -", os.path.relpath(f, showcase_dir))

report = []
total_links = 0
broken_links = 0

for filepath in html_files:
    rel_file = os.path.relpath(filepath, showcase_dir)
    file_dir = os.path.dirname(filepath)

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    parser = LinkExtractor()
    parser.feed(content)

    # Also search for JS pageUrl or string paths if any
    js_matches = re.findall(r'pageUrl:\s*[\"\']([^\"\']+)[\"\']', content)
    for jm in js_matches:
        parser.links.append(('script-js', 'pageUrl', jm, 0))

    # Also check inline styles or other urls if any
    style_urls = re.findall(r'url\([\'\"]?([^\'\"]+)[\'\"]?\)', content)
    for su in style_urls:
        if not su.startswith('data:'):
            parser.links.append(('style', 'url', su, 0))

    file_report = {'file': rel_file, 'links': []}

    for tag, attr, val, line in parser.links:
        val_clean = val.strip()
        if val_clean.startswith(('http://', 'https://', 'mailto:', 'javascript:', '#', 'data:', '${')) or not val_clean:
            continue
        
        target = val_clean.split('#')[0].split('?')[0]
        if not target:
            continue

        total_links += 1
        target_abs = os.path.normpath(os.path.join(file_dir, target))
        exists = os.path.exists(target_abs)
        if not exists:
            broken_links += 1
        
        file_report['links'].append({
            'tag': tag,
            'attr': attr,
            'val': val_clean,
            'target_abs': target_abs,
            'exists': exists,
            'line': line
        })
    
    report.append(file_report)

print(f"\n--- AUDIT SUMMARY ---")
print(f"Total HTML files: {len(html_files)}")
print(f"Total relative links checked: {total_links}")
print(f"Broken links: {broken_links}")

print("\n--- LINK BREAKDOWN BY FILE ---")
for r in report:
    print(f"\nFile: {r['file']}")
    for l in r['links']:
        status = "OK" if l['exists'] else "BROKEN"
        print(f"  [{status}] <{l['tag']} {l['attr']}=\"{l['val']}\"> -> {os.path.relpath(l['target_abs'], showcase_dir)}")
