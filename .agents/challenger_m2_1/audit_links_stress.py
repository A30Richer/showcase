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
    url_without_frag = url.split('#')[0].split('?')[0]
    return unquote(url_without_frag)

def resolve_target(html_file_path, target_url):
    cleaned = clean_target_path(target_url)
    if not cleaned:
        return None
    
    if cleaned.startswith("/"):
        resolved = os.path.normpath(os.path.join(SHOWCASE_DIR, cleaned.lstrip("/")))
    else:
        html_dir = os.path.dirname(html_file_path)
        resolved = os.path.normpath(os.path.join(html_dir, cleaned))
    return resolved

def audit_stress():
    html_files = []
    for root, dirs, files in os.walk(SHOWCASE_DIR):
        parts = root.split(os.sep)
        if ".agents" in parts:
            continue
        for f in files:
            if f.endswith(".html"):
                html_files.append(os.path.join(root, f))

    html_files.sort()
    
    missing_links = []
    all_relative_links = []

    # Regexes
    url_css_regex = re.compile(r"url\(\s*['\"]?([^'\"\)\s]+)['\"]?\s*\)", re.IGNORECASE)
    # Match any single/double quoted string that looks like a relative file path or filename ending with common extensions or path navigation
    any_string_path_regex = re.compile(r"['\"]((?:\.\.?/|[a-zA-Z0-9_\-]+/)*[a-zA-Z0-9_\-]+\.(?:html|css|js|png|jpg|jpeg|svg|gif|webp|json|ico))(?:[?#][^'\"]*)?['\"]")
    # Match JS location assignments like location.href = "...", window.open("...")
    js_location_regex = re.compile(r"(?:location\.href|location|window\.open)\s*=\s*['\"]([^'\"]+)['\"]|(?:location\.href|location|window\.open)\(\s*['\"]([^'\"]+)['\"]", re.IGNORECASE)

    for html_path in html_files:
        rel_html_path = os.path.relpath(html_path, SHOWCASE_DIR)
        with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')

        # 1. Attributes on all elements
        for tag in soup.find_all(True):
            for attr, val in tag.attrs.items():
                attr_lower = attr.lower()
                vals = val if isinstance(val, list) else [val]
                for raw_val in vals:
                    # Check standard URL attributes
                    if attr_lower in ['href', 'src', 'action', 'poster', 'data-src', 'data-href', 'data-url']:
                        if not is_external_or_special(raw_val):
                            target_disk_path = resolve_target(html_path, raw_val)
                            exists = os.path.exists(target_disk_path) if target_disk_path else False
                            item = {
                                'source_file': rel_html_path,
                                'tag': tag.name,
                                'attr': attr,
                                'raw_url': raw_val,
                                'target_disk_path': target_disk_path,
                                'exists': exists,
                                'context': f"HTML attribute ({attr})"
                            }
                            all_relative_links.append(item)
                            if not exists:
                                missing_links.append(item)

                    # Check inline style attributes for url(...)
                    if attr_lower == 'style':
                        css_matches = url_css_regex.findall(raw_val)
                        for raw_url in css_matches:
                            if not is_external_or_special(raw_url):
                                target_disk_path = resolve_target(html_path, raw_url)
                                exists = os.path.exists(target_disk_path) if target_disk_path else False
                                item = {
                                    'source_file': rel_html_path,
                                    'tag': tag.name,
                                    'attr': 'style url()',
                                    'raw_url': raw_url,
                                    'target_disk_path': target_disk_path,
                                    'exists': exists,
                                    'context': "Inline style url()"
                                }
                                all_relative_links.append(item)
                                if not exists:
                                    missing_links.append(item)

                    # Check event attributes like onclick, onload, onchange
                    if attr_lower.startswith('on'):
                        paths_in_event = any_string_path_regex.findall(raw_val)
                        for raw_url in paths_in_event:
                            if not is_external_or_special(raw_url):
                                target_disk_path = resolve_target(html_path, raw_url)
                                exists = os.path.exists(target_disk_path) if target_disk_path else False
                                item = {
                                    'source_file': rel_html_path,
                                    'tag': tag.name,
                                    'attr': attr,
                                    'raw_url': raw_url,
                                    'target_disk_path': target_disk_path,
                                    'exists': exists,
                                    'context': f"Event handler attribute ({attr})"
                                }
                                all_relative_links.append(item)
                                if not exists:
                                    missing_links.append(item)

        # 2. Style tags for url(...)
        for style_tag in soup.find_all('style'):
            if style_tag.string:
                css_matches = url_css_regex.findall(style_tag.string)
                for raw_url in css_matches:
                    if not is_external_or_special(raw_url):
                        target_disk_path = resolve_target(html_path, raw_url)
                        exists = os.path.exists(target_disk_path) if target_disk_path else False
                        item = {
                            'source_file': rel_html_path,
                            'tag': 'style',
                            'attr': 'css url()',
                            'raw_url': raw_url,
                            'target_disk_path': target_disk_path,
                            'exists': exists,
                            'context': "Style tag url()"
                        }
                        all_relative_links.append(item)
                        if not exists:
                            missing_links.append(item)

        # 3. Script tags for paths and location assignments
        for script_tag in soup.find_all('script'):
            if script_tag.string:
                js_code = script_tag.string
                # String literals with extensions
                matches = any_string_path_regex.findall(js_code)
                for raw_url in matches:
                    if not is_external_or_special(raw_url):
                        target_disk_path = resolve_target(html_path, raw_url)
                        exists = os.path.exists(target_disk_path) if target_disk_path else False
                        item = {
                            'source_file': rel_html_path,
                            'tag': 'script',
                            'attr': 'js_string_literal',
                            'raw_url': raw_url,
                            'target_disk_path': target_disk_path,
                            'exists': exists,
                            'context': "JS string literal"
                        }
                        all_relative_links.append(item)
                        if not exists:
                            missing_links.append(item)

                # Location assignments
                loc_matches = js_location_regex.findall(js_code)
                for match in loc_matches:
                    raw_url = match[0] or match[1]
                    if raw_url and not is_external_or_special(raw_url):
                        target_disk_path = resolve_target(html_path, raw_url)
                        exists = os.path.exists(target_disk_path) if target_disk_path else False
                        item = {
                            'source_file': rel_html_path,
                            'tag': 'script',
                            'attr': 'js_location',
                            'raw_url': raw_url,
                            'target_disk_path': target_disk_path,
                            'exists': exists,
                            'context': "JS location assignment"
                        }
                        all_relative_links.append(item)
                        if not exists:
                            missing_links.append(item)

    print("=" * 60)
    print("STRESS LINK AUDIT RESULTS:")
    print(f"Total HTML files audited: {len(html_files)}")
    print(f"Total relative links/paths scanned & verified: {len(all_relative_links)}")
    print(f"Missing / Broken targets found: {len(missing_links)}")
    print("=" * 60)

    if missing_links:
        print("\nBROKEN LINKS DETAILS:")
        for idx, m in enumerate(missing_links, 1):
            print(f"{idx}. Source File: {m['source_file']}")
            print(f"   Context: {m['context']}")
            print(f"   Raw URL: {m['raw_url']}")
            print(f"   Resolved Target: {m['target_disk_path']}")
            print("-" * 50)
        return False
    else:
        print("\nSTRESS TEST PASSED: ALL RELATIVE LINKS AND ASSETS RESOLVE TO EXISTING DISK FILES!")
        return True

if __name__ == '__main__':
    res = audit_stress()
    if not res:
        sys.exit(1)
