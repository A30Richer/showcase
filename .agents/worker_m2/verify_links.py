import os
import re
import glob

showcase_dir = '/root/ai-workspace/test/dashboard/showcase'
html_files = glob.glob(f'{showcase_dir}/**/*.html', recursive=True)

href_src_pattern = re.compile(r'(?:href|src)=[\"\']([^\"\']+)[\"\']')
js_pageurl_pattern = re.compile(r'pageUrl:\s*[\"\']([^\"\']+)[\"\']')

total_checked = 0
broken = []
passed = []

for html_file in sorted(html_files):
    if '/.agents/' in html_file or '/.git/' in html_file or '/.gemini/' in html_file:
        continue
    rel_html = os.path.relpath(html_file, showcase_dir)
    dir_of_file = os.path.dirname(html_file)

    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    links = href_src_pattern.findall(content) + js_pageurl_pattern.findall(content)

    for link in links:
        link_str = link.strip()
        # Ignore external links, anchor links, dynamic JS template strings
        if link_str.startswith(('http://', 'https://', 'mailto:', 'javascript:', '#', '${')) or not link_str:
            continue
        
        # Strip anchor or query params if any
        target_path_clean = link_str.split('#')[0].split('?')[0]
        if not target_path_clean:
            continue

        total_checked += 1
        target_abs = os.path.normpath(os.path.join(dir_of_file, target_path_clean))

        if os.path.exists(target_abs):
            passed.append((rel_html, link_str, target_abs))
        else:
            broken.append((rel_html, link_str, target_abs))

print(f"Total HTML files scanned: {len([f for f in html_files if not ('/.agents/' in f or '/.git/' in f or '/.gemini/' in f)])}")
print(f"Total relative links checked: {total_checked}")
print(f"Passed: {len(passed)}")
print(f"Broken: {len(broken)}")

if broken:
    print("\nBROKEN LINKS DETECTED:")
    for src_f, l_str, t_abs in broken:
        print(f"  In {src_f}: \"{l_str}\" -> Resolved to \"{t_abs}\" (NOT FOUND)")
else:
    print("\nSUCCESS: 100% of relative links resolve to existing files on disk!")
