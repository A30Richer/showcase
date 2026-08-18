# Comprehensive Directory Survey & Categorization Analysis

**Target Directory:** `/root/ai-workspace/test/dashboard/showcase`  
**Date:** 2026-07-28  
**Agent:** explorer_survey_1 (Read-Only Investigator)  

---

## Executive Summary

A comprehensive survey of `/root/ai-workspace/test/dashboard/showcase` was conducted to prepare for directory structure reorganization as specified in `ORIGINAL_REQUEST.md`. Currently, 19 HTML files sit scattered in the root directory alongside `index.html`, 2 existing subdirectories (`assets/`, `reports/`), 1 unexpected directory (`website-design/`), and system/agent metadata directories (`.agents/`, `.gemini/`, `.git/`, `.github/`).

All 19 target HTML files were identified and mapped to their designated subdirectories (`themes/`, `apps/`, `pages/`). Key edge cases were identified, including link adjustments across HTML files, internal references to `main.html` from `reports/`, and the location of `sync_showcase.sh` at `/root/ai-workspace/test/sync_showcase.sh`.

---

## 1. Directory Structure & File Enumeration

### 1.1 Root Directory Contents (`/root/ai-workspace/test/dashboard/showcase`)

| Item Name | Type | Size (Bytes) | Category / Purpose |
|---|---|---|---|
| `index.html` | File | 42,944 | Main Portal Landing Page (Stays at Root) |
| `style_01_glassmorphic.html` | File | 19,221 | Theme Template -> Target: `themes/` |
| `style_02_neumorphic.html` | File | 16,095 | Theme Template -> Target: `themes/` |
| `style_03_cyberpunk.html` | File | 10,074 | Theme Template -> Target: `themes/` |
| `style_04_neobrutalism.html` | File | 10,851 | Theme Template -> Target: `themes/` |
| `style_05_clean_saas.html` | File | 12,200 | Theme Template -> Target: `themes/` |
| `style_06_synthwave.html` | File | 7,576 | Theme Template -> Target: `themes/` |
| `style_07_luxury_gold.html` | File | 7,485 | Theme Template -> Target: `themes/` |
| `style_08_bento_grid.html` | File | 7,594 | Theme Template -> Target: `themes/` |
| `style_09_claymorphism.html` | File | 6,407 | Theme Template -> Target: `themes/` |
| `style_10_hacker_terminal.html` | File | 8,134 | Theme Template -> Target: `themes/` |
| `youtube_downloader.html` | File | 29,179 | Web App Tool -> Target: `apps/` |
| `vocal_remover.html` | File | 15,282 | Web App Tool -> Target: `apps/` |
| `second_brain.html` | File | 18,253 | Web App Tool -> Target: `apps/` |
| `shop_vouchers.html` | File | 43,862 | Web App Tool -> Target: `apps/` |
| `cute_quiz.html` | File | 17,593 | Interactive Page -> Target: `pages/` |
| `love_counter.html` | File | 16,373 | Interactive Page -> Target: `pages/` |
| `present_agy_cli.html` | File | 25,470 | Interactive Page -> Target: `pages/` |
| `website_design.html` | File | 56,596 | Interactive Page -> Target: `pages/` |
| `main.html` | File | 13,920 | Interactive Page / EA Hub -> Target: `pages/` |
| `README.md` | File | 1,228 | Documentation (Stays at Root) |
| `SECURITY.md` | File | 530 | Security Policy (Stays at Root) |
| `.gitignore` | File | 90 | Git Ignore Configuration (Stays at Root) |
| `assets/` | Directory | N/A | Asset directory (Images) |
| `reports/` | Directory | N/A | Automated backtest & monitor reports |
| `website-design/` | Directory | N/A | Unexpected directory (Contains `index.html`) |
| `.agents/` | Directory | N/A | Agent framework metadata |
| `.gemini/` | Directory | N/A | System metadata |
| `.git/` | Directory | N/A | Git VCS repository |
| `.github/` | Directory | N/A | GitHub configuration |

