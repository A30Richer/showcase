# Handoff Report — Explorer Survey 2

## 1. Observation
Across `/root/ai-workspace/test/dashboard/showcase`, an exhaustive automated link survey inspected 26 HTML files.
Full survey raw data is preserved in `.agents/explorer_survey_2/full_survey.json` and documented in `.agents/explorer_survey_2/analysis.md`.

Direct findings by file category:
1. **Root HTML File (`index.html`)**:
   - Contains 23 relative hyperlinks in `<a href="...">` pointing to HTML files currently in root:
     - Pages: `main.html` (L522), `present_agy_cli.html` (L558), `cute_quiz.html` (L578), `love_counter.html` (L596), `website_design.html` (L709).
     - Apps: `second_brain.html` (L614), `youtube_downloader.html` (L653), `vocal_remover.html` (L671), `shop_vouchers.html` (L689).
     - Themes: `style_01_glassmorphic.html` through `style_10_hacker_terminal.html` (L727, L745, L763, L781, L799, L817, L835, L853, L871, L889).
     - Reports: `reports/market-monitor.html` (L484), `reports/vp-breakout.html` (L502), `reports/gold-small-account.html` (L540).

2. **Themes HTML Files (`style_01_glassmorphic.html` .. `style_10_hacker_terminal.html`)**:
   - Each of the 10 theme files contains 2 back navigation links: `<a href="website_design.html">` (e.g. style_01 L369 & L376; style_02 L327 & L334; style_03 L179 & L183, etc.).

3. **Apps HTML Files (`second_brain.html`, `vocal_remover.html`, `youtube_downloader.html`, `shop_vouchers.html`)**:
   - `second_brain.html` (L293, L304), `vocal_remover.html` (L369, L377), `youtube_downloader.html` (L550, L558) contain back links `<a href="index.html">`.
   - `shop_vouchers.html` contains dynamic JS template string `${shop.avatar}` (L1241).

4. **Pages HTML Files (`cute_quiz.html`, `love_counter.html`, `present_agy_cli.html`, `website_design.html`, `main.html`)**:
   - `cute_quiz.html` (L391) & `present_agy_cli.html` (L270) contain `<a href="index.html">`.
   - `love_counter.html` has 0 internal relative links.
   - `website_design.html` contains `<a href="index.html">` (L807, L817) and JavaScript array string literals `'style_01_glassmorphic.html'` through `'style_10_hacker_terminal.html'` (L889, L930, L971, L1007, L1045, L1079, L1113, L1147, L1190, L1225).
   - `main.html` contains self-links `main.html` (L298, L306), report links `reports/*.html` (L307-L311, L362, L391, L420, L449), and asset image links `assets/images/*.png` (L341, L370, L399, L428).

5. **Reports HTML Files (`reports/gold-high-profit.html`, `reports/gold-small-account.html`, `reports/market-monitor.html`, `reports/us100-daytrade.html`, `reports/vp-breakout.html`)**:
   - All 5 report files contain back links `<a href="../main.html">` (e.g. gold-high-profit L50, L56, L67).
   - Sibling report links `vp-breakout.html`, etc. stay within `reports/`.
   - Asset image references `../assets/images/*.png` stay relative from `reports/`.

6. **Standalone Subdirectory (`website-design/index.html`)**:
   - Contains 0 relative links to root files.

---

## 2. Logic Chain
1. Moving `style_01_...` through `style_10_...` into `themes/` increases their directory depth by 1 level (`themes/`). Therefore, any reference to `website_design.html` (which is moving to `pages/website_design.html`) must change from `website_design.html` to `../pages/website_design.html`.
2. Moving `youtube_downloader.html`, `vocal_remover.html`, `second_brain.html`, `shop_vouchers.html` into `apps/` increases their directory depth by 1 level (`apps/`). Any reference to `index.html` must change from `index.html` to `../index.html`.
3. Moving `cute_quiz.html`, `present_agy_cli.html`, `website_design.html`, `main.html` into `pages/` increases their directory depth by 1 level (`pages/`).
   - `index.html` references must change to `../index.html`.
   - Theme references inside `website_design.html` (JS array `'style_01_...html'`) must change to `'../themes/style_01_...html'`.
   - In `main.html`, links to `reports/*` must change from `reports/*` to `../reports/*`, and links to `assets/images/*` must change to `../assets/images/*`.
4. Files remaining in `reports/` do not change position, but their target `main.html` has moved to `pages/main.html`. Thus, `<a href="../main.html">` inside all 5 report files MUST be updated to `<a href="../pages/main.html">`.
5. Root `index.html` stays at root, so references to files moving into `themes/`, `apps/`, and `pages/` must add directory prefixes (`themes/`, `apps/`, `pages/`).

---

## 3. Caveats
- No caveats. All 26 HTML files and their asset references were 100% parsed and accounted for.

---

## 4. Conclusion
Moving HTML showcase files into subdirectories (`themes/`, `apps/`, `pages/`) requires updates across 20 HTML files:
- 10 theme files in `themes/` update navigation to `../pages/website_design.html`.
- 4 app files in `apps/` update navigation to `../index.html`.
- 4 page files in `pages/` update navigation to `../index.html`, `../themes/style_*.html`, `../reports/*`, `../assets/images/*`.
- 5 report files in `reports/` update navigation to `../pages/main.html`.
- Root `index.html` updates 22 links to add `themes/`, `apps/`, and `pages/` prefixes.

A complete line-by-line transformation matrix is delivered in `/root/ai-workspace/test/dashboard/showcase/.agents/explorer_survey_2/analysis.md`.

---

## 5. Verification Method
1. Inspect `analysis.md` for exact line numbers and transformation rules.
2. Run automated link check after moving files:
   ```bash
   python3 -c "
   import glob, os, re
   # verify all href, src, and JS string relative links resolve to existing files on disk
   "
   ```
3. Invalidation condition: Any relative path link returning 404 or broken reference when opened in browser or checked via static analysis script.
