#!/usr/bin/env python3
import os
import sys
import re
from pathlib import Path
from html.parser import HTMLParser

SHOWCASE_DIR = Path("/root/ai-workspace/showcase")

class DetailHTMLParser(HTMLParser):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.elements = []
        
    def handle_starttag(self, tag, attrs):
        line, col = self.getpos()
        attr_dict = dict(attrs)
        self.elements.append((tag, attr_dict, line))

def check_file_references(file_path):
    rel_path = file_path.relative_to(SHOWCASE_DIR)
    content = file_path.read_text(encoding='utf-8', errors='ignore')
    file_dir = file_path.parent
    
    parser = DetailHTMLParser(file_path.name)
    try:
        parser.feed(content)
    except Exception as e:
        print(f"[{rel_path}] Parse error: {e}")
        
    issues = []
    
    # Check HTML attributes
    for tag, attrs, line in parser.elements:
        for key in ('href', 'src', 'data-src', 'action'):
            if key in attrs:
                val = attrs[key].strip()
                if not val or val.startswith(('http://', 'https://', '//', 'data:', 'javascript:', 'mailto:', 'tel:', '#')):
                    continue
                if '${' in val or '{{' in val:
                    continue
                
                # Strip fragment and query
                clean_val = val.split('#')[0].split('?')[0]
                if not clean_val:
                    continue
                
                target = (file_dir / clean_val).resolve()
                if not target.exists():
                    issues.append((line, tag, key, val, str(target), "Target file does not exist"))

    # Check JS pageUrl or similar path variables
    js_paths = re.findall(r'[\'\"](\.\.?[^\'\"]+\.(?:html|png|jpg|jpeg|svg|css|js))[\'\"]', content)
    for path_str in js_paths:
        target = (file_dir / path_str).resolve()
        if not target.exists():
            issues.append((0, 'js-literal', 'string', path_str, str(target), "JS path target does not exist"))

    # Specific subfolder rules check for un-updated paths:
    # E.g. in a subfolder (depth 1: themes/, apps/, pages/, reports/), paths to assets/ should start with ../
    if len(rel_path.parts) > 1:
        # Check for bad un-updated relative paths like src="assets/images/..." instead of "../assets/images/..."
        bad_assets = re.findall(r'(?:href|src)=["\'](assets/[^"\']+)["\']', content)
        for ba in bad_assets:
            issues.append((0, 'un-updated-asset', 'src/href', ba, str(file_dir / ba), "Subfolder file references root assets/ without ../ prefix"))

        # Check for un-updated main.html references in reports
        if rel_path.parts[0] == 'reports':
            bad_mains = re.findall(r'href=["\'](main\.html[^"\']*)["\']', content)
            for bm in bad_mains:
                issues.append((0, 'un-updated-main', 'href', bm, str(file_dir / bm), "Report file references main.html without ../pages/ prefix"))

        # Check for un-updated index.html references in apps or pages
        if rel_path.parts[0] in ('apps', 'pages'):
            bad_indices = re.findall(r'href=["\'](index\.html[^"\']*)["\']', content)
            for bi in bad_indices:
                issues.append((0, 'un-updated-index', 'href', bi, str(file_dir / bi), f"{rel_path.parts[0]} file references index.html without ../ prefix"))

        # Check for un-updated website_design.html references in themes
        if rel_path.parts[0] == 'themes':
            bad_webdesigns = re.findall(r'href=["\'](website_design\.html[^"\']*)["\']', content)
            for bw in bad_webdesigns:
                issues.append((0, 'un-updated-website_design', 'href', bw, str(file_dir / bw), "Theme file references website_design.html without ../pages/ prefix"))

    return rel_path, issues

def run_detailed_checks():
    print("=== Running Detailed Edge Case & Sanity Tester ===")
    html_files = sorted([f for f in SHOWCASE_DIR.glob("**/*.html") if ".agents" not in f.parts])
    
    total_issues = 0
    file_results = {}
    
    for f in html_files:
        rel_path, issues = check_file_references(f)
        file_results[str(rel_path)] = issues
        if issues:
            total_issues += len(issues)
            print(f"\n❌ {rel_path} has {len(issues)} issue(s):")
            for line, tag, key, val, resolved, msg in issues:
                print(f"  - Line {line} <{tag} {key}=\"{val}\">: {msg} -> {resolved}")
        else:
            print(f"✓ {rel_path} OK")
            
    print(f"\nCompleted detailed checks. Total issues: {total_issues}")
    return total_issues == 0, file_results

if __name__ == '__main__':
    ok, _ = run_detailed_checks()
    sys.exit(0 if ok else 1)
