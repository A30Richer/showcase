# Handoff Report: Showcase Sync Script & Test Harness Survey

**From:** `explorer_survey_3`  
**To:** Orchestrator / Implementer  
**Date:** 2026-07-28  
**Working Directory:** `/root/ai-workspace/test/dashboard/showcase/.agents/explorer_survey_3`  

---

## 1. Observation

### Observation 1: `sync_showcase.sh` Code & Location
- **File Location**: `/root/ai-workspace/test/sync_showcase.sh` (Line 1 to 42)
- **Source Directory**: `/root/ai-workspace/test/dashboard/showcase` (Line 5: `SHOWCASE_SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/dashboard/showcase" && pwd)"`)
- **Target Repository**: `/root/ai-workspace/showcase` (Line 6: `SHOWCASE_REPO="/root/ai-workspace/showcase"`)
- **Exclusion Logic**: Line 17-18: `if rel == '.git' or rel.startswith('.git/'): continue`
- **Copy Logic**: Line 24-25: `if not (os.path.exists(d_file) and os.path.samefile(s_file, d_file)): shutil.copy2(s_file, d_file)`
- **Deletion Logic**: Absent. No code exists to remove files in `$SHOWCASE_REPO` that are absent in `$SHOWCASE_SRC`.

### Observation 2: System Tool Availability
- Executed `which rsync` via `run_command`.
- **Result**: Command exited with code `0`, output: `rsync not found`.

### Observation 3: Current Target Repo Contents (`/root/ai-workspace/showcase`)
- Listing `/root/ai-workspace/showcase` shows root-level files matching `/root/ai-workspace/test/dashboard/showcase`, including `.agents/` and `.gemini/` directories.

### Observation 4: Test Infrastructure Audit
- Inspected `/root/ai-workspace/test/tests/` directory: contains 7 python test files (`test_bot_dashboard_fixes.py`, `test_ea_correctness.py`, `test_market_news_elliott_regressions.py`, `test_optimization.py`, `test_regressions.py`, `test_reporting_utils.py`, `test_shop_voucher_monitor.py`).
- No HTML link verification scripts, showcase validators, or layout compliance auditors exist in the project repository.

---

## 2. Logic Chain

1. **Premise 1 (from Obs 1 & Obs 3)**: `sync_showcase.sh` uses `os.walk(src)` to copy files from `src` to `dst`. It only excludes `.git`.
2. **Premise 2 (from Obs 1)**: Moving 19 HTML files into `themes/`, `apps/`, and `pages/` will create new target files in `dst/themes/`, `dst/apps/`, `dst/pages/`.
3. **Deduction 1 (from Premise 1 & 2)**: Because `sync_showcase.sh` contains no deletion/pruning logic, the original 19 HTML files located at the root of `dst` (`/root/ai-workspace/showcase`) will not be deleted by `sync_showcase.sh`.
4. **Deduction 2 (from Premise 1 & Obs 3)**: `.agents/` and `.gemini/` will continue to be copied to the deployment target repository unless explicitly added to an exclusion filter.
5. **Premise 3 (from Obs 2)**: Because `rsync` is not installed on the system, mirror sync with deletion cannot rely on `rsync --delete`.
6. **Deduction 3 (from Premise 3)**: Mirror sync and stale file pruning must be implemented in Python within `sync_showcase.sh` using two-pass traversal (`os.walk` + `os.remove`).
7. **Premise 4 (from Obs 4)**: Requirement R2 mandates a 100% pass on automated link audit, and R3 mandates seamless sync compatibility. However, zero link auditor scripts currently exist in the codebase.
8. **Deduction 4 (from Premise 4)**: A new Python script (e.g. `verify_showcase.py`) must be created to parse all HTML files, validate relative href/src targets, check directory layout, and test post-sync repository state.

---

## 3. Caveats

- **Git Remote Authentication**: `sync_showcase.sh` contains `git push origin main` to `git@github.com:A30Richer/showcase.git`. Local execution in offline environment may fail at `git push` if SSH keys/network are unavailable, but local staging (`git add -A` and `git commit`) will function normally.
- **Dynamic JS Asset Paths**: HTML files might contain dynamic asset loadings via JavaScript strings. Link auditor should focus on standard HTML attributes (`href`, `src`, `srcset`).

---

## 4. Conclusion

1. `sync_showcase.sh` requires an update to implement a two-pass Python mirror sync (copying valid files and pruning stale files/empty directories) and to exclude `.agents` and `.gemini`.
2. A new Python verification harness (`verify_showcase.py`) is required to perform 100% automated link auditing and layout verification for R1, R2, and R3 compliance.

---

## 5. Verification Method

### How to Verify Findings Independently:

1. **Verify Sync Script Location & Behavior**:
   ```bash
   cat /root/ai-workspace/test/sync_showcase.sh
   ```
   Inspect lines 15-26 to confirm absence of pruning logic and presence of only `.git` exclusion.

2. **Verify System `rsync` Tool**:
   ```bash
   which rsync || echo "rsync not found"
   ```
   Confirm that `rsync` is not installed on the host system.

3. **Verify Absence of Link Auditor**:
   ```bash
   find /root/ai-workspace/test -name "*link*" -o -name "*audit*" -o -name "*showcase*.py"
   ```
   Confirm that no link auditing tools exist prior to implementation.

4. **Post-Implementation Verification Command**:
   After implementer updates `sync_showcase.sh` and creates `verify_showcase.py`:
   ```bash
   python3 /root/ai-workspace/test/dashboard/showcase/verify_showcase.py
   bash /root/ai-workspace/test/sync_showcase.sh
   ```

