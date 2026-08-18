#!/usr/bin/env python3
"""
Adversarial Test Harness for Milestone 3 Sync Script (sync_showcase.sh)
"""
import os
import shutil
import subprocess
import sys

SHOWCASE_SRC = "/root/ai-workspace/test/dashboard/showcase"
SHOWCASE_DST = "/root/ai-workspace/showcase"
SYNC_SCRIPT = "/root/ai-workspace/test/sync_showcase.sh"

def run_sync():
    res = subprocess.run(["bash", SYNC_SCRIPT], capture_output=True, text=True)
    print("--- SYNC OUTPUT ---")
    print(res.stdout)
    if res.stderr:
        print("--- SYNC STDERR ---")
        print(res.stderr)
    return res

def test_stale_pruning():
    print("=== Test 1: Stale File & Folder Pruning ===")
    
    # 1. Create stale files
    stale_root = os.path.join(SHOWCASE_DST, "stale_test.html")
    stale_theme = os.path.join(SHOWCASE_DST, "themes", "stale_theme.html")
    stale_nested_dir = os.path.join(SHOWCASE_DST, "deep", "nested")
    stale_nested_file = os.path.join(stale_nested_dir, "stale_nested.html")
    
    os.makedirs(os.path.dirname(stale_theme), exist_ok=True)
    os.makedirs(stale_nested_dir, exist_ok=True)
    
    with open(stale_root, "w") as f:
        f.write("<!-- stale root file -->")
    with open(stale_theme, "w") as f:
        f.write("<!-- stale theme file -->")
    with open(stale_nested_file, "w") as f:
        f.write("<!-- stale nested file -->")

    print(f"Created stale files:\n  {stale_root}\n  {stale_theme}\n  {stale_nested_file}")

    # Run sync
    res = run_sync()
    assert res.returncode == 0, f"Sync script failed with return code {res.returncode}"

    # Verify stale files are pruned
    pruning_failed = []
    if os.path.exists(stale_root): pruning_failed.append(stale_root)
    if os.path.exists(stale_theme): pruning_failed.append(stale_theme)
    if os.path.exists(stale_nested_file): pruning_failed.append(stale_nested_file)
    if os.path.exists(os.path.join(SHOWCASE_DST, "deep")): pruning_failed.append("deep/")

    if pruning_failed:
        print(f"❌ PRUNING FAILED! Unpruned items: {pruning_failed}")
        # Clean up stale files
        for p in [stale_root, stale_theme, stale_nested_file]:
            if os.path.exists(p): os.remove(p)
        if os.path.exists(os.path.join(SHOWCASE_DST, "deep")):
            shutil.rmtree(os.path.join(SHOWCASE_DST, "deep"))
        sys.exit(1)
    else:
        print("✓ All stale files and empty directories pruned successfully!")

def main():
    test_stale_pruning()

if __name__ == "__main__":
    main()
