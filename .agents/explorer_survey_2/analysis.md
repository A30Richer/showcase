# HTML Relative Link & Asset Reference Survey Analysis Report

## Executive Summary

This report documents all relative hyperlinks, asset references, script imports, style links, iframe, and JavaScript path references across **26 HTML files** in `/root/ai-workspace/test/dashboard/showcase`.
It provides exact line-by-line inventory and exact path transformation rules required when reorganizing the showcase files into `themes/`, `apps/`, `pages/`, preserving root `index.html`, and maintaining existing subdirectories (`reports/`, `website-design/`).

### Summary of File Categorization & Target Destinations
| Current Relative Path | Target Destination | Categorization | Total Refs Found |
|---|---|---|---|
| `cute_quiz.html` | `pages/cute_quiz.html` | pages | 1 |
| `index.html` | `index.html` | Root | 23 |
| `love_counter.html` | `pages/love_counter.html` | pages | 0 |
| `main.html` | `pages/main.html` | pages | 15 |
| `present_agy_cli.html` | `pages/present_agy_cli.html` | pages | 1 |
| `reports/gold-high-profit.html` | `reports/gold-high-profit.html` | reports | 8 |
| `reports/gold-small-account.html` | `reports/gold-small-account.html` | reports | 8 |
| `reports/market-monitor.html` | `reports/market-monitor.html` | reports | 8 |
| `reports/us100-daytrade.html` | `reports/us100-daytrade.html` | reports | 8 |
| `reports/vp-breakout.html` | `reports/vp-breakout.html` | reports | 9 |
| `second_brain.html` | `apps/second_brain.html` | apps | 2 |
| `shop_vouchers.html` | `apps/shop_vouchers.html` | apps | 1 |
| `style_01_glassmorphic.html` | `themes/style_01_glassmorphic.html` | themes | 2 |
| `style_02_neumorphic.html` | `themes/style_02_neumorphic.html` | themes | 2 |
| `style_03_cyberpunk.html` | `themes/style_03_cyberpunk.html` | themes | 2 |
| `style_04_neobrutalism.html` | `themes/style_04_neobrutalism.html` | themes | 2 |
| `style_05_clean_saas.html` | `themes/style_05_clean_saas.html` | themes | 2 |
| `style_06_synthwave.html` | `themes/style_06_synthwave.html` | themes | 2 |
| `style_07_luxury_gold.html` | `themes/style_07_luxury_gold.html` | themes | 2 |
| `style_08_bento_grid.html` | `themes/style_08_bento_grid.html` | themes | 2 |
| `style_09_claymorphism.html` | `themes/style_09_claymorphism.html` | themes | 2 |
| `style_10_hacker_terminal.html` | `themes/style_10_hacker_terminal.html` | themes | 2 |
| `vocal_remover.html` | `apps/vocal_remover.html` | apps | 2 |
| `website-design/index.html` | `website-design/index.html` | website-design | 0 |
| `website_design.html` | `pages/website_design.html` | pages | 13 |
| `youtube_downloader.html` | `apps/youtube_downloader.html` | apps | 2 |

---

## Detailed File-by-File Inventory & Path Transformation Matrix

### File: `cute_quiz.html` -> `pages/cute_quiz.html`
| Line | Type | Original Reference | Resolved Target File | Required Transformed Path |
|---|---|---|---|---|
| 391 | `href` | `index.html` | `index.html` | `../index.html` |


