# Forensic Audit Report — Milestone 3 (Iteration 1)

## VERDICT: INTEGRITY VIOLATION / AUDIT VETO ❌

## Audit Findings & Evidence:
1. Symlink Path Aliasing Defect:
   - `/root/ai-workspace/test/dashboard/showcase` is a symbolic link pointing directly to `/root/ai-workspace/showcase` (`dashboard/showcase -> /root/ai-workspace/showcase`).
   - In `sync_showcase.sh`, `SHOWCASE_SRC` (`/root/ai-workspace/test/dashboard/showcase`) and `SHOWCASE_REPO` (`/root/ai-workspace/showcase`) resolve to the exact same physical directory (`/root/ai-workspace/showcase`).
   - Pass 1 `os.walk(src)` indexes all files in `/root/ai-workspace/showcase` (including stale files created in target), causing Pass 2 `if rel_path not in src_rel_files` to ALWAYS evaluate to `False`.
   - Empirical test: Adding a stale test file (`stale_test.html`) to `/root/ai-workspace/showcase` resulted in 0 files pruned (`Pruned 0 stale file(s)`). Instead of pruning, `sync_showcase.sh` staged, committed, and pushed `stale_test.html` to git.

2. Git Staging Leak of Internal Metadata:
   - `.agents/` and `.gemini/` metadata directories are staged by `git add -A` in `sync_showcase.sh` and pushed to GitHub unless ignored.
   - `/root/ai-workspace/showcase/.gitignore` does NOT exclude `.agents/` or `.gemini/`, leading to internal agent workspace metadata being committed to production Git repository.

## Required Remediations:
1. Fix symlink path aliasing defect so pruning works correctly (e.g. either restore `dashboard/showcase` as a physical directory containing source files or update `sync_showcase.sh` / prune logic to correctly detect and prune stale files in `/root/ai-workspace/showcase`).
2. Exclude `.agents/` and `.gemini/` from git staging (e.g., add `.agents` and `.gemini` to `/root/ai-workspace/showcase/.gitignore`).
