import os
import re
import sys
from bs4 import BeautifulSoup
from urllib.parse import unquote, urlparse

SHOWCASE_DIR = "/root/ai-workspace/test/dashboard/showcase"

def is_external_or_special(url):
    if not url or url.strip() == "" or url.startswith("#"):
        return True
    parsed = urlparse(url)
    if parsed.scheme in ["http", "https", "mailto", "tel", "javascript", "data"]:
        return True
    if url.startswith("//"):
        return True
    return False

def clean_target_path(url):
    # Remove query params and fragment
    url_without_frag = url.split('#')[0].split('?')[0]
    # URL decode
    return unquote(url_without_frag)

def resolve_target(html_file_path, target_url):
    cleaned = clean_target_path(target_url)
    if not cleaned:
        return None
    
    if cleaned.startswith("/"):
        # Absolute path relative to showcase root
        resolved = os.path.normpath(os.path.join(SHOWCASE_DIR, cleaned.lstrip("/")))
    else:
        # Relative path relative to HTML file location
        html_dir = os.path.dirname(html_file_path)
        resolved = os.path.normpath(os.path.join(html_dir, cleaned))
    return resolved

def audit_showcase():
    html_files = []
    for root, dirs, files in os.walk(SHOWCASE_DIR):
        # Exclude .agents directory
        parts = root.split(os.sep)
        if ".agents" in parts:
            continue
        for f in files:
            if f.endswith(".html"):
                html_files.append(os.path.join(root, f))

    html_files.sort()
    print(f"Found {len(html_files)} HTML files to audit in {SHOWCASE_DIR}:")
    for f in html_files:
        print(f"  - {os.path.relpath(f, SHOWCASE_DIR)}")
    print("=" * 60)

    total_links_found = 0
    total_relative_links = 0
    missing_links = []
    checked_links = []

    # Regex for finding string literals in JS code: e.g. 'path/file.ext' or "./path" or "../path"
    js_path_regex = re.compile(r"['\"]((?:\.\.?/|/|[a-zA-Z0-9_\-]+/)[^'\"\s>]+\.(?:html|css|js|png|jpg|jpeg|svg|gif|webp|json))(?:[?#][^'\"]*)?['\"]")

    for html_path in html_files:
        rel_html_path = os.path.relpath(html_path, SHOWCASE_DIR)
        with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')

        # 1. Inspect HTML attributes across all tags
        for tag in soup.find_all(True):
            for attr, val in tag.attrs.items():
                if attr.lower() in ['href', 'src', 'action', 'poster', 'data-src', 'data-href']:
                    vals = val if isinstance(val, list) else [val]
                    for raw_url in vals:
                        total_links_found += 1
                        if is_external_or_special(raw_url):
                            continue
                        
                        total_relative_links += 1
                        target_disk_path = resolve_target(html_path, raw_url)
                        exists = os.path.exists(target_disk_path) if target_disk_path else False
                        
                        item = {
                            'source_file': rel_html_path,
                            'tag': tag.name,
                            'attr': attr,
                            'raw_url': raw_url,
                            'target_disk_path': target_disk_path,
                            'exists': exists,
                            'context': 'HTML Tag Attribute'
                        }
                        checked_links.append(item)
                        if not exists:
                            missing_links.append(item)

        # 2. Inspect JS string literals inside <script> tags
        for script_tag in soup.find_all('script'):
            if script_tag.string:
                js_code = script_tag.string
                matches = js_path_regex.findall(js_code)
                for raw_url in matches:
                    total_links_found += 1
                    if is_external_or_special(raw_url):
                        continue
                    
                    total_relative_links += 1
                    target_disk_path = resolve_target(html_path, raw_url)
                    exists = os.path.exists(target_disk_path) if target_disk_path else False

                    item = {
                        'source_file': rel_html_path,
                        'tag': 'script',
                        'attr': 'js_literal',
                        'raw_url': raw_url,
                        'target_disk_path': target_disk_path,
                        'exists': exists,
                        'context': 'JS String Literal in <script>'
                    }
                    checked_links.append(item)
                    if not exists:
                        missing_links.append(item)

    print(f"\nAudit Summary:")
    print(f"Total HTML files audited: {len(html_files)}")
    print(f"Total link occurrences scanned: {total_links_found}")
    print(f"Total relative link targets verified: {total_relative_links}")
    print(f"Broken / missing relative link targets: {len(missing_links)}")
    print("=" * 60)

    if missing_links:
        print("\nBROKEN LINKS FOUND:")
        for idx, m in enumerate(missing_links, 1):
            print(f"{idx}. File: {m['source_file']}")
            print(f"   Context: {m['context']} (<{m['tag']} {m['attr']}>)")
            print(f"   Raw URL: {m['raw_url']}")
            print(f"   Resolved Target: {m['target_disk_path']}")
            print("-" * 50)
        return False
    else:
        print("\nALL RELATIVE LINKS ARE VALID AND EXIST ON DISK!")
        return True

if __name__ == '__main__':
    success = audit_showcase()
    if not success:
        sys.exit(1)