### File: `index.html` -> `index.html`
| Line | Type | Original Reference | Resolved Target File | Required Transformed Path |
|---|---|---|---|---|
| 439 | `href` | `index.html` | `index.html` | `index.html` |
| 484 | `href` | `reports/market-monitor.html` | `reports/market-monitor.html` | `reports/market-monitor.html` |
| 502 | `href` | `reports/vp-breakout.html` | `reports/vp-breakout.html` | `reports/vp-breakout.html` |
| 522 | `href` | `main.html` | `main.html` | `pages/main.html` |
| 540 | `href` | `reports/gold-small-account.html` | `reports/gold-small-account.html` | `reports/gold-small-account.html` |
| 558 | `href` | `present_agy_cli.html` | `present_agy_cli.html` | `pages/present_agy_cli.html` |
| 578 | `href` | `cute_quiz.html` | `cute_quiz.html` | `pages/cute_quiz.html` |
| 596 | `href` | `love_counter.html` | `love_counter.html` | `pages/love_counter.html` |
| 614 | `href` | `second_brain.html` | `second_brain.html` | `apps/second_brain.html` |
| 653 | `href` | `youtube_downloader.html` | `youtube_downloader.html` | `apps/youtube_downloader.html` |
| 671 | `href` | `vocal_remover.html` | `vocal_remover.html` | `apps/vocal_remover.html` |
| 689 | `href` | `shop_vouchers.html` | `shop_vouchers.html` | `apps/shop_vouchers.html` |
| 709 | `href` | `website_design.html` | `website_design.html` | `pages/website_design.html` |
| 727 | `href` | `style_01_glassmorphic.html` | `style_01_glassmorphic.html` | `themes/style_01_glassmorphic.html` |
| 745 | `href` | `style_02_neumorphic.html` | `style_02_neumorphic.html` | `themes/style_02_neumorphic.html` |
| 763 | `href` | `style_03_cyberpunk.html` | `style_03_cyberpunk.html` | `themes/style_03_cyberpunk.html` |
| 781 | `href` | `style_04_neobrutalism.html` | `style_04_neobrutalism.html` | `themes/style_04_neobrutalism.html` |
| 799 | `href` | `style_05_clean_saas.html` | `style_05_clean_saas.html` | `themes/style_05_clean_saas.html` |
| 817 | `href` | `style_06_synthwave.html` | `style_06_synthwave.html` | `themes/style_06_synthwave.html` |
| 835 | `href` | `style_07_luxury_gold.html` | `style_07_luxury_gold.html` | `themes/style_07_luxury_gold.html` |
| 853 | `href` | `style_08_bento_grid.html` | `style_08_bento_grid.html` | `themes/style_08_bento_grid.html` |
| 871 | `href` | `style_09_claymorphism.html` | `style_09_claymorphism.html` | `themes/style_09_claymorphism.html` |
| 889 | `href` | `style_10_hacker_terminal.html` | `style_10_hacker_terminal.html` | `themes/style_10_hacker_terminal.html` |


### File: `love_counter.html` -> `pages/love_counter.html`
*No internal relative hyperlinks or asset references found.*


### File: `main.html` -> `pages/main.html`
| Line | Type | Original Reference | Resolved Target File | Required Transformed Path |
|---|---|---|---|---|
| 298 | `href` | `main.html` | `main.html` | `main.html` |
| 306 | `href` | `main.html` | `main.html` | `main.html` |
| 307 | `href` | `reports/gold-small-account.html` | `reports/gold-small-account.html` | `../reports/gold-small-account.html` |
| 308 | `href` | `reports/vp-breakout.html` | `reports/vp-breakout.html` | `../reports/vp-breakout.html` |
| 309 | `href` | `reports/gold-high-profit.html` | `reports/gold-high-profit.html` | `../reports/gold-high-profit.html` |
| 310 | `href` | `reports/us100-daytrade.html` | `reports/us100-daytrade.html` | `../reports/us100-daytrade.html` |
| 311 | `href` | `reports/market-monitor.html` | `reports/market-monitor.html` | `../reports/market-monitor.html` |
| 341 | `src` | `assets/images/gold_micro_100_backtest_chart.png` | `assets/images/gold_micro_100_backtest_chart.png` | `../assets/images/gold_micro_100_backtest_chart.png` |
| 362 | `href` | `reports/gold-small-account.html` | `reports/gold-small-account.html` | `../reports/gold-small-account.html` |
| 370 | `src` | `assets/images/vp_breakout_best_chart.png` | `assets/images/vp_breakout_best_chart.png` | `../assets/images/vp_breakout_best_chart.png` |
| 391 | `href` | `reports/vp-breakout.html` | `reports/vp-breakout.html` | `../reports/vp-breakout.html` |
| 399 | `src` | `assets/images/gold_backtest_results.png` | `assets/images/gold_backtest_results.png` | `../assets/images/gold_backtest_results.png` |
| 420 | `href` | `reports/gold-high-profit.html` | `reports/gold-high-profit.html` | `../reports/gold-high-profit.html` |
| 428 | `src` | `assets/images/us100_backtest_results.png` | `assets/images/us100_backtest_results.png` | `../assets/images/us100_backtest_results.png` |
| 449 | `href` | `reports/us100-daytrade.html` | `reports/us100-daytrade.html` | `../reports/us100-daytrade.html` |


### File: `present_agy_cli.html` -> `pages/present_agy_cli.html`
| Line | Type | Original Reference | Resolved Target File | Required Transformed Path |
|---|---|---|---|---|
| 270 | `href` | `index.html` | `index.html` | `../index.html` |


