# Showcase Reorganization Survey 3: Synchronization Script & Test Harness Analysis

**Target Project:** `/root/ai-workspace/test/dashboard/showcase`  
**Target Repository:** `/root/ai-workspace/showcase`  
**Script Under Investigation:** `/root/ai-workspace/test/sync_showcase.sh`  
**Date:** 2026-07-28  
**Agent:** `explorer_survey_3` (Read-Only Investigator)  

---

## Executive Summary

An in-depth technical investigation was conducted on `sync_showcase.sh` and related deployment/verification infrastructure in `/root/ai-workspace/test` and `/root/ai-workspace/showcase`.

### Key Discoveries:
1. **Script Location & Structure**: `sync_showcase.sh` is located at `/root/ai-workspace/test/sync_showcase.sh`. It uses a Bash wrapper around an inline Python script (`python3 -c "..."`) to copy files from `/root/ai-workspace/test/dashboard/showcase` (`$SHOWCASE_SRC`) to `/root/ai-workspace/showcase` (`$SHOWCASE_REPO`), followed by automated Git staging (`git add -A`), commit, and push to GitHub (`git@github.com:A30Richer/showcase.git`).
2. **System Dependency Constraint**: `rsync` is **not installed** on the system (`which rsync` returned non-zero code). Synchronization must rely entirely on Python standard library (`os`, `shutil`).
3. **Critical Sync Script Flaws**:
   - **No Deletion / Mirror Logic**: `sync_showcase.sh` currently only copies files from source to destination. When HTML files are moved into `themes/`, `apps/`, and `pages/`, the old HTML files at the root of `/root/ai-workspace/showcase` will remain as stale orphaned duplicates.
   - **Metadata Leakage**: The current exclusion filter only excludes `.git`. Internal metadata directories such as `.agents/` and `.gemini/` are currently copied over into the public showcase repository.
4. **Absence of Link Audit / Verification Harness**: No link auditing, HTML verification, or showcase test scripts currently exist in the repository. A dedicated Python verification harness (`verify_showcase.py` or similar) is required to validate 100% link integrity and layout compliance before and after running `sync_showcase.sh`.

---

## 1. `sync_showcase.sh` Deep Dive & Architecture

### 1.1 File Location & Path Resolution
- **File Path**: `/root/ai-workspace/test/sync_showcase.sh`
- **Source Path (`SHOWCASE_SRC`)**: `$(cd "$(dirname "${BASH_SOURCE[0]}")/dashboard/showcase" && pwd)` -> `/root/ai-workspace/test/dashboard/showcase`
- **Destination Path (`SHOWCASE_REPO`)**: `/root/ai-workspace/showcase`

### 1.2 Full Code Inspection
```bash
#!/usr/bin/env bash
# Helper script to sync dashboard/showcase to standalone showcase repository & push to GitHub Pages
set -e

SHOWCASE_SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/dashboard/showcase" && pwd)"
SHOWCASE_REPO="/root/ai-workspace/showcase"

echo "🔄 Syncing dashboard/showcase to $SHOWCASE_REPO ..."
python3 -c "
import os, shutil

src = '$SHOWCASE_SRC'
dst = '$SHOWCASE_REPO'

for root, dirs, files in os.walk(src):
    rel = os.path.relpath(root, src)
    if rel == '.git' or rel.startswith('.git/'):
        continue
    target_dir = os.path.join(dst, rel) if rel != '.' else dst
    os.makedirs(target_dir, exist_ok=True)
    for f in files:
        s_file = os.path.join(root, f)
        d_file = os.path.join(target_dir, f)
        if not (os.path.exists(d_file) and os.path.samefile(s_file, d_file)):
            shutil.copy2(s_file, d_file)
"

if [ -d "$SHOWCASE_REPO/.git" ]; then
    echo "📦 Committing and pushing to git@github.com:A30Richer/showcase.git ..."
    cd "$SHOWCASE_REPO"
    git add -A
    if ! git diff --cached --quiet; then
        git commit -m "sync: update showcase files from dashboard"
        git push origin main
        echo "✅ Pushed to GitHub Pages successfully!"
    else
        echo "ℹ️ No changes in showcase repo."
    fi
else
    echo "⚠️ Showcase git repository not found at $SHOWCASE_REPO"
fi
```

### 1.3 Detailed Analysis of Sync Logic

