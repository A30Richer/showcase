import subprocess
import os
import difflib

showcase_dir = '/root/ai-workspace/test/dashboard/showcase'

file_mappings = {
    'index.html': 'index.html',
    'website-design/index.html': 'website-design/index.html',
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
    'youtube_downloader.html': 'apps/youtube_downloader.html',
    'vocal_remover.html': 'apps/vocal_remover.html',
    'second_brain.html': 'apps/second_brain.html',
    'shop_vouchers.html': 'apps/shop_vouchers.html',
    'cute_quiz.html': 'pages/cute_quiz.html',
    'love_counter.html': 'pages/love_counter.html',
    'present_agy_cli.html': 'pages/present_agy_cli.html',
    'website_design.html': 'pages/website_design.html',
    'main.html': 'pages/main.html',
    'reports/gold-high-profit.html': 'reports/gold-high-profit.html',
    'reports/gold-small-account.html': 'reports/gold-small-account.html',
    'reports/market-monitor.html': 'reports/market-monitor.html',
    'reports/us100-daytrade.html': 'reports/us100-daytrade.html',
    'reports/vp-breakout.html': 'reports/vp-breakout.html',
}

files_with_non_link_diffs = {}

for old_path, new_path in file_mappings.items():
    orig_content = subprocess.check_output(
        ['git', 'show', f'HEAD:{old_path}'],
        cwd=showcase_dir,
        text=True
    )
    
    full_new_path = os.path.join(showcase_dir, new_path)
    with open(full_new_path, 'r', encoding='utf-8') as f:
        curr_content = f.read()
        
    orig_lines = orig_content.splitlines(keepends=True)
    curr_lines = curr_content.splitlines(keepends=True)
    
    diff = list(difflib.unified_diff(orig_lines, curr_lines))
    
    non_link_diffs = []
    for line in diff:
        if line.startswith(('+', '-')) and not line.startswith(('+++', '---')):
            clean_line = line[1:].strip()
            # If line change does not involve href=, src=, pageUrl:, or path adjustments
            # check if it's purely a link path change or structural/content change
            if not any(k in line for k in ['href=', 'src=', 'pageUrl:', '../pages/', '../themes/', '../apps/', '../index.html', '../reports/', '../assets/', 'themes/', 'apps/', 'pages/']):
                non_link_diffs.append(line.strip())
            # Even if it contains href or src, check if title/text inside tag changed as well!
            elif line.startswith('+') or line.startswith('-'):
                # Check if non-attribute text in the line changed
                pass
                
    if non_link_diffs:
        files_with_non_link_diffs[new_path] = non_link_diffs

print(f"Files with non-link diffs count: {len(files_with_non_link_diffs)}")
for fpath, diffs in files_with_non_link_diffs.items():
    print(f"\nFile: {fpath} ({len(diffs)} lines):")
    for d in diffs[:10]:
        print(f"  {d}")
    if len(diffs) > 10:
        print(f"  ... and {len(diffs)-10} more lines.")
