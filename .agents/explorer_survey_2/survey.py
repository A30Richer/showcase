import glob
import os
import re
import json

showcase_dir = '/root/ai-workspace/test/dashboard/showcase'

dest_map = {
    'index.html': 'index.html',
    # themes
    'style_01_glassmorphic.html': 'themes/style_01_glassmorphic.html',
    'style_02_neumorphic.html': 'themes/style_02_neumorphic.html',
    'style_03_cyberpunk.html': 'themes/style_03_cyberpunk.html',
    'style_04_neobrutalism.html': 'themes/style_04_neobrutalism.html',
    'style_05_clean_saas.html': 'themes/style_05_clean_saas.html',
    'style_06_synthwave.html': 'themes/style_06_synthwave.html',
    'style_07_luxury_gold.html': 'themes/style_07_luxury_gold.html',
    'style_08_bento_grid.html': 'themes/style_08_bento_grid.html',
    'style_09_claymorphism.html': 'themes/style_09_claymorphism.html',
    'style_10_hacker_terminal.html': 'themes/style_10_hacker_terminal.html',
    # apps
    'youtube_downloader.html': 'apps/youtube_downloader.html',
    'vocal_remover.html': 'apps/vocal_remover.html',
    'second_brain.html': 'apps/second_brain.html',
    'shop_vouchers.html': 'apps/shop_vouchers.html',
    # pages
    'cute_quiz.html': 'pages/cute_quiz.html',
    'love_counter.html': 'pages/love_counter.html',
    'present_agy_cli.html': 'pages/present_agy_cli.html',
    'website_design.html': 'pages/website_design.html',
    'main.html': 'pages/main.html',
    # reports
    'reports/gold-high-profit.html': 'reports/gold-high-profit.html',
    'reports/gold-small-account.html': 'reports/gold-small-account.html',
    'reports/market-monitor.html': 'reports/market-monitor.html',
    'reports/us100-daytrade.html': 'reports/us100-daytrade.html',
    'reports/vp-breakout.html': 'reports/vp-breakout.html',
    'website-design/index.html': 'website-design/index.html'
}

html_files = sorted(glob.glob(os.path.join(showcase_dir, '**/*.html'), recursive=True))

report_data = []

for fpath in html_files:
    rel_src = os.path.relpath(fpath, showcase_dir)
    rel_dst = dest_map.get(rel_src, rel_src)
    src_dir = os.path.dirname(rel_src)
    dst_dir = os.path.dirname(rel_dst)
    
    file_record = {
        'src': rel_src,
        'dst': rel_dst,
        'src_dir': src_dir,
        'dst_dir': dst_dir,
        'refs': []
    }
    
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    found_refs = []
    for i, line in enumerate(lines, 1):
        # find href
        for m in re.finditer(r'href=[\'\"]([^\'\"]+)[\'\"]', line):
            val = m.group(1)
            if not val.startswith('http') and not val.startswith('//') and not val.startswith('#') and not val.startswith('javascript:'):
                found_refs.append((i, 'href', val))
        # find src
        for m in re.finditer(r'src=[\'\"]([^\'\"]*)[\'\"]', line):
            val = m.group(1)
            if val and not val.startswith('http') and not val.startswith('//') and not val.startswith('data:'):
                found_refs.append((i, 'src', val))
        # find JS string references to relative path files
        for m in re.finditer(r'[\'\"]([^\'\"]+\.(?:html|png|jpg|jpeg|svg|css|js|json))[\'\"]', line):
            val = m.group(1)
            if not val.startswith('http') and not val.startswith('//'):
                if not any(r[0] == i and r[2] == val for r in found_refs):
                    found_refs.append((i, 'js_str', val))

    for line_num, rtype, val in found_refs:
        is_dynamic = '${' in val
        if is_dynamic:
            transformed = val  # needs template string evaluation logic if applicable
        else:
            orig_target_path = os.path.normpath(os.path.join(src_dir, val))
            new_target_path = dest_map.get(orig_target_path, orig_target_path)
            transformed = os.path.relpath(new_target_path, dst_dir)
        
        file_record['refs'].append({
            'line': line_num,
            'type': rtype,
            'original': val,
            'transformed': transformed,
            'is_dynamic': is_dynamic
        })
    
    report_data.append(file_record)

with open('/root/ai-workspace/test/dashboard/showcase/.agents/explorer_survey_2/full_survey.json', 'w') as f:
    json.dump(report_data, f, indent=2)

print(f"Processed {len(report_data)} HTML files successfully.")
