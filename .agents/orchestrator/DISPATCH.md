## 2026-07-28T14:26:47Z
You are the Project Orchestrator. Your working directory is /root/ai-workspace/test/dashboard/showcase/.agents/orchestrator.
The original request file is at /root/ai-workspace/test/dashboard/showcase/.agents/ORIGINAL_REQUEST.md.

Your objective is to carry out the user request completely:
1. Categorize HTML files in `dashboard/showcase/` into clean subdirectories:
   - `themes/`: `style_01_glassmorphic.html` through `style_10_hacker_terminal.html`
   - `apps/`: `youtube_downloader.html`, `vocal_remover.html`, `second_brain.html`, `shop_vouchers.html`
   - `pages/`: `cute_quiz.html`, `love_counter.html`, `present_agy_cli.html`, `website_design.html`, `main.html`
   - Root: Keep `index.html`, `assets/`, `reports/`, and category folders (`themes/`, `apps/`, `pages/`).
2. Inspect and update all internal relative links (`<a href="...">`, `<img src="...">`, `<script src="...">`, `<link rel="stylesheet">`) across all HTML files to reflect new paths.
3. Verify and update `sync_showcase.sh` (and any related scripts) so syncing works flawlessly.
4. Perform thorough verification and link auditing.
5. Maintain `/root/ai-workspace/test/dashboard/showcase/.agents/orchestrator/progress.md` and report when all milestones are finished.
