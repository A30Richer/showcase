import os
import re
import sys
from html.parser import HTMLParser

SHOWCASE_DIR = "/root/ai-workspace/test/dashboard/showcase"

class HTMLSyntaxAndLinkParser(HTMLParser):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.tags = []
        self.links = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        attr_dict = dict(attrs)
        for attr in ['href', 'src', 'action', 'data-src', 'data-href']:
            if attr in attr_dict:
                val = attr_dict[attr]
                if val:
                    self.links.append((tag, attr, val, self.getpos()))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

def get_all_html_files(base_dir):
    html_files = []
    for root, dirs, files in os.walk(base_dir):
        # Ignore .agents, .git, etc.
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for f in files:
            if f.endswith('.html'):
                html_files.append(os.path.join(root, f))
    return sorted(html_files)

def audit():
    html_files = get_all_html_files(SHOWCASE_DIR)
    print(f"Found {len(html_files)} HTML files in {SHOWCASE_DIR}:")
    for f in html_files:
        rel = os.path.relpath(f, SHOWCASE_DIR)
        print(f"  - {rel}")

    total_links_checked = 0
    broken_links = []
    syntax_errors = []
    js_links_checked = 0

    href_src_regex = re.compile(r'(?:href|src)=["\']([^"\']+)["\']', re.IGNORECASE)
    js_pageurl_regex = re.compile(r'pageUrl:\s*["\']([^"\']+)["\']', re.IGNORECASE)

    for file_path in html_files:
        rel_file = os.path.relpath(file_path, SHOWCASE_DIR)
        file_dir = os.path.dirname(file_path)

        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()

        # 1. HTML Syntax check
        parser = HTMLSyntaxAndLinkParser(rel_file)
        try:
            parser.feed(content)
        except Exception as e:
            syntax_errors.append((rel_file, f"HTML parse error: {str(e)}"))

        # Check for obvious unclosed or corrupted HTML tags from raw regex/lines
        # e.g. href="... without closing quote, broken <a href="... >
        unclosed_quotes = re.findall(r'<[^>]*href=["\'][^"\'\s>]*$', content, re.MULTILINE)
        if unclosed_quotes:
            syntax_errors.append((rel_file, f"Unclosed quotes in tags: {unclosed_quotes}"))

        # 2. Check HTML attributes links
        for tag, attr, val, pos in parser.links:
            val_clean = val.strip()
            # Skip external, anchor, mailto, javascript, dynamic JS template strings
            if val_clean.startswith(('http://', 'https://', 'mailto:', 'javascript:', '#', '${', 'data:')) or not val_clean:
                continue

            target_clean = val_clean.split('#')[0].split('?')[0]
            if not target_clean:
                continue

            total_links_checked += 1
            target_abs = os.path.normpath(os.path.join(file_dir, target_clean))

            if not os.path.exists(target_abs):
                broken_links.append((rel_file, tag, attr, val_clean, target_abs, pos))

        # 3. Check JS pageUrl links (e.g. in website_design.html)
        js_matches = js_pageurl_regex.findall(content)
        for val in js_matches:
            val_clean = val.strip()
            if val_clean.startswith(('http://', 'https://', '#', '${')) or not val_clean:
                continue
            target_clean = val_clean.split('#')[0].split('?')[0]
            if not target_clean:
                continue

            js_links_checked += 1
            target_abs = os.path.normpath(os.path.join(file_dir, target_clean))
            if not os.path.exists(target_abs):
                broken_links.append((rel_file, 'JS:pageUrl', 'value', val_clean, target_abs, (0, 0)))

    print("\n" + "="*60)
    print("AUDIT RESULTS SUMMARY")
    print("="*60)
    print(f"Total HTML files scanned: {len(html_files)}")
    print(f"Total HTML tag links checked: {total_links_checked}")
    print(f"Total JS literal links checked: {js_links_checked}")
    print(f"Total relative links checked: {total_links_checked + js_links_checked}")
    print(f"Syntax errors found: {len(syntax_errors)}")
    print(f"Broken relative links found: {len(broken_links)}")

    if syntax_errors:
        print("\n[!] SYNTAX ERRORS DETECTED:")
        for err in syntax_errors:
            print(f"  File: {err[0]} -> {err[1]}")

    if broken_links:
        print("\n[!] BROKEN RELATIVE LINKS DETECTED:")
        for b in broken_links:
            print(f"  File: {b[0]} (line {b[5][0]}) [{b[1]} {b[2]}]: \"{b[3]}\" -> Resolved: \"{b[4]}\" (NOT FOUND)")

    if len(syntax_errors) == 0 and len(broken_links) == 0:
        print("\n[✓] ALL CHECKS PASSED PERFECTLY!")

if __name__ == "__main__":
    audit()