### File: `reports/gold-high-profit.html` -> `reports/gold-high-profit.html`
| Line | Type | Original Reference | Resolved Target File | Required Transformed Path |
|---|---|---|---|---|
| 50 | `href` | `../main.html` | `main.html` | `../pages/main.html` |
| 56 | `href` | `../main.html` | `main.html` | `../pages/main.html` |
| 57 | `href` | `vp-breakout.html` | `reports/vp-breakout.html` | `vp-breakout.html` |
| 58 | `href` | `gold-high-profit.html` | `reports/gold-high-profit.html` | `gold-high-profit.html` |
| 59 | `href` | `us100-daytrade.html` | `reports/us100-daytrade.html` | `us100-daytrade.html` |
| 60 | `href` | `market-monitor.html` | `reports/market-monitor.html` | `market-monitor.html` |
| 67 | `href` | `../main.html` | `main.html` | `../pages/main.html` |
| 92 | `src` | `../assets/images/gold_backtest_results.png` | `assets/images/gold_backtest_results.png` | `../assets/images/gold_backtest_results.png` |


### File: `reports/gold-small-account.html` -> `reports/gold-small-account.html`
| Line | Type | Original Reference | Resolved Target File | Required Transformed Path |
|---|---|---|---|---|
| 78 | `href` | `../main.html` | `main.html` | `../pages/main.html` |
| 84 | `href` | `../main.html` | `main.html` | `../pages/main.html` |
| 85 | `href` | `gold-small-account.html` | `reports/gold-small-account.html` | `gold-small-account.html` |
| 86 | `href` | `vp-breakout.html` | `reports/vp-breakout.html` | `vp-breakout.html` |
| 87 | `href` | `gold-high-profit.html` | `reports/gold-high-profit.html` | `gold-high-profit.html` |
| 88 | `href` | `us100-daytrade.html` | `reports/us100-daytrade.html` | `us100-daytrade.html` |
| 95 | `href` | `../main.html` | `main.html` | `../pages/main.html` |
| 304 | `src` | `../assets/images/gold_micro_100_backtest_chart.png` | `assets/images/gold_micro_100_backtest_chart.png` | `../assets/images/gold_micro_100_backtest_chart.png` |


### File: `reports/market-monitor.html` -> `reports/market-monitor.html`
| Line | Type | Original Reference | Resolved Target File | Required Transformed Path |
|---|---|---|---|---|
| 49 | `href` | `../main.html` | `main.html` | `../pages/main.html` |
| 55 | `href` | `../main.html` | `main.html` | `../pages/main.html` |
| 56 | `href` | `vp-breakout.html` | `reports/vp-breakout.html` | `vp-breakout.html` |
| 57 | `href` | `gold-high-profit.html` | `reports/gold-high-profit.html` | `gold-high-profit.html` |
| 58 | `href` | `us100-daytrade.html` | `reports/us100-daytrade.html` | `us100-daytrade.html` |
| 59 | `href` | `market-monitor.html` | `reports/market-monitor.html` | `market-monitor.html` |
| 66 | `href` | `../main.html` | `main.html` | `../pages/main.html` |
| 87 | `src` | `../assets/images/vp_zones_chart.png` | `assets/images/vp_zones_chart.png` | `../assets/images/vp_zones_chart.png` |


### File: `reports/us100-daytrade.html` -> `reports/us100-daytrade.html`
| Line | Type | Original Reference | Resolved Target File | Required Transformed Path |
|---|---|---|---|---|
| 50 | `href` | `../main.html` | `main.html` | `../pages/main.html` |
| 56 | `href` | `../main.html` | `main.html` | `../pages/main.html` |
| 57 | `href` | `vp-breakout.html` | `reports/vp-breakout.html` | `vp-breakout.html` |
| 58 | `href` | `gold-high-profit.html` | `reports/gold-high-profit.html` | `gold-high-profit.html` |
| 59 | `href` | `us100-daytrade.html` | `reports/us100-daytrade.html` | `us100-daytrade.html` |
| 60 | `href` | `market-monitor.html` | `reports/market-monitor.html` | `market-monitor.html` |
| 67 | `href` | `../main.html` | `main.html` | `../pages/main.html` |
| 92 | `src` | `../assets/images/us100_backtest_results.png` | `assets/images/us100_backtest_results.png` | `../assets/images/us100_backtest_results.png` |


