#!/usr/bin/env python3
import os
from pathlib import Path
from html.parser import HTMLParser

SHOWCASE_DIR = Path("/root/ai-workspace/showcase")

class LinkGrabber(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if k in ('href', 'src'):
                self.links.append((tag, k, v))

def run_matrix():
    print("=== CROSS-DIRECTORY LINK & ASSET MATRIX ===")
    
    categories = {
        'themes -> pages': [],
        'pages -> themes': [],
        'main -> reports': [],
        'reports -> pages': [],
        'apps -> index': [],
        'pages -> index': [],
        'reports -> assets': [],
        'pages -> assets': [],
        'index -> subdirectories': []
    }

    html_files = sorted([f for f in SHOWCASE_DIR.glob("**/*.html") if ".agents" not in f.parts])
    
    for f in html_files:
        rel_f = f.relative_to(SHOWCASE_DIR)
        parser = LinkGrabber()
        parser.feed(f.read_text(encoding='utf-8', errors='ignore'))
        
        for tag, attr, url in parser.links:
            if url.startswith(('http', '//', '#', 'data:', 'javascript:')):
                continue
            clean_url = url.split('#')[0].split('?')[0]
            if not clean_url:
                continue
            
            target = (f.parent / clean_url).resolve()
            exists = target.exists()
            entry = (str(rel_f), tag, attr, url, clean_url, str(target), exists)
            
            # Categorize
            folder = rel_f.parts[0] if len(rel_f.parts) > 1 else 'root'
            
            if folder == 'themes' and 'pages/' in clean_url:
                categories['themes -> pages'].append(entry)
            elif folder == 'pages' and 'themes/' in clean_url:
                categories['pages -> themes'].append(entry)
            elif str(rel_f) == 'pages/main.html' and 'reports/' in clean_url:
                categories['main -> reports'].append(entry)
            elif folder == 'reports' and 'pages/' in clean_url:
                categories['reports -> pages'].append(entry)
            elif folder == 'apps' and clean_url.endswith('index.html'):
                categories['apps -> index'].append(entry)
            elif folder == 'pages' and clean_url.endswith('index.html'):
                categories['pages -> index'].append(entry)
            elif folder == 'reports' and 'assets/' in clean_url:
                categories['reports -> assets'].append(entry)
            elif folder == 'pages' and 'assets/' in clean_url:
                categories['pages -> assets'].append(entry)
            elif folder == 'root' and any(clean_url.startswith(d) for d in ('themes/', 'apps/', 'pages/', 'reports/', 'assets/')):
                categories['index -> subdirectories'].append(entry)

    for cat_name, entries in categories.items():
        print(f"\n--- {cat_name} (Total: {len(entries)}) ---")
        for src_f, tag, attr, raw_url, clean_url, target, exists in entries:
            status = "OK" if exists else "BROKEN"
            print(f"  [{status}] {src_f} --<{tag} {attr}=\"{raw_url}\">--> {clean_url} (Resolved: {target})")

if __name__ == '__main__':
    run_matrix()