### 1.2 Subdirectory Contents

#### `assets/images/` (6 image files)
- `gold_backtest_results.png` (133,071 B)
- `gold_micro_100_backtest_chart.png` (239,929 B)
- `us100_backtest_results.png` (123,036 B)
- `volume_profile_chart.png` (131,025 B)
- `vp_breakout_best_chart.png` (118,035 B)
- `vp_zones_chart.png` (167,895 B)

#### `reports/` (5 HTML report files)
- `gold-high-profit.html` (5,361 B)
- `gold-small-account.html` (16,662 B)
- `market-monitor.html` (5,161 B)
- `us100-daytrade.html` (5,359 B)
- `vp-breakout.html` (5,560 B)

#### `website-design/` (1 HTML file)
- `website-design/index.html` (46,856 B) — *Unexpected legacy file/folder*

---

## 2. Confirmation of Categorization Targets

Per `ORIGINAL_REQUEST.md`, the reorganization targets are verified as follows:

### 2.1 `themes/` (10 files)
- `style_01_glassmorphic.html` -> `themes/style_01_glassmorphic.html`
- `style_02_neumorphic.html` -> `themes/style_02_neumorphic.html`
- `style_03_cyberpunk.html` -> `themes/style_03_cyberpunk.html`
- `style_04_neobrutalism.html` -> `themes/style_04_neobrutalism.html`
- `style_05_clean_saas.html` -> `themes/style_05_clean_saas.html`
- `style_06_synthwave.html` -> `themes/style_06_synthwave.html`
- `style_07_luxury_gold.html` -> `themes/style_07_luxury_gold.html`
- `style_08_bento_grid.html` -> `themes/style_08_bento_grid.html`
- `style_09_claymorphism.html` -> `themes/style_09_claymorphism.html`
- `style_10_hacker_terminal.html` -> `themes/style_10_hacker_terminal.html`

### 2.2 `apps/` (4 files)
- `youtube_downloader.html` -> `apps/youtube_downloader.html`
- `vocal_remover.html` -> `apps/vocal_remover.html`
- `second_brain.html` -> `apps/second_brain.html`
- `shop_vouchers.html` -> `apps/shop_vouchers.html`

### 2.3 `pages/` (5 files)
- `cute_quiz.html` -> `pages/cute_quiz.html`
- `love_counter.html` -> `pages/love_counter.html`
- `present_agy_cli.html` -> `pages/present_agy_cli.html`
- `website_design.html` -> `pages/website_design.html`
- `main.html` -> `pages/main.html`

### 2.4 Root Level Items
- `index.html` (Main entry point)
- `assets/` (Asset images)
- `reports/` (Trading & backtest reports)
- `themes/` (New directory)
- `apps/` (New directory)
- `pages/` (New directory)
- `README.md`, `SECURITY.md`, `.gitignore`

---

## 3. Unexpected Files, Missing Files, and Edge Cases

### Edge Case 1: Legacy Directory `website-design/`
- **Observation:** Directory `website-design/` exists containing `website-design/index.html` (46,856 B).
- **Comparison:** Root file `website_design.html` (56,596 B) is actively linked by `index.html` (line 709) and all 10 `style_*.html` theme files.
- **Impact:** `website-design/index.html` is an unreferenced duplicate/older version of `website_design.html`.
- **Recommendation:** `website_design.html` must be moved to `pages/website_design.html` as requested. The directory `website-design/` can be archived or removed during implementation to keep root clean.

### Edge Case 2: Location of `sync_showcase.sh`
- **Observation:** `sync_showcase.sh` is located at `/root/ai-workspace/test/sync_showcase.sh` (one directory above `dashboard/showcase`).
- **Mechanism:** The script computes `SHOWCASE_SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/dashboard/showcase" && pwd)"` and executes Python `os.walk(src)` to copy all subdirectories and files recursively to `/root/ai-workspace/showcase`.
- **Impact:** Moving files into `themes/`, `apps/`, and `pages/` inside `dashboard/showcase` will automatically be preserved by `os.walk(src)`. No logic changes to `sync_showcase.sh` are required for directory traversal, but checking script execution after moving files is recommended.