### File: `reports/vp-breakout.html` -> `reports/vp-breakout.html`
| Line | Type | Original Reference | Resolved Target File | Required Transformed Path |
|---|---|---|---|---|
| 50 | `href` | `../main.html` | `main.html` | `../pages/main.html` |
| 56 | `href` | `../main.html` | `main.html` | `../pages/main.html` |
| 57 | `href` | `vp-breakout.html` | `reports/vp-breakout.html` | `vp-breakout.html` |
| 58 | `href` | `gold-high-profit.html` | `reports/gold-high-profit.html` | `gold-high-profit.html` |
| 59 | `href` | `us100-daytrade.html` | `reports/us100-daytrade.html` | `us100-daytrade.html` |
| 60 | `href` | `market-monitor.html` | `reports/market-monitor.html` | `market-monitor.html` |
| 67 | `href` | `../main.html` | `main.html` | `../pages/main.html` |
| 92 | `src` | `../assets/images/vp_breakout_best_chart.png` | `assets/images/vp_breakout_best_chart.png` | `../assets/images/vp_breakout_best_chart.png` |
| 97 | `src` | `../assets/images/vp_zones_chart.png` | `assets/images/vp_zones_chart.png` | `../assets/images/vp_zones_chart.png` |


### File: `second_brain.html` -> `apps/second_brain.html`
| Line | Type | Original Reference | Resolved Target File | Required Transformed Path |
|---|---|---|---|---|
| 293 | `href` | `index.html` | `index.html` | `../index.html` |
| 304 | `href` | `index.html` | `index.html` | `../index.html` |


### File: `shop_vouchers.html` -> `apps/shop_vouchers.html`
| Line | Type | Original Reference | Resolved Target File | Required Transformed Path |
|---|---|---|---|---|
| 1241 | `src` | `${shop.avatar}` | `Dynamic JS template variable` | `${shop.avatar}` |


### File: `style_01_glassmorphic.html` -> `themes/style_01_glassmorphic.html`
| Line | Type | Original Reference | Resolved Target File | Required Transformed Path |
|---|---|---|---|---|
| 369 | `href` | `website_design.html` | `website_design.html` | `../pages/website_design.html` |
| 376 | `href` | `website_design.html` | `website_design.html` | `../pages/website_design.html` |


### File: `style_02_neumorphic.html` -> `themes/style_02_neumorphic.html`
| Line | Type | Original Reference | Resolved Target File | Required Transformed Path |
|---|---|---|---|---|
| 327 | `href` | `website_design.html` | `website_design.html` | `../pages/website_design.html` |
| 334 | `href` | `website_design.html` | `website_design.html` | `../pages/website_design.html` |


### File: `style_03_cyberpunk.html` -> `themes/style_03_cyberpunk.html`
| Line | Type | Original Reference | Resolved Target File | Required Transformed Path |
|---|---|---|---|---|
| 179 | `href` | `website_design.html` | `website_design.html` | `../pages/website_design.html` |
| 183 | `href` | `website_design.html` | `website_design.html` | `../pages/website_design.html` |


### File: `style_04_neobrutalism.html` -> `themes/style_04_neobrutalism.html`
| Line | Type | Original Reference | Resolved Target File | Required Transformed Path |
|---|---|---|---|---|
| 232 | `href` | `website_design.html` | `website_design.html` | `../pages/website_design.html` |
| 240 | `href` | `website_design.html` | `website_design.html` | `../pages/website_design.html` |


### File: `style_05_clean_saas.html` -> `themes/style_05_clean_saas.html`
| Line | Type | Original Reference | Resolved Target File | Required Transformed Path |
|---|---|---|---|---|
| 242 | `href` | `website_design.html` | `website_design.html` | `../pages/website_design.html` |
| 247 | `href` | `website_design.html` | `website_design.html` | `../pages/website_design.html` |


### File: `style_06_synthwave.html` -> `themes/style_06_synthwave.html`
| Line | Type | Original Reference | Resolved Target File | Required Transformed Path |
|---|---|---|---|---|
| 147 | `href` | `website_design.html` | `website_design.html` | `../pages/website_design.html` |
| 151 | `href` | `website_design.html` | `website_design.html` | `../pages/website_design.html` |


### File: `style_07_luxury_gold.html` -> `themes/style_07_luxury_gold.html`
| Line | Type | Original Reference | Resolved Target File | Required Transformed Path |
|---|---|---|---|---|
| 165 | `href` | `website_design.html` | `website_design.html` | `../pages/website_design.html` |
| 169 | `href` | `website_design.html` | `website_design.html` | `../pages/website_design.html` |


