# Forensic Investigation & Remediation Strategy — Milestone 3 Fix

## Executive Summary
This report analyzes the root causes of the Milestone 3 sync script audit vetoes (symlink path aliasing defect and git staging leak of internal metadata) and presents a complete, verified remediation plan for Worker M3.

---

## 1. Observation

### 1.1 Symlink Path Aliasing Defect
- **Symlink Verification**:
  Command: `ls -ld /root/ai-workspace/test/dashboard/showcase`
  Result: `lrwxrwxrwx+ 1 root root 30 Jul 27 20:14 showcase -> /root/ai-workspace/showcase`
  Command: `python3 -c "import os; print(os.path.realpath('/root/ai-workspace/test/dashboard/showcase') == os.path.realpath('/root/ai-workspace/showcase'))"`
  Result: `True`
- **Sync Script Configuration (`/root/ai-workspace/test/sync_showcase.sh`)**:
  Line 5: `SHOWCASE_SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/dashboard/showcase" && pwd)"`
  Line 6: `SHOWCASE_REPO="/root/ai-workspace/showcase"`
  Line 12: `src = '$SHOWCASE_SRC'`
  Line 13: `dst = '$SHOWCASE_REPO'`
  Because `SHOWCASE_SRC` is a symlink to `SHOWCASE_REPO`, `src` and `dst` point to the exact same physical directory on disk (`/root/ai-workspace/showcase`).
- **Pruning Failure Behavior**:
  In Pass 1 (`for root, dirs, files in os.walk(src):`), `os.walk(src)` scans `/root/ai-workspace/showcase`. Any file created in `dst` (e.g. `stale_test.html` or `stale_test_2.tmp`) is immediately indexed in `src_rel_files`.
  In Pass 2 (`for root, dirs, files in os.walk(dst, topdown=False):`), `if rel_path not in src_rel_files:` evaluates to `False` for every file in `dst`.
  Result: Stale files are **never** deleted. `sync_showcase.sh` outputs `Pruned 0 stale file(s)`.

### 1.2 Git Staging Leak of Internal Metadata
- **Git Staging Mechanism**:
  In `sync_showcase.sh` (line 76): `git add -A` is run inside `SHOWCASE_REPO` (`/root/ai-workspace/showcase`).
- **Git Ignore Missing Rules**:
  Contents of `/root/ai-workspace/showcase/.gitignore`:
  ```gitignore
  # Ignore sensitive files
  .env*
  *.key
  *.pem

  # OS / Editor files
  .DS_Store
  .vscode/
  .idea/
  ```
  Neither `.agents/` nor `.gemini/` are excluded in `/root/ai-workspace/showcase/.gitignore`.
- **Observed Leak**:
  `git -C /root/ai-workspace/showcase log` shows recent commits containing:
  - `.agents/challenger_m3_1/handoff.md`
  - `.agents/reviewer_m3_1/handoff.md`
  - `.agents/challenger_m3_1/test_m3_sync.py`
  - `stale_test_2.tmp`
  Agent internal metadata and test artifacts were staged by `git add -A` and committed to GitHub Pages.

---

## 2. Logic Chain

1. **Observation 1.1**: `/root/ai-workspace/test/dashboard/showcase` is a symbolic link pointing directly to `/root/ai-workspace/showcase`.
2. **Inference**: Both `SHOWCASE_SRC` and `SHOWCASE_REPO` resolve to `/root/ai-workspace/showcase`. `src` and `dst` in `sync_showcase.sh` are identical physical paths.
3. **Inference**: Pass 1 of `sync_showcase.sh` populates `src_rel_files` with every file present in `/root/ai-workspace/showcase`.
4. **Inference**: Pass 2 checks if target files exist in `src_rel_files`. Since `src` IS `dst`, every file in target is found in `src_rel_files`. Therefore, stale file deletion is bypassed completely.
5. **Conclusion 1**: Mirror sync pruning cannot function as long as `dashboard/showcase` is a symlink to `/root/ai-workspace/showcase`. The symlink must be unlinked and replaced with an independent physical source directory `/root/ai-workspace/test/dashboard/showcase`.
6. **Observation 1.2**: `sync_showcase.sh` runs `git add -A` in `SHOWCASE_REPO`, while `.gitignore` in `SHOWCASE_REPO` lacks `.agents/` and `.gemini/`.
7. **Inference**: Any untracked or modified files in `.agents/` or `.gemini/` in `SHOWCASE_REPO` are automatically staged by git.
8. **Conclusion 2**: `.agents/` and `.gemini/` must be added to `/root/ai-workspace/showcase/.gitignore`, and cached metadata files must be removed from git index via `git rm -r --cached`.

---

## 3. Caveats