| Component | Implementation | Assessment & Defect Identification |
|---|---|---|
| **Interpreter** | `#!/usr/bin/env bash` with `set -e` | Standard error handling for shell execution. |
| **Directory Traversal** | Python `os.walk(src)` | Recursively visits all subdirectories in `$SHOWCASE_SRC`. |
| **Exclusions** | `if rel == '.git' or rel.startswith('.git/'): continue` | **Defect**: Only filters out `.git`. Does NOT filter out `.agents/` or `.gemini/`. |
| **Copy Decision** | `if not (os.path.exists(d_file) and os.path.samefile(s_file, d_file))` | Uses `shutil.copy2` to preserve file timestamps/metadata. `os.path.samefile` avoids copying if target is hard-linked or identical path. |
| **Deletion / Pruning** | *None* | **Critical Defect**: Missing mirror / orphan cleanup. Files removed or relocated in `src` remain untouched in `dst`. |
| **Git Deployment** | `git add -A`, `git diff --cached --quiet`, `git commit`, `git push origin main` | Automates staging and pushing to remote repo `git@github.com:A30Richer/showcase.git` when changes are detected. |

### 1.4 System Dependencies Check
- **`bash`**: Available.
- **`python3`** (standard libraries `os`, `shutil`): Available (Python 3.10+).
- **`git`**: Available.
- **`rsync`**: **NOT INSTALLED** (`which rsync` failed with exit code 127). All directory mirroring must be implemented in Python.

---

## 2. Required Updates for `sync_showcase.sh`

### 2.1 Problem Identification: Layout Migration Impact
When the 19 scattered root HTML files are relocated into their respective subdirectories:
- `themes/` (10 files: `style_01_glassmorphic.html` .. `style_10_hacker_terminal.html`)
- `apps/` (4 files: `youtube_downloader.html`, `vocal_remover.html`, `second_brain.html`, `shop_vouchers.html`)
- `pages/` (5 files: `cute_quiz.html`, `love_counter.html`, `present_agy_cli.html`, `website_design.html`, `main.html`)

Running the current `sync_showcase.sh` will yield the following flawed outcome:
1. `os.walk(src)` will copy the new files into `$SHOWCASE_REPO/themes/`, `$SHOWCASE_REPO/apps/`, and `$SHOWCASE_REPO/pages/`.
2. The existing copies of these 19 HTML files at `$SHOWCASE_REPO/` (root) will **NOT** be deleted.
3. `/root/ai-workspace/showcase` will contain 38 HTML files (19 at root + 19 in subfolders), leading to dirty deployment, duplicate routes, and risk of masking broken links.
4. `.agents/` and `.gemini/` will continue to be synced to the target repo.

### 2.2 Required Modifications for `sync_showcase.sh`

1. **Explicit Ignore List**: Filter out internal metadata folders (`.git`, `.agents`, `.gemini`, `__pycache__`, `.DS_Store`).
2. **Two-Pass Mirror Sync with Stale File Cleanup**:
   - **Pass 1 (Copy/Update)**: Copy all valid files from `src` to `dst`, maintaining a set `src_files` of relative paths copied.
   - **Pass 2 (Prune Stale Files)**: Walk `dst`. For any file not present in `src_files` (and not part of `.git` or `.github`), delete it from `dst`.
3. **Empty Directory Pruning**: Remove subdirectories in `dst` that become empty after pruning stale files.
4. **Enhanced Console Logging**: Output explicit feedback regarding copied, updated, and pruned files.

### 2.3 Proposed Implementation Code for `sync_showcase.sh`

```bash
#!/usr/bin/env bash
# Helper script to sync dashboard/showcase to standalone showcase repository & push to GitHub Pages
set -e

SHOWCASE_SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/dashboard/showcase" && pwd)"
SHOWCASE_REPO="/root/ai-workspace/showcase"

echo "🔄 Syncing dashboard/showcase to $SHOWCASE_REPO ..."
python3 -c "
import os, shutil

src = '$SHOWCASE_SRC'
dst = '$SHOWCASE_REPO'

EXCLUDE_DIRS = {'.git', '.agents', '.gemini', '__pycache__'}
EXCLUDE_FILES = {'.DS_Store'}

# Pass 1: Copy/update files from src to dst and record all valid relative file paths
src_rel_files = set()

for root, dirs, files in os.walk(src):
    # Exclude unwanted directories in-place
    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
    
    rel = os.path.relpath(root, src)
    target_dir = os.path.join(dst, rel) if rel != '.' else dst
    os.makedirs(target_dir, exist_ok=True)
    
    for f in files:
        if f in EXCLUDE_FILES:
            continue
        s_file = os.path.join(root, f)
        d_file = os.path.join(target_dir, f)
        
        rel_path = os.path.normpath(os.path.join(rel, f)) if rel != '.' else f
        src_rel_files.add(rel_path)
        
        if not (os.path.exists(d_file) and os.path.samefile(s_file, d_file)):
            shutil.copy2(s_file, d_file)

# Pass 2: Prune stale files from dst that no longer exist in src
pruned_count = 0
for root, dirs, files in os.walk(dst, topdown=False):
    rel = os.path.relpath(root, dst)
    
    # Skip git and github workflow directories
    if rel == '.git' or rel.startswith('.git/') or rel == '.github' or rel.startswith('.github/'):
        continue
    if any(part in EXCLUDE_DIRS for part in rel.split(os.sep)):
        continue

    for f in files:
        rel_path = os.path.normpath(os.path.join(rel, f)) if rel != '.' else f
        if rel_path not in src_rel_files:
            d_file = os.path.join(root, f)
            os.remove(d_file)
            print(f'  🗑️ Removed stale file from showcase target: {rel_path}')
            pruned_count += 1

    # Remove empty directories (except dst root)
    if root != dst and not os.listdir(root):
        os.rmdir(root)
        print(f'  🗑️ Removed empty directory: {rel}')

print(f'✅ Mirror sync complete. Pruned {pruned_count} stale file(s).')
"

if [ -d "$SHOWCASE_REPO/.git" ]; then
    echo "📦 Committing and pushing to git@github.com:A30Richer/showcase.git ..."
    cd "$SHOWCASE_REPO"
    git add -A
    if ! git diff --cached --quiet; then
        git commit -m "sync: update showcase files from dashboard"
        git push origin main
        echo "✅ Pushed to GitHub Pages successfully!"
    else
        echo "ℹ️ No changes in showcase repo."
    fi
else
    echo "⚠️ Showcase git repository not found at $SHOWCASE_REPO"
fi
```