### File: `style_08_bento_grid.html` -> `themes/style_08_bento_grid.html`
| Line | Type | Original Reference | Resolved Target File | Required Transformed Path |
|---|---|---|---|---|
| 149 | `href` | `website_design.html` | `website_design.html` | `../pages/website_design.html` |
| 153 | `href` | `website_design.html` | `website_design.html` | `../pages/website_design.html` |


### File: `style_09_claymorphism.html` -> `themes/style_09_claymorphism.html`
| Line | Type | Original Reference | Resolved Target File | Required Transformed Path |
|---|---|---|---|---|
| 116 | `href` | `website_design.html` | `website_design.html` | `../pages/website_design.html` |
| 120 | `href` | `website_design.html` | `website_design.html` | `../pages/website_design.html` |


### File: `style_10_hacker_terminal.html` -> `themes/style_10_hacker_terminal.html`
| Line | Type | Original Reference | Resolved Target File | Required Transformed Path |
|---|---|---|---|---|
| 153 | `href` | `website_design.html` | `website_design.html` | `../pages/website_design.html` |
| 157 | `href` | `website_design.html` | `website_design.html` | `../pages/website_design.html` |


### File: `vocal_remover.html` -> `apps/vocal_remover.html`
| Line | Type | Original Reference | Resolved Target File | Required Transformed Path |
|---|---|---|---|---|
| 369 | `href` | `index.html` | `index.html` | `../index.html` |
| 377 | `href` | `index.html` | `index.html` | `../index.html` |


### File: `website-design/index.html` -> `website-design/index.html`
*No internal relative hyperlinks or asset references found.*


### File: `website_design.html` -> `pages/website_design.html`
| Line | Type | Original Reference | Resolved Target File | Required Transformed Path |
|---|---|---|---|---|
| 807 | `href` | `index.html` | `index.html` | `../index.html` |
| 817 | `href` | `index.html` | `index.html` | `../index.html` |
| 889 | `js_str` | `style_01_glassmorphic.html` | `style_01_glassmorphic.html` | `../themes/style_01_glassmorphic.html` |
| 930 | `js_str` | `style_02_neumorphic.html` | `style_02_neumorphic.html` | `../themes/style_02_neumorphic.html` |
| 971 | `js_str` | `style_03_cyberpunk.html` | `style_03_cyberpunk.html` | `../themes/style_03_cyberpunk.html` |
| 1007 | `js_str` | `style_04_neobrutalism.html` | `style_04_neobrutalism.html` | `../themes/style_04_neobrutalism.html` |
| 1045 | `js_str` | `style_05_clean_saas.html` | `style_05_clean_saas.html` | `../themes/style_05_clean_saas.html` |
| 1079 | `js_str` | `style_06_synthwave.html` | `style_06_synthwave.html` | `../themes/style_06_synthwave.html` |
| 1113 | `js_str` | `style_07_luxury_gold.html` | `style_07_luxury_gold.html` | `../themes/style_07_luxury_gold.html` |
| 1147 | `js_str` | `style_08_bento_grid.html` | `style_08_bento_grid.html` | `../themes/style_08_bento_grid.html` |
| 1190 | `js_str` | `style_09_claymorphism.html` | `style_09_claymorphism.html` | `../themes/style_09_claymorphism.html` |
| 1225 | `js_str` | `style_10_hacker_terminal.html` | `style_10_hacker_terminal.html` | `../themes/style_10_hacker_terminal.html` |
| 1303 | `href` | `${item.pageUrl}` | `Dynamic JS template variable` | `${item.pageUrl}` |


### File: `youtube_downloader.html` -> `apps/youtube_downloader.html`
| Line | Type | Original Reference | Resolved Target File | Required Transformed Path |
|---|---|---|---|---|
| 550 | `href` | `index.html` | `index.html` | `../index.html` |
| 558 | `href` | `index.html` | `index.html` | `../index.html` |


---

## Subdirectory Path Transformation Rules & Ruleset

### 1. Root Directory (`index.html`)
- Remains at `/index.html` (root level).
- **Hyperlinks to Pages** (`pages/`):
  - `main.html` -> `pages/main.html` (Line 522)
  - `present_agy_cli.html` -> `pages/present_agy_cli.html` (Line 558)
  - `cute_quiz.html` -> `pages/cute_quiz.html` (Line 578)
  - `love_counter.html` -> `pages/love_counter.html` (Line 596)
  - `website_design.html` -> `pages/website_design.html` (Line 709)
