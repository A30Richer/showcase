import os
import re
from html.parser import HTMLParser

SHOWCASE_DIR = "/root/ai-workspace/test/dashboard/showcase"

class LinkContractAuditor(HTMLParser):
    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath
        self.rel_path = os.path.relpath(filepath, SHOWCASE_DIR)
        self.category = self.get_category(self.rel_path)
        self.links = []
        self.raw_content = ""

    def get_category(self, rel_path):
        if rel_path == 'index.html':
            return 'root'
        elif rel_path.startswith('themes/'):
            return 'themes'
        elif rel_path.startswith('apps/'):
            return 'apps'
        elif rel_path.startswith('pages/'):
            return 'pages'
        elif rel_path.startswith('reports/'):
            return 'reports'
        elif rel_path.startswith('website-design/'):
            return 'website-design'
        return 'other'

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        for attr_name in ['href', 'src']:
            if attr_name in attr_dict and attr_dict[attr_name]:
                val = attr_dict[attr_name].strip()
                if not val.startswith(('http://', 'https://', 'mailto:', 'javascript:', '#', '${', 'data:')):
                    self.links.append((tag, attr_name, val, self.getpos()))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

def check_all_contracts():
    all_files = []
    for root, dirs, files in os.walk(SHOWCASE_DIR):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for f in files:
            if f.endswith('.html'):
                all_files.append(os.path.join(root, f))
    
    all_files.sort()

    report = []
    unconverted_links = []
    contract_violations = []

    href_src_regex = re.compile(r'(?:href|src)=["\']([^"\']+)["\']', re.IGNORECASE)
    js_pageurl_regex = re.compile(r'pageUrl:\s*["\']([^"\']+)["\']', re.IGNORECASE)

    for filepath in all_files:
        rel_path = os.path.relpath(filepath, SHOWCASE_DIR)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        parser = LinkContractAuditor(filepath)
        parser.feed(content)

        # Also find JS string literals
        js_matches = js_pageurl_regex.findall(content)
        for jm in js_matches:
            val = jm.strip()
            if not val.startswith(('http://', 'https://', '#', '${')):
                parser.links.append(('js:pageUrl', 'value', val, (0, 0)))

        category = parser.category

        for tag, attr, link, pos in parser.links:
            clean_link = link.split('#')[0].split('?')[0]
            if not clean_link:
                continue

            target_abs = os.path.normpath(os.path.join(os.path.dirname(filepath), clean_link))
            exists = os.path.exists(target_abs)

            # Contract checks based on category:
            # 1. root index.html: should point to themes/, apps/, pages/, reports/
            if category == 'root':
                if clean_link in ['index.html', './index.html']:
                    pass # root index linking to self or anchor
                elif not (clean_link.startswith('themes/') or clean_link.startswith('apps/') or clean_link.startswith('pages/') or clean_link.startswith('reports/') or clean_link.startswith('assets/')):
                    contract_violations.append((rel_path, tag, attr, link, "Root index.html link does not start with folder prefix"))

            # 2. themes/*.html: should point to ../pages/website_design.html or ../index.html
            elif category == 'themes':
                if not clean_link.startswith('../'):
                    contract_violations.append((rel_path, tag, attr, link, "Themes HTML link is not relative to parent folder (missing ../)"))

            # 3. apps/*.html: should point to ../index.html or ../pages/
            elif category == 'apps':
                if not clean_link.startswith('../') and not clean_link.startswith('http'):
                    contract_violations.append((rel_path, tag, attr, link, "Apps HTML link is not relative to parent folder (missing ../)"))

            # 4. pages/*.html: should point to ../index.html, ../themes/, ../reports/, ../assets/
            elif category == 'pages':
                if not clean_link.startswith('../'):
                    contract_violations.append((rel_path, tag, attr, link, "Pages HTML link is not relative to parent folder (missing ../)"))

            # 5. reports/*.html: should point to ../pages/main.html, ../assets/, or sibling report
            elif category == 'reports':
                if clean_link.endswith('main.html') and not clean_link.startswith('../pages/'):
                    contract_violations.append((rel_path, tag, attr, link, "Report link to main.html does not point to ../pages/main.html"))

            if not exists:
                unconverted_links.append((rel_path, tag, attr, link, target_abs))

    print(f"Scanned {len(all_files)} files.")
    print(f"Contract violations: {len(contract_violations)}")
    if contract_violations:
        print("CONTRACT VIOLATIONS DETECTED:")
        for cv in contract_violations:
            print(" ", cv)

    print(f"Unresolved targets (404 broken): {len(unconverted_links)}")
    if unconverted_links:
        print("UNRESOLVED LINKS DETECTED:")
        for ul in unconverted_links:
            print(" ", ul)

if __name__ == '__main__':
    check_all_contracts()