- **Existing Git History**: Commits containing `.agents/` metadata are already present in git history of `/root/ai-workspace/showcase`. Adding `.agents/` to `.gitignore` and running `git rm -r --cached .agents` will remove them from future commits, but existing git history remains unless rebased. (Untracking via `git rm --cached` is sufficient for repository clean-up).
- **Loose Files in Dashboard**: `/root/ai-workspace/test/dashboard/` contains loose HTML files (`style_01...`, `website_design.html`) left over from pre-reorganization. When setting up the physical `dashboard/showcase` directory, source files should be copied from `/root/ai-workspace/showcase` (which already has the clean reorganized structure `themes/`, `apps/`, `pages/`, `assets/`, `reports/`, `index.html`).

---

## 4. Remediation Strategy for Worker M3

### Step 1: Unlink and Create Physical Source Directory
1. Remove the symlink:
   `rm /root/ai-workspace/test/dashboard/showcase`
2. Create the physical source directory:
   `mkdir -p /root/ai-workspace/test/dashboard/showcase`
3. Copy canonical source contents from `/root/ai-workspace/showcase` to `/root/ai-workspace/test/dashboard/showcase`:
   ```bash
   cp -a /root/ai-workspace/showcase/index.html /root/ai-workspace/test/dashboard/showcase/
   cp -a /root/ai-workspace/showcase/themes /root/ai-workspace/test/dashboard/showcase/
   cp -a /root/ai-workspace/showcase/apps /root/ai-workspace/test/dashboard/showcase/
   cp -a /root/ai-workspace/showcase/pages /root/ai-workspace/test/dashboard/showcase/
   cp -a /root/ai-workspace/showcase/assets /root/ai-workspace/test/dashboard/showcase/
   cp -a /root/ai-workspace/showcase/reports /root/ai-workspace/test/dashboard/showcase/
   cp -a /root/ai-workspace/showcase/PROJECT.md /root/ai-workspace/test/dashboard/showcase/
   cp -a /root/ai-workspace/showcase/.agents /root/ai-workspace/test/dashboard/showcase/
   if [ -d /root/ai-workspace/showcase/.gemini ]; then
       cp -a /root/ai-workspace/showcase/.gemini /root/ai-workspace/test/dashboard/showcase/
   fi
   ```

### Step 2: Prevent Git Metadata Leak
1. Update `/root/ai-workspace/showcase/.gitignore` (and `/root/ai-workspace/test/dashboard/showcase/.gitignore`):
   ```gitignore
   # Ignore sensitive files
   .env*
   *.key
   *.pem

   # OS / Editor files
   .DS_Store
   .vscode/
   .idea/

   # Agent and CLI internal metadata
   .agents/
   .gemini/
   *.tmp
   ```
2. Remove cached `.agents/`, `.gemini/`, and stale files from showcase Git repository:
   ```bash
   git -C /root/ai-workspace/showcase rm -r --cached .agents .gemini 2>/dev/null || true
   git -C /root/ai-workspace/showcase rm --cached stale_test.html stale_test_2.tmp 2>/dev/null || true
   rm -f /root/ai-workspace/showcase/stale_test.html /root/ai-workspace/showcase/stale_test_2.tmp
   ```

### Step 3: Add Safeguards to `sync_showcase.sh`
Add path aliasing assertion at the start of Python sync in `/root/ai-workspace/test/sync_showcase.sh`:
```python
if os.path.realpath(src) == os.path.realpath(dst):
    raise RuntimeError(f"Symlink path aliasing defect: src ({src}) and dst ({dst}) resolve to the same path.")
```

---

## 5. Verification Method

To verify the fix independently:

```bash
# 1. Check symlink is gone and dashboard/showcase is a real directory
python3 -c "
import os
assert not os.path.islink('/root/ai-workspace/test/dashboard/showcase'), 'FAIL: dashboard/showcase is still a symlink!'
assert os.path.isdir('/root/ai-workspace/test/dashboard/showcase'), 'FAIL: dashboard/showcase is not a directory!'
assert os.path.realpath('/root/ai-workspace/test/dashboard/showcase') != os.path.realpath('/root/ai-workspace/showcase'), 'FAIL: src and dst realpaths are identical!'
print('PASS: Symlink path aliasing broken successfully!')
"

# 2. Test stale file pruning
echo "<!-- stale test file -->" > /root/ai-workspace/showcase/stale_test_m3.html
bash /root/ai-workspace/test/sync_showcase.sh

python3 -c "
import os
assert not os.path.exists('/root/ai-workspace/showcase/stale_test_m3.html'), 'FAIL: stale file was not pruned!'
print('PASS: Stale file pruned successfully!')
"

# 3. Check git staging leak prevention
git -C /root/ai-workspace/showcase status --porcelain | grep -E '\.agents|\.gemini' && echo "FAIL: Metadata leaked into git!" || echo "PASS: No metadata leaked into git!"
```