- **Hyperlinks to Apps** (`apps/`):
  - `second_brain.html` -> `apps/second_brain.html` (Line 614)
  - `youtube_downloader.html` -> `apps/youtube_downloader.html` (Line 653)
  - `vocal_remover.html` -> `apps/vocal_remover.html` (Line 671)
  - `shop_vouchers.html` -> `apps/shop_vouchers.html` (Line 689)
- **Hyperlinks to Themes** (`themes/`):
  - `style_01_glassmorphic.html` .. `style_10_hacker_terminal.html` -> `themes/style_01_glassmorphic.html` .. `themes/style_10_hacker_terminal.html` (Lines 727, 745, 763, 781, 799, 817, 835, 853, 871, 889)
- **Hyperlinks to Reports** (`reports/`):
  - `reports/*.html` -> unchanged (`reports/*.html`) (Lines 484, 502, 540)

### 2. Files Moving into `themes/` (`style_01` to `style_10`)
- Location changes from `root` to `themes/` (one directory level deeper).
- **Hyperlink to `website_design.html`**:
  - Original: `href="website_design.html"`
  - Transformed: `href="../pages/website_design.html"` (Lines vary per file: e.g., style_01 lines 369, 376; style_02 lines 327, 334; etc.)

### 3. Files Moving into `apps/` (`second_brain.html`, `vocal_remover.html`, `youtube_downloader.html`, `shop_vouchers.html`)
- Location changes from `root` to `apps/` (one directory level deeper).
- **Hyperlink to Root `index.html`**:
  - Original: `href="index.html"`
  - Transformed: `href="../index.html"` (second_brain: 293, 304; vocal_remover: 369, 377; youtube_downloader: 550, 558)

### 4. Files Moving into `pages/` (`cute_quiz.html`, `present_agy_cli.html`, `website_design.html`, `main.html`)
- Location changes from `root` to `pages/` (one directory level deeper).
- **Hyperlinks to Root `index.html`**:
  - Original: `href="index.html"` -> `href="../index.html"` (cute_quiz: 391; present_agy_cli: 270; website_design: 807, 817)
- **`pages/website_design.html` (Theme gallery cards & JS data array)**:
  - JS Array data (`style_01_glassmorphic.html` .. `style_10_hacker_terminal.html`):
    - Original: `'style_01_glassmorphic.html'` .. `'style_10_hacker_terminal.html'`
    - Transformed: `'../themes/style_01_glassmorphic.html'` .. `'../themes/style_10_hacker_terminal.html'` (Lines 889, 930, 971, 1007, 1045, 1079, 1113, 1147, 1190, 1225)
- **`pages/main.html` (Trading Dashboard & Reports navigation)**:
  - Self-references (`main.html`): `href="main.html"` -> `href="main.html"` (remains relative within `pages/`, lines 298, 306)
  - Links to Reports (`reports/*.html`): `href="reports/*.html"` -> `href="../reports/*.html"` (Lines 307-311, 362, 391, 420, 449)
  - Image references (`assets/images/*.png`): `src="assets/images/*.png"` -> `src="../assets/images/*.png"` (Lines 341, 370, 399, 428)

### 5. Files Remaining in `reports/` (`gold-high-profit.html`, `gold-small-account.html`, `market-monitor.html`, `us100-daytrade.html`, `vp-breakout.html`)
- HTML files remain inside `reports/` directory.
- **Navigation Links Back to `main.html`**:
  - Original: `href="../main.html"` (points to old root `main.html`)
  - Transformed: `href="../pages/main.html"` (MUST update to new location in `pages/`!)
- **Sibling Report Links** (`vp-breakout.html`, `gold-high-profit.html`, etc.):
  - Unchanged (`vp-breakout.html`, `gold-high-profit.html`, etc.)
- **Asset Image References** (`../assets/images/*.png`):
  - Unchanged (`../assets/images/*.png`) because relative depth from `reports/` to `assets/` remains identical.

---

## Verification Strategy & Invalidation Conditions

1. **Static Link Verification**: Check every `<a href>`, `<img src>`, `<script src>`, `<link href>`, and JS string literal in the codebase using Python regex parser to ensure 0 references point to non-existent paths.
2. **Local HTTP Server Test**: Launch `python3 -m http.server` and test navigation between root `index.html`, `themes/*`, `apps/*`, `pages/*`, and `reports/*`.
3. **Invalidation Conditions**: Any remaining relative path starting with `style_*.html` in root index without `themes/` prefix, or `../main.html` in reports without `../pages/main.html`.