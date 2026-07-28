import json
import os

showcase_dir = '/root/ai-workspace/test/dashboard/showcase'
survey_json_path = '/root/ai-workspace/test/dashboard/showcase/.agents/explorer_survey_2/full_survey.json'
analysis_md_path = '/root/ai-workspace/test/dashboard/showcase/.agents/explorer_survey_2/analysis.md'
handoff_md_path = '/root/ai-workspace/test/dashboard/showcase/.agents/explorer_survey_2/handoff.md'

with open(survey_json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Grouping files
themes_files = [d for d in data if d['dst'].startswith('themes/')]
apps_files = [d for d in data if d['dst'].startswith('apps/')]
pages_files = [d for d in data if d['dst'].startswith('pages/')]
reports_files = [d for d in data if d['dst'].startswith('reports/')]
root_files = [d for d in data if d['dst'] == 'index.html']
other_files = [d for d in data if d['dst'].startswith('website-design/')]

analysis_content = []

analysis_content.append("# HTML Relative Link & Asset Reference Survey Analysis Report")
analysis_content.append("\n## Executive Summary\n")
analysis_content.append("This report documents all relative hyperlinks, asset references, script imports, style links, iframe, and JavaScript path references across **26 HTML files** in `/root/ai-workspace/test/dashboard/showcase`.")
analysis_content.append("It provides exact line-by-line inventory and exact path transformation rules required when reorganizing the showcase files into `themes/`, `apps/`, `pages/`, preserving root `index.html`, and maintaining existing subdirectories (`reports/`, `website-design/`).\n")

analysis_content.append("### Summary of File Categorization & Target Destinations")
analysis_content.append("| Current Relative Path | Target Destination | Categorization | Total Refs Found |")
analysis_content.append("|---|---|---|---|")

for item in data:
    analysis_content.append(f"| `{item['src']}` | `{item['dst']}` | {item['dst'].split('/')[0] if '/' in item['dst'] else 'Root'} | {len(item['refs'])} |")

analysis_content.append("\n---\n")
analysis_content.append("## Detailed File-by-File Inventory & Path Transformation Matrix\n")

for item in data:
    src = item['src']
    dst = item['dst']
    refs = item['refs']
    
    analysis_content.append(f"### File: `{src}` -> `{dst}`")
    if not refs:
        analysis_content.append("*No internal relative hyperlinks or asset references found.*")
    else:
        analysis_content.append("| Line | Type | Original Reference | Resolved Target File | Required Transformed Path |")
        analysis_content.append("|---|---|---|---|---|")
        for r in refs:
            line = r['line']
            rtype = r['type']
            orig = r['original']
            trans = r['transformed']
            
            # compute target file name
            if '${' in orig:
                target_desc = "Dynamic JS template variable"
            else:
                src_dir = os.path.dirname(src)
                target_desc = os.path.normpath(os.path.join(src_dir, orig))
            
            analysis_content.append(f"| {line} | `{rtype}` | `{orig}` | `{target_desc}` | `{trans}` |")
    analysis_content.append("\n")

analysis_content.append("---\n")
analysis_content.append("## Subdirectory Path Transformation Rules & Ruleset\n")

analysis_content.append("### 1. Root Directory (`index.html`)")
analysis_content.append("- Remains at `/index.html` (root level).")
analysis_content.append("- **Hyperlinks to Pages** (`pages/`):")
analysis_content.append("  - `main.html` -> `pages/main.html` (Line 522)")
analysis_content.append("  - `present_agy_cli.html` -> `pages/present_agy_cli.html` (Line 558)")
analysis_content.append("  - `cute_quiz.html` -> `pages/cute_quiz.html` (Line 578)")
analysis_content.append("  - `love_counter.html` -> `pages/love_counter.html` (Line 596)")
analysis_content.append("  - `website_design.html` -> `pages/website_design.html` (Line 709)")
analysis_content.append("- **Hyperlinks to Apps** (`apps/`):")
analysis_content.append("  - `second_brain.html` -> `apps/second_brain.html` (Line 614)")
analysis_content.append("  - `youtube_downloader.html` -> `apps/youtube_downloader.html` (Line 653)")
analysis_content.append("  - `vocal_remover.html` -> `apps/vocal_remover.html` (Line 671)")
analysis_content.append("  - `shop_vouchers.html` -> `apps/shop_vouchers.html` (Line 689)")
analysis_content.append("- **Hyperlinks to Themes** (`themes/`):")
analysis_content.append("  - `style_01_glassmorphic.html` .. `style_10_hacker_terminal.html` -> `themes/style_01_glassmorphic.html` .. `themes/style_10_hacker_terminal.html` (Lines 727, 745, 763, 781, 799, 817, 835, 853, 871, 889)")
analysis_content.append("- **Hyperlinks to Reports** (`reports/`):")
analysis_content.append("  - `reports/*.html` -> unchanged (`reports/*.html`) (Lines 484, 502, 540)")

analysis_content.append("\n### 2. Files Moving into `themes/` (`style_01` to `style_10`)")
analysis_content.append("- Location changes from `root` to `themes/` (one directory level deeper).")
analysis_content.append("- **Hyperlink to `website_design.html`**:")
analysis_content.append("  - Original: `href=\"website_design.html\"`")
analysis_content.append("  - Transformed: `href=\"../pages/website_design.html\"` (Lines vary per file: e.g., style_01 lines 369, 376; style_02 lines 327, 334; etc.)")

analysis_content.append("\n### 3. Files Moving into `apps/` (`second_brain.html`, `vocal_remover.html`, `youtube_downloader.html`, `shop_vouchers.html`)")
analysis_content.append("- Location changes from `root` to `apps/` (one directory level deeper).")
analysis_content.append("- **Hyperlink to Root `index.html`**:")
analysis_content.append("  - Original: `href=\"index.html\"`")
analysis_content.append("  - Transformed: `href=\"../index.html\"` (second_brain: 293, 304; vocal_remover: 369, 377; youtube_downloader: 550, 558)")

analysis_content.append("\n### 4. Files Moving into `pages/` (`cute_quiz.html`, `present_agy_cli.html`, `website_design.html`, `main.html`)")
analysis_content.append("- Location changes from `root` to `pages/` (one directory level deeper).")
analysis_content.append("- **Hyperlinks to Root `index.html`**:")
analysis_content.append("  - Original: `href=\"index.html\"` -> `href=\"../index.html\"` (cute_quiz: 391; present_agy_cli: 270; website_design: 807, 817)")
analysis_content.append("- **`pages/website_design.html` (Theme gallery cards & JS data array)**:")
analysis_content.append("  - JS Array data (`style_01_glassmorphic.html` .. `style_10_hacker_terminal.html`):")
analysis_content.append("    - Original: `'style_01_glassmorphic.html'` .. `'style_10_hacker_terminal.html'`")
analysis_content.append("    - Transformed: `'../themes/style_01_glassmorphic.html'` .. `'../themes/style_10_hacker_terminal.html'` (Lines 889, 930, 971, 1007, 1045, 1079, 1113, 1147, 1190, 1225)")
analysis_content.append("- **`pages/main.html` (Trading Dashboard & Reports navigation)**:")
analysis_content.append("  - Self-references (`main.html`): `href=\"main.html\"` -> `href=\"main.html\"` (remains relative within `pages/`, lines 298, 306)")
analysis_content.append("  - Links to Reports (`reports/*.html`): `href=\"reports/*.html\"` -> `href=\"../reports/*.html\"` (Lines 307-311, 362, 391, 420, 449)")
analysis_content.append("  - Image references (`assets/images/*.png`): `src=\"assets/images/*.png\"` -> `src=\"../assets/images/*.png\"` (Lines 341, 370, 399, 428)")

analysis_content.append("\n### 5. Files Remaining in `reports/` (`gold-high-profit.html`, `gold-small-account.html`, `market-monitor.html`, `us100-daytrade.html`, `vp-breakout.html`)")
analysis_content.append("- HTML files remain inside `reports/` directory.")
analysis_content.append("- **Navigation Links Back to `main.html`**:")
analysis_content.append("  - Original: `href=\"../main.html\"` (points to old root `main.html`)")
analysis_content.append("  - Transformed: `href=\"../pages/main.html\"` (MUST update to new location in `pages/`!)")
analysis_content.append("- **Sibling Report Links** (`vp-breakout.html`, `gold-high-profit.html`, etc.):")
analysis_content.append("  - Unchanged (`vp-breakout.html`, `gold-high-profit.html`, etc.)")
analysis_content.append("- **Asset Image References** (`../assets/images/*.png`):")
analysis_content.append("  - Unchanged (`../assets/images/*.png`) because relative depth from `reports/` to `assets/` remains identical.")

analysis_content.append("\n---\n")
analysis_content.append("## Verification Strategy & Invalidation Conditions\n")
analysis_content.append("1. **Static Link Verification**: Check every `<a href>`, `<img src>`, `<script src>`, `<link href>`, and JS string literal in the codebase using Python regex parser to ensure 0 references point to non-existent paths.")
analysis_content.append("2. **Local HTTP Server Test**: Launch `python3 -m http.server` and test navigation between root `index.html`, `themes/*`, `apps/*`, `pages/*`, and `reports/*`.")
analysis_content.append("3. **Invalidation Conditions**: Any remaining relative path starting with `style_*.html` in root index without `themes/` prefix, or `../main.html` in reports without `../pages/main.html`.")

with open(analysis_md_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(analysis_content))

print(f"Written analysis report to {analysis_md_path}")
