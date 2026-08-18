# Handoff Report — Adversarial Challenge of Milestone 3 Sync Script

## VERDICT: REQUEST_CHANGES ❌

---

## 1. Observation

- **Environment & Symlink Configuration**:
  - `SHOWCASE_SRC`: `/root/ai-workspace/test/dashboard/showcase`
  - `SHOWCASE_REPO`: `/root/ai-workspace/showcase`
  - Running `ls -ld /root/ai-workspace/test/dashboard/showcase` shows:
    `showcase -> /root/ai-workspace/showcase`
  - Running `python3 -c "import os; print(os.path.realpath('/root/ai-workspace/test/dashboard/showcase') == os.path.realpath('/root/ai-workspace/showcase'))"` returns `True`.

- **Empirical Stale File Pruning Failure**:
  - Test command:
    ```bash
    echo "<!-- stale root file -->" > /root/ai-workspace/showcase/stale_test.html
    bash /root/ai-workspace/test/sync_showcase.sh
    ```
  - Command output from `sync_showcase.sh`:
    ```
    🔄 Syncing dashboard/showcase to /root/ai-workspace/showcase ...
    ✅ Mirror sync complete. Pruned 0 stale file(s).
    📦 Committing and pushing to git@github.com:A30Richer/showcase.git ...
    [main 3ac420a] sync: update showcase files from dashboard
     6 files changed, 144 insertions(+)
     create mode 100644 .agents/challenger_m3_1/progress.md
     create mode 100644 .agents/challenger_m3_1/test_m3_sync.py
     create mode 100644 stale_test.html
    ✅ Pushed to GitHub Pages successfully!
    ```
  - Verification: `os.path.exists('/root/ai-workspace/showcase/stale_test.html')` returned `True` AFTER sync completed.
  - Result: `stale_test.html` was **NOT** pruned. Instead, `sync_showcase.sh` staged, committed, and pushed `stale_test.html` to `origin/main`.

- **Git Working Tree & Metadata Pollution**:
  - Running `git -C /root/ai-workspace/showcase status` reveals:
    ```
    Untracked files:
      .agents/challenger_m3_1/test_m3_sync.py
    ```
  - `sync_showcase.sh` line 15 defines `EXCLUDE_DIRS = {'.git', '.agents', '.gemini', '__pycache__'}` in Python, but line 76 runs `git add -A` inside `SHOWCASE_REPO`. Because `/root/ai-workspace/showcase/.gitignore` does NOT exclude `.agents` or `.gemini`, `git add -A` stages and commits internal `.agents/` directory contents into the Git repository and pushes them to GitHub Pages.

---

## 2. Logic Chain

1. **Observation**: `/root/ai-workspace/test/dashboard/showcase` is a symlink pointing to `/root/ai-workspace/showcase`.
2. **Inference**: The source directory (`SHOWCASE_SRC`) and target repository directory (`SHOWCASE_REPO`) resolve to the exact same physical directory on disk (`os.path.realpath(src) == os.path.realpath(dst)`).
3. **Observation**: In `sync_showcase.sh`, Pass 1 iterates `os.walk(src)`. Because `src` is symlinked to `dst`, any file created in `dst` (such as `stale_test.html`) immediately exists in `src`.
4. **Observation**: Pass 1 records all relative paths in `src` into `src_rel_files`. Therefore, `stale_test.html` is added to `src_rel_files`.
5. **Observation**: Pass 2 iterates `dst` and checks `if rel_path not in src_rel_files:`. Because `stale_test.html` was recorded in `src_rel_files` during Pass 1, Pass 2 evaluates this check to `False` and skips pruning.
6. **Inference**: Pruning can **NEVER** delete stale files as long as `SHOWCASE_SRC` is a symlink to `SHOWCASE_REPO`.
7. **Observation**: `sync_showcase.sh` proceeds to run `git add -A` in `SHOWCASE_REPO`. Because stale files are not pruned and `.agents` is not ignored in `.gitignore`, Git commits and pushes stale test files and agent workspace metadata to GitHub.
8. **Conclusion**: `sync_showcase.sh` fails Task Criterion 1 (automatic pruning of stale files), Task Criterion 2 (sync idempotency), and causes repository pollution. Milestone 3 MUST be rejected with `REQUEST_CHANGES`.

---

## 3. Caveats

- If `dashboard/showcase` is intended to be an actual separate directory rather than a symlink to `showcase`, the symlink must be replaced with physical source files or `sync_showcase.sh` / `.gitignore` must handle canonical path checking and ignore `.agents`.
- No other caveats.

---

## 4. Conclusion & Actionable Recommendations

**Verdict**: **REQUEST_CHANGES** ❌

### Failure Summary:
1. **Pruning Defect**: Creating dummy file `stale_test.html` in `/root/ai-workspace/showcase` followed by `sync_showcase.sh` results in `Pruned 0 stale file(s)`. The file is retained and committed to git.
2. **Symlink Alias Conflict**: `SHOWCASE_SRC` (`/root/ai-workspace/test/dashboard/showcase`) is a symlink to `SHOWCASE_REPO` (`/root/ai-workspace/showcase`), causing Python `os.walk` to treat target files as source files.
3. **Git Repository Pollution**: `sync_showcase.sh` executes `git add -A` in `SHOWCASE_REPO` without ignoring `.agents` in `.gitignore`, leading to internal agent metadata being committed to production Git history.

### Required Remediations for Worker/Implementer:
1. **Resolve Source vs Target Directory Structure**: Ensure `dashboard/showcase` is either a distinct directory or update `sync_showcase.sh` to prevent `src` and `dst` path aliasing.
2. **Fix Pruning Logic**: Verify that when a stale file (e.g. `stale_test.html`) is added to `/root/ai-workspace/showcase`, running `sync_showcase.sh` prunes it and reports `Pruned 1 stale file(s)`.
3. **Add `.agents` and `.gemini` to `.gitignore`**: Add `.agents/` and `.gemini/` to `/root/ai-workspace/showcase/.gitignore` so `git add -A` does not commit internal agent work files.

---

## 5. Verification Method

To independently verify this failure or re-verify after fixes:

```bash
# 1. Create a dummy stale file in showcase
echo "<!-- stale test -->" > /root/ai-workspace/showcase/stale_test.html

# 2. Execute sync script
bash /root/ai-workspace/test/sync_showcase.sh

# 3. Assert stale file is pruned (Must pass when fixed, currently FAILS)
python3 -c "
import os
assert not os.path.exists('/root/ai-workspace/showcase/stale_test.html'), 'FAILED: stale_test.html was not pruned!'
print('PASS: stale_test.html was pruned successfully!')
"
```

Invalidation condition: If `stale_test.html` remains in `/root/ai-workspace/showcase` after `sync_showcase.sh` runs.
