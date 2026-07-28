import os
import re
from html.parser import HTMLParser

SHOWCASE_DIR = "/root/ai-workspace/test/dashboard/showcase"

def get_all_html_files():
    files_list = []
    for root, dirs, files in os.walk(SHOWCASE_DIR):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for f in files:
            if f.endswith('.html'):
                files_list.append(os.path.join(root, f))
    return sorted(files_list)

def deep_inspect():
    html_files = get_all_html_files()
    href_src_pattern = re.compile(r'(?:href|src)=["\']([^"\']+)["\']', re.IGNORECASE)
    js_pageurl_pattern = re.compile(r'pageUrl:\s*["\']([^"\']+)["\']', re.IGNORECASE)

    total_files = len(html_files)
    total_links = 0
    file_summary = {}

    for filepath in html_files:
        rel_path = os.path.relpath(filepath, SHOWCASE_DIR)
        dir_path = os.path.dirname(filepath)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        links = href_src_pattern.findall(content) + js_pageurl_pattern.findall(content)
        file_links = []

        for l in links:
            l_str = l.strip()
            if l_str.startswith(('http://', 'https://', 'mailto:', 'javascript:', '#', '${', 'data:')) or not l_str:
                continue
            
            clean_path = l_str.split('#')[0].split('?')[0]
            if not clean_path:
                continue

            target_abs = os.path.normpath(os.path.join(dir_path, clean_path))
            exists = os.path.exists(target_abs)
            file_links.append({
                'link': l_str,
                'target_abs': target_abs,
                'rel_target': os.path.relpath(target_abs, SHOWCASE_DIR),
                'exists': exists
            })
            total_links += 1

        file_summary[rel_path] = file_links

    print(f"Total HTML files: {total_files}")
    print(f"Total relative links: {total_links}\n")

    broken_count = 0
    for rel_path, links in file_summary.items():
        print(f"📄 {rel_path} ({len(links)} links):")
        for item in links:
            status = "✓ OK" if item['exists'] else "❌ BROKEN"
            if not item['exists']:
                broken_count += 1
            print(f"   [{status}] '{item['link']}' -> {item['rel_target']}")
        print()

    print("="*60)
    print(f"FINAL AUDIT RESULT: {total_links} links checked, {broken_count} broken.")
    print("="*60)

if __name__ == '__main__':
    deep_inspect()
