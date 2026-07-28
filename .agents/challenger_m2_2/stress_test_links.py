#!/usr/bin/env python3
import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

BASE_DIR = Path("/root/ai-workspace/test/dashboard/showcase").resolve()

class LinkExtractor(HTMLParser):
    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath
        self.links = [] # list of (tag, attr, val, line_no)
        
    def handle_starttag(self, tag, attrs):
        line_no = self.getpos()[0]
        for attr, val in attrs:
            if not val:
                continue
            if attr in ('href', 'src', 'action', 'data'):
                self.links.append((tag, attr, val, line_no))

def is_external_or_special(url):
    url_lower = url.strip().lower()
    if url_lower.startswith(('http://', 'https://', '//', 'data:', 'javascript:', 'mailto:', 'tel:')):
        return True
    if url_lower.startswith('#'):
        return True
    if '${' in url or '{{' in url: # JS template literal placeholders
        return True
    return False

def clean_path(url):
    # strip query string and hash anchor
    clean = url.split('#')[0].split('?')[0].strip()
    return clean

def extract_js_and_css_urls(content):
    # Regex for url('...') or url("...") or url(...)
    urls = []
    for match in re.finditer(r'url\s*\(\s*[\'"]?([^\'")]+)[\'"]?\s*\)', content):
        urls.append(('css-url', 'url', match.group(1)))
    # Regex for JS string references to relative files ending in .html, .png, .jpg, .svg, .css, .js
    # e.g. pageUrl: '../themes/style_01_glassmorphic.html'
    for match in re.finditer(r'[\'\"](\.\.?[^\'\"]+\.(?:html|png|jpg|jpeg|svg|css|js))[\'\"]', content):
        urls.append(('js-string', 'path', match.group(1)))
    return urls

def test_all_links():
    print(f"=== Starting Empirical Link Audit in {BASE_DIR} ===")
    
    html_files = list(BASE_DIR.glob("**/*.html"))
    # Exclude files inside .agents/ if any
    html_files = [f for f in html_files if ".agents" not in f.parts]
    
    print(f"Found {len(html_files)} HTML files to inspect.")
    
    total_links_found = 0
    checked_links = 0
    passed_links = 0
    failed_links = []
    
    # Specific category checks
    cross_dir_checks = {
        'themes_to_pages': [],
        'pages_to_themes': [],
        'main_to_reports': [],
        'reports_to_pages': [],
        'apps_to_index': [],
        'pages_to_index': [],
        'index_to_subfolders': []
    }

    for html_file in sorted(html_files):
        rel_html_path = html_file.relative_to(BASE_DIR)
        file_dir = html_file.parent
        content = html_file.read_text(encoding='utf-8', errors='ignore')
        
        # 1. Parse HTML tags
        parser = LinkExtractor(html_file)
        try:
            parser.feed(content)
        except Exception as e:
            print(f"Error parsing HTML {rel_html_path}: {e}")
        
        tag_links = parser.links
        
        # 2. Extract CSS / JS references
        extra_urls = extract_js_and_css_urls(content)
        
        all_references = tag_links + [ (tag, attr, url, 0) for tag, attr, url in extra_urls ]
        
        for item in all_references:
            tag, attr, url, line_no = item
            total_links_found += 1
            
            if is_external_or_special(url):
                continue
            
            cleaned_url = clean_path(url)
            if not cleaned_url:
                continue
            
            checked_links += 1
            
            # Resolve target path relative to the file's directory
            target_path = (file_dir / cleaned_url).resolve()
            
            exists = target_path.exists()
            
            if exists:
                passed_links += 1
            else:
                failed_links.append({
                    'source_file': str(rel_html_path),
                    'line': line_no,
                    'tag': tag,
                    'attr': attr,
                    'raw_url': url,
                    'cleaned_url': cleaned_url,
                    'resolved_path': str(target_path)
                })

            # Record for specific category verification
            source_folder = rel_html_path.parts[0] if len(rel_html_path.parts) > 1 else 'root'
            
            if source_folder == 'themes' and 'pages/' in cleaned_url:
                cross_dir_checks['themes_to_pages'].append((str(rel_html_path), url, exists))
            elif source_folder == 'pages' and 'themes/' in cleaned_url:
                cross_dir_checks['pages_to_themes'].append((str(rel_html_path), url, exists))
            elif rel_html_path == Path('pages/main.html') and 'reports/' in cleaned_url:
                cross_dir_checks['main_to_reports'].append((str(rel_html_path), url, exists))
            elif source_folder == 'reports' and 'pages/' in cleaned_url:
                cross_dir_checks['reports_to_pages'].append((str(rel_html_path), url, exists))
            elif source_folder == 'apps' and cleaned_url in ('../index.html', 'index.html'):
                cross_dir_checks['apps_to_index'].append((str(rel_html_path), url, exists))
            elif source_folder == 'pages' and cleaned_url in ('../index.html', 'index.html'):
                cross_dir_checks['pages_to_index'].append((str(rel_html_path), url, exists))
            elif source_folder == 'root' and any(cleaned_url.startswith(p) for p in ('themes/', 'apps/', 'pages/', 'reports/', 'assets/')):
                cross_dir_checks['index_to_subfolders'].append((str(rel_html_path), url, exists))

    print("\n=== SUMMARY RESULTS ===")
    print(f"Total HTML files scanned: {len(html_files)}")
    print(f"Total link references found: {total_links_found}")
    print(f"Internal relative links checked: {checked_links}")
    print(f"Passed links: {passed_links}")
    print(f"Failed / Broken links: {len(failed_links)}")
    
    if failed_links:
        print("\n!!! BROKEN LINKS DETECTED !!!")
        for fl in failed_links:
            print(f"  File: {fl['source_file']}:{fl['line']} | Tag: <{fl['tag']} {fl['attr']}=\"{fl['raw_url']}\"> -> Target not found: {fl['resolved_path']}")
    else:
        print("\n✅ ALL internal relative links and asset paths resolve successfully!")
        
    print("\n=== CATEGORY CROSS-DIRECTORY LINK COUNTS ===")
    for cat, items in cross_dir_checks.items():
        valid_count = sum(1 for src, url, ex in items if ex)
        total_cat = len(items)
        print(f"  {cat}: {valid_count}/{total_cat} valid")
        
    return len(failed_links) == 0, failed_links, cross_dir_checks

if __name__ == '__main__':
    success, failed, cross_checks = test_all_links()
    if not success:
        sys.exit(1)
