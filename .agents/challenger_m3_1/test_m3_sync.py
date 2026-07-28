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

    # 2. Create git & github dummy files that MUST NOT be pruned
    git_dummy_dir = os.path.join(SHOWCASE_DST, ".git", "dummy_test_dir")
    git_dummy_file = os.path.join(git_dummy_dir, "test_git_file")
    os.makedirs(git_dummy_dir, exist_ok=True)
    with open(git_dummy_file, "w") as f:
        f.write("git dummy")

    github_dummy_dir = os.path.join(SHOWCASE_DST, ".github", "workflows")
    github_dummy_file = os.path.join(github_dummy_dir, "test_workflow.yml")
    os.makedirs(github_dummy_dir, exist_ok=True)
    with open(github_dummy_file, "w") as f:
        f.write("github dummy")

    print(f"Created stale files:\n  {stale_root}\n  {stale_theme}\n  {stale_nested_file}")
    print(f"Created preserved files:\n  {git_dummy_file}\n  {github_dummy_file}")

    # Run sync
    res = run_sync()
    assert res.returncode == 0, f"Sync script failed with return code {res.returncode}"

    # Verify stale files are pruned
    assert not os.path.exists(stale_root), f"FAILED: {stale_root} was NOT pruned!"
    assert not os.path.exists(stale_theme), f"FAILED: {stale_theme} was NOT pruned!"
    assert not os.path.exists(stale_nested_file), f"FAILED: {stale_nested_file} was NOT pruned!"
    assert not os.path.exists(os.path.join(SHOWCASE_DST, "deep")), f"FAILED: Directory 'deep' was NOT pruned!"
    print("✓ All stale files and empty directories pruned successfully!")

    # Verify preserved files are intact
    assert os.path.exists(git_dummy_file), f"FAILED: {git_dummy_file} was incorrectly pruned!"
    assert os.path.exists(github_dummy_file), f"FAILED: {github_dummy_file} was incorrectly pruned!"
    print("✓ Excluded directories (.git, .github) preserved successfully!")

    # Clean up dummy test files created in .git and .github
    os.remove(git_dummy_file)
    os.rmdir(git_dummy_dir)
    os.remove(github_dummy_file)
    os.rmdir(github_dummy_dir)

def test_sync_idempotency():
    print("\n=== Test 2: Sync Idempotency ===")
    # First sync run (ensure baseline)
    res1 = run_sync()
    assert res1.returncode == 0

    # Second sync run immediately after
    res2 = run_sync()
    assert res2.returncode == 0

    assert "Pruned 0 stale file(s)" in res2.stdout, f"Idempotency failed: second run pruned files! Stdout: {res2.stdout}"
    assert ("No changes in showcase repo" in res2.stdout or "Everything up-to-date" in res2.stdout or "nothing to commit" in res2.stdout), \
        f"Idempotency failed: git repository not clean on second run! Stdout: {res2.stdout}"

    print("✓ Sync idempotency verified! (0 pruned files on second run, clean git state)")

def test_content_update_sync():
    print("\n=== Test 3: Modified Content Synchronization ===")
    test_src_file = os.path.join(SHOWCASE_SRC, "themes", "style_01_glassmorphic.html")
    test_dst_file = os.path.join(SHOWCASE_DST, "themes", "style_01_glassmorphic.html")

    with open(test_src_file, "r") as f:
        orig_content = f.read()

    try:
        # Append comment to source file
        with open(test_src_file, "a") as f:
            f.write("\n<!-- empirical test comment -->")

        res = run_sync()
        assert res.returncode == 0

        with open(test_dst_file, "r") as f:
            dst_content = f.read()

        assert "<!-- empirical test comment -->" in dst_content, "FAILED: Updated content was not synced to target file!"
        print("✓ Modified content synchronized successfully!")

    finally:
        # Restore original file content
        with open(test_src_file, "w") as f:
            f.write(orig_content)
        run_sync()

def main():
    test_stale_pruning()
    test_sync_idempotency()
    test_content_update_sync()
    print("\n🎉 ALL M3 ADVERSARIAL TESTS PASSED PERFECTLY!")

if __name__ == "__main__":
    main()
