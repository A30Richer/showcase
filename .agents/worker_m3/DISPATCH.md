## 2026-07-28T14:37:49Z
Task — Milestone 3: Sync Script Compatibility & Mirroring
Script to update: /root/ai-workspace/test/sync_showcase.sh

Instructions:
1. Update /root/ai-workspace/test/sync_showcase.sh:
   - Expand exclusion patterns to ignore `.git`, `.agents`, `.gemini` (and any subpaths).
   - Implement a robust two-pass Python mirror sync algorithm:
     - Pass 1 (Copy/Update): Walk source `/root/ai-workspace/test/dashboard/showcase` and copy new or updated files to `/root/ai-workspace/showcase`.
     - Pass 2 (Prune/Clean): Walk target `/root/ai-workspace/showcase` and remove any files or empty directories that no longer exist in source (eliminating stale root HTML files from pre-reorganization).
2. Execute `/root/ai-workspace/test/sync_showcase.sh` (or `bash /root/ai-workspace/test/sync_showcase.sh`) to perform sync.
3. Verify that `/root/ai-workspace/showcase` matches `/root/ai-workspace/test/dashboard/showcase` structure cleanly:
   - Root contains only `index.html`, `assets/`, `reports/`, `themes/`, `apps/`, `pages/` (and `.git`).
   - `themes/` contains 10 files, `apps/` contains 4 files, `pages/` contains 5 files.
   - Stale loose HTML files at root of `/root/ai-workspace/showcase` are removed.
4. Record changes in /root/ai-workspace/test/dashboard/showcase/.agents/worker_m3/changes.md and write your handoff report to /root/ai-workspace/test/dashboard/showcase/.agents/worker_m3/handoff.md. Send a message to the orchestrator when finished.