### Edge Case 3: Required Link & Asset Path Updates

1. **Links inside root `index.html`**:
   - Lines 522 (`main.html`), 558 (`present_agy_cli.html`), 578 (`cute_quiz.html`), 596 (`love_counter.html`), 709 (`website_design.html`) -> Prefix with `pages/`
   - Lines 614 (`second_brain.html`), 653 (`youtube_downloader.html`), 671 (`vocal_remover.html`), 689 (`shop_vouchers.html`) -> Prefix with `apps/`
   - Lines 727-889 (`style_01_glassmorphic.html` through `style_10_hacker_terminal.html`) -> Prefix with `themes/`
   - Reports links (lines 484, 502, 540) remain `reports/*.html`.

2. **Links inside 10 Theme HTML files (`themes/style_01_...` to `themes/style_10_...`)**:
   - Currently contain `<a href="website_design.html">`
   - Must be updated to `<a href="../pages/website_design.html">`

3. **Links inside App HTML files (`apps/`)**:
   - `youtube_downloader.html` (lines 550, 558), `vocal_remover.html` (lines 369, 377), `second_brain.html` (lines 293, 304) contain `<a href="index.html">`
   - Must be updated to `<a href="../index.html">`

4. **Links inside Page HTML files (`pages/`)**:
   - `cute_quiz.html` (line 391), `present_agy_cli.html` (line 270), `website_design.html` (lines 807, 817) contain `<a href="index.html">` -> Update to `<a href="../index.html">`
   - `main.html`:
     - Links to `reports/*.html` (lines 307-311, 362) -> Update to `../reports/*.html`
     - Asset images `<img src="assets/images/...">` (lines 341, 374, 407, 440, 473) -> Update to `../assets/images/...`

5. **Links inside Report HTML files (`reports/*.html`)**:
   - `gold-high-profit.html` (lines 50, 56, 67), `gold-small-account.html` (lines 78, 84, 95), `market-monitor.html` (lines 49, 55, 66), `us100-daytrade.html` (lines 50, 56, 67), `vp-breakout.html` (lines 50, 56, 67) currently link to `../main.html`
   - Must be updated to `../pages/main.html`

---

## 4. Reorganization Summary Matrix

| Original Path | Target Path | Link Updates Required |
|---|---|---|
| `style_01_glassmorphic.html` ... `style_10_hacker_terminal.html` | `themes/style_01_...` - `themes/style_10_...` | Update `website_design.html` -> `../pages/website_design.html` |
| `youtube_downloader.html` | `apps/youtube_downloader.html` | Update `index.html` -> `../index.html` |
| `vocal_remover.html` | `apps/vocal_remover.html` | Update `index.html` -> `../index.html` |
| `second_brain.html` | `apps/second_brain.html` | Update `index.html` -> `../index.html` |
| `shop_vouchers.html` | `apps/shop_vouchers.html` | No internal relative page links present |
| `cute_quiz.html` | `pages/cute_quiz.html` | Update `index.html` -> `../index.html` |
| `love_counter.html` | `pages/love_counter.html` | Self-contained, no relative links |
| `present_agy_cli.html` | `pages/present_agy_cli.html` | Update `index.html` -> `../index.html` |
| `website_design.html` | `pages/website_design.html` | Update `index.html` -> `../index.html` |
| `main.html` | `pages/main.html` | Update `reports/*` -> `../reports/*`, `assets/images/*` -> `../assets/images/*` |
| `index.html` | `index.html` (Root) | Update all 19 links to include subfolder prefixes (`themes/`, `apps/`, `pages/`) |
| `reports/*.html` (5 files) | `reports/*.html` | Update `../main.html` -> `../pages/main.html` |
