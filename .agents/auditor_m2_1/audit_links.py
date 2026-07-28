import os
import re
import glob

showcase_dir = '/root/ai-workspace/test/dashboard/showcase'
html_files = sorted(glob.glob(f'{showcase_dir}/**/*.html', recursive=True))

html_files = [f for f in html_files if '/.agents/' not in f and '/.git/' not in f and '/.gemini/' not in f]

print(f"Found {len(html_files)} HTML files:")
for f in html_files:
    print(f"  - {os.path.relpath(f, showcase_dir)}")

href_src_pattern = re.compile(r'(?:href|src)=[\"\']([^\"\']+)[\"\']')
js_pageurl_pattern = re.compile(r'pageUrl:\s*[\"\']([^\"\']+)[\"\']')

all_links = []
broken_links = []

for fpath in html_files:
    rel_path = os.path.relpath(fpath, showcase_dir)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    matches = href_src_pattern.findall(content) + js_pageurl_pattern.findall(content)
    for link in matches:
        link_str = link.strip()
        if link_str.startswith(('http://', 'https://', 'mailto:', 'javascript:', '#', '${')) or not link_str:
            continue
        clean_link = link_str.split('#')[0].split('?')[0]
        if not clean_link:
            continue
        
        target_abs = os.path.normpath(os.path.join(os.path.dirname(fpath), clean_link))
        exists = os.path.exists(target_abs)
        all_links.append((rel_path, link_str, target_abs, exists))
        if not exists:
            broken_links.append((rel_path, link_str, target_abs))

print(f"\nTotal internal relative links checked: {len(all_links)}")
print(f"Broken links count: {len(broken_links)}")
if broken_links:
    for src, link, target in broken_links:
        print(f"BROKEN: in {src} -> link: {link} (target: {target})")
else:
    print("All internal relative links resolve successfully to existing files on disk!")
