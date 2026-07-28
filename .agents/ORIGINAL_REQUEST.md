# Original User Request

## 2026-07-28T14:26:36Z

Reorganize the `dashboard/showcase` directory structure to be clean, modular, and aesthetically structured. Move scattered HTML showcase pages into logical subfolders (`themes/`, `apps/`, `pages/`), preserve root `index.html`, update all relative hyperlinks/asset paths, and ensure the synchronization script works seamlessly.

Working directory: /root/ai-workspace/test/dashboard/showcase
Integrity mode: development

## Requirements

### R1. Logical Folder Structure & File Categorization
Categorize HTML files in `dashboard/showcase/` into clean subdirectories:
- `themes/`: Design style templates (`style_01_glassmorphic.html` through `style_10_hacker_terminal.html`).
- `apps/`: Web application tools (`youtube_downloader.html`, `vocal_remover.html`, `second_brain.html`, `shop_vouchers.html`).
- `pages/`: Interactive pages (`cute_quiz.html`, `love_counter.html`, `present_agy_cli.html`, `website_design.html`, `main.html`).
- Root: Keep `index.html`, `assets/`, `reports/`, and category folders (`themes/`, `apps/`, `pages/`).

### R2. Link & Asset Path Integrity
Inspect and update all internal relative links (`<a href="...">`, `<img src="...">`, `<script src="...">`, `<link rel="stylesheet">`) across all HTML files to reflect the new directory paths without breaking navigation.

### R3. Sync Script Compatibility
Verify and update `sync_showcase.sh` (or any related scripts) so syncing to `/root/ai-workspace/showcase` and GitHub Pages works flawlessly with the new clean directory layout.

## Acceptance Criteria

### Directory & Navigation Integrity
- [ ] Root of `dashboard/showcase` is clean with clear subdirectories (`themes/`, `apps/`, `pages/`, `assets/`, `reports/`) and root `index.html`.
- [ ] Automated relative link audit passes 100% with no 404 broken links or broken assets across all HTML files.
- [ ] `sync_showcase.sh` completes without errors and mirrors the organized structure cleanly.
