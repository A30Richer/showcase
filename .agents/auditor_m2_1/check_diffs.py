import subprocess
import os
import difflib

showcase_dir = '/root/ai-workspace/test/dashboard/showcase'

# File mappings from original path at HEAD to current path in working tree
file_mappings = {
    'index.html': 'index.html',
    'website-design/index.html': 'website-design/index.html',
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
}

print(f"Comparing {len(file_mappings)} files against HEAD...")

total_changes = 0
suspicious_changes = []

for old_path, new_path in file_mappings.items():
    # Get original content from git HEAD
    try:
        orig_content = subprocess.check_output(
            ['git', 'show', f'HEAD:{old_path}'],
            cwd=showcase_dir,
            text=True
        )
    except Exception as e:
        print(f"ERROR reading HEAD:{old_path}: {e}")
        continue
    
    full_new_path = os.path.join(showcase_dir, new_path)
    if not os.path.exists(full_new_path):
        print(f"ERROR: {new_path} does not exist!")
        continue
    
    with open(full_new_path, 'r', encoding='utf-8') as f:
        curr_content = f.read()
        
    if orig_content == curr_content:
        print(f"Unchanged: {new_path}")
        continue
        
    orig_lines = orig_content.splitlines(keepends=True)
    curr_lines = curr_content.splitlines(keepends=True)
    
    diff = list(difflib.unified_diff(
        orig_lines, curr_lines,
        fromfile=f'HEAD:{old_path}',
        tofile=f'WORKING:{new_path}'
    ))
    
    print(f"\n--- Diff for {new_path} ({len(diff)} diff lines) ---")
    changes_in_file = 0
    for line in diff:
        if line.startswith(('+', '-')) and not line.startswith(('+++', '---')):
            changes_in_file += 1
            # Check if line change is something other than href/src/pageUrl or expected asset paths
            # Remove + / - marker
            clean_line = line[1:].strip()
            # If line is non-empty and doesn't contain href, src, or pageUrl, mark for detailed review
            if clean_line and not any(k in line for k in ['href', 'src', 'pageUrl', 'url(', 'stylesheet']):
                suspicious_changes.append((new_path, line.strip()))
            print(f"  {line.strip()}")
    total_changes += changes_in_file

print("\n" + "="*50)
print(f"Summary: Audited {len(file_mappings)} files.")
print(f"Suspicious (non-link/path) line diffs: {len(suspicious_changes)}")
if suspicious_changes:
    print("Found suspicious non-link changes:")
    for path, line in suspicious_changes:
        print(f"  [{path}] {line}")
else:
    print("All modified lines pertain ONLY to relative link / path updates!")
