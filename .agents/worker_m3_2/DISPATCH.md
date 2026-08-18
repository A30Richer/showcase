## 2026-07-28T14:45:51Z
You are Worker M3 (Iteration 2) (teamwork_preview_worker).
Your working directory is /root/ai-workspace/test/dashboard/showcase/.agents/worker_m3_2.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

MANDATORY INSTRUCTIONS:
1. Read /root/ai-workspace/test/dashboard/showcase/.agents/ORIGINAL_REQUEST.md and /root/ai-workspace/test/dashboard/showcase/PROJECT.md first.
2. Read the Explorer M3 Fix remediation strategy at /root/ai-workspace/test/dashboard/showcase/.agents/explorer_m3_fix/handoff.md.

Task: Implement Milestone 3 Remediation to fix symlink path aliasing defect and git metadata leak.
1. Unlink `/root/ai-workspace/test/dashboard/showcase` (remove symlink: `rm /root/ai-workspace/test/dashboard/showcase`).
2. Create physical source directory `/root/ai-workspace/test/dashboard/showcase` and populate it with canonical contents from `/root/ai-workspace/showcase` (`index.html`, `themes/`, `apps/`, `pages/`, `assets/`, `reports/`, `PROJECT.md`, `.agents/`, `.gemini/` if present).
3. Update `.gitignore` in both `/root/ai-workspace/showcase/.gitignore` and `/root/ai-workspace/test/dashboard/showcase/.gitignore` to ignore `.agents/`, `.gemini/`, and `*.tmp`.
4. Untrack cached `.agents/` and `.gemini/` from Git in `/root/ai-workspace/showcase`:
   `git -C /root/ai-workspace/showcase rm -r --cached .agents .gemini 2>/dev/null || true`
   `git -C /root/ai-workspace/showcase rm --cached stale_test.html stale_test_2.tmp 2>/dev/null || true`
   Remove any physical stale files: `rm -f /root/ai-workspace/showcase/stale_test.html /root/ai-workspace/showcase/stale_test_2.tmp`
5. Update `/root/ai-workspace/test/sync_showcase.sh` to include a safeguard asserting `os.path.realpath(src) != os.path.realpath(dst)` before starting sync.
6. Run `bash /root/ai-workspace/test/sync_showcase.sh` and verify:
   - Symlink path aliasing is resolved (`os.path.realpath(src) != os.path.realpath(dst)`).
   - Stale file pruning works (test creating a dummy stale file in `/root/ai-workspace/showcase` and running sync_showcase.sh — verify it is pruned).
   - Git status is clean and `.agents/` or `.gemini/` metadata are NOT staged or committed to GitHub.
7. Write your execution report and verification results to /root/ai-workspace/test/dashboard/showcase/.agents/worker_m3_2/handoff.md and notify the orchestrator.