---

## 3. Test Harness & Verification Script Analysis

### 3.1 Audit of Existing Test Infrastructure
- **Search Scope**: Entire `/root/ai-workspace/test` workspace including `tests/` directory.
- **Existing Test Files**:
  - `tests/test_bot_dashboard_fixes.py`
  - `tests/test_ea_correctness.py`
  - `tests/test_market_news_elliott_regressions.py`
  - `tests/test_optimization.py`
  - `tests/test_regressions.py`
  - `tests/test_reporting_utils.py`
  - `tests/test_shop_voucher_monitor.py`
- **Result**: All existing test scripts focus exclusively on trading bot strategies, EA correctness, and market monitor logic. **Zero** test scripts or link auditor harnesses exist for the `showcase` web presentation hub.

### 3.2 Required Verification Script Specification
To fulfill Acceptance Criteria R1, R2, and R3, an automated Python test script (e.g., `verify_showcase.py`) must be created.

#### Functional Requirements for `verify_showcase.py`:

1. **Directory Structure Verification (R1 Compliance)**:
   - Check that `themes/` exists and contains exactly 10 style files (`style_01_glassmorphic.html` through `style_10_hacker_terminal.html`).
   - Check that `apps/` exists and contains exactly 4 application files (`youtube_downloader.html`, `vocal_remover.html`, `second_brain.html`, `shop_vouchers.html`).
   - Check that `pages/` exists and contains exactly 5 interactive files (`cute_quiz.html`, `love_counter.html`, `present_agy_cli.html`, `website_design.html`, `main.html`).
   - Check that `index.html` remains at the root of `dashboard/showcase`.
   - Check that no migrated HTML files remain at the root of `dashboard/showcase`.

2. **Automated Relative Link & Asset Audit (R2 Compliance)**:
   - Parse all `.html` files in `dashboard/showcase/` (including subdirectories `themes/`, `apps/`, `pages/`, `reports/`).
   - Extract attributes: `<a href>`, `<img src>`, `<script src>`, `<link rel="stylesheet" href>`, `<iframe src>`, `<source src>`.
   - Ignore external/special links (`http://`, `https://`, `#`, `mailto:`, `javascript:`, `tel:`).
   - Normalize target paths (strip query strings `?v=1` or hash fragments `#section`).
   - Resolve relative target paths against the HTML file's directory.
   - Assert file existence on disk (case-sensitive).
   - Output clear pass/fail status per file and overall 100% pass metric.

3. **Sync Script & Mirror Parity Audit (R3 Compliance)**:
   - Execute `sync_showcase.sh`.
   - Verify that `/root/ai-workspace/showcase` matches `/root/ai-workspace/test/dashboard/showcase` structure.
   - Confirm no stale files exist at `/root/ai-workspace/showcase` root.
   - Confirm `.agents/` and `.gemini/` are excluded from `/root/ai-workspace/showcase`.

---

## 4. Implementation Recommendations & Handoff Plan

| Task Area | Recommended Action | Priority |
|---|---|---|
| **Sync Script** | Update `/root/ai-workspace/test/sync_showcase.sh` with two-pass mirror cleanup and `.agents`/`.gemini` exclusions. | **High** |
| **Verification Harness** | Create a standalone test script `verify_showcase.py` under `/root/ai-workspace/test/tests/` or `/root/ai-workspace/test/dashboard/showcase/`. | **High** |
| **Execution Order** | 1. Implement directory moves (`themes/`, `apps/`, `pages/`) & update relative paths in HTML.<br>2. Update `sync_showcase.sh`.<br>3. Run `verify_showcase.py`.<br>4. Run `sync_showcase.sh` to update target showcase repo. | **Sequential** |

