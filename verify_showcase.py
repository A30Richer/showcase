#!/usr/bin/env python3
"""
verify_showcase.py - Showcase Directory Link Audit & Sync Verification Tool

This script performs 100% link integrity audit and structural verification
for the showcase dashboard repository and its synchronized deployment target.

Key Verification Steps:
1. Verifies structural file counts (10 themes, 4 apps, 5 pages, 1 index.html).
2. Audits all HTML files in showcase directory for broken internal relative links (href and src attributes).
3. Executes /root/ai-workspace/test/sync_showcase.sh script.
4. Verifies target directory /root/ai-workspace/showcase for matching structural counts and 0 broken links.
5. Exits with code 0 on 100% success, non-zero on failure.
"""

import sys
import os
import glob
import subprocess
import html.parser
import urllib.parse

# Default Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_SHOWCASE_DIR = os.path.normpath(SCRIPT_DIR)
SYNC_SCRIPT_PATH = os.path.normpath(os.path.join(SRC_SHOWCASE_DIR, "../../sync_showcase.sh"))
DST_SHOWCASE_DIR = "/root/ai-workspace/showcase"

EXPECTED_COUNTS = {
    "themes": 10,
    "apps": 4,
    "pages": 5,
    "root_index": 1,
}

EXCLUDE_DIRS = {".git", ".agents", ".gemini", "__pycache__", ".github", "node_modules"}

IGNORE_PREFIXES = (
    "http://",
    "https://",
    "mailto:",
    "javascript:",
    "data:",
    "tel:",
    "ftp://",
    "file://",
    "//",
)


class HTMLLinkExtractor(html.parser.HTMLParser):
    """Parses HTML and extracts href and src attribute values."""
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        for attr, val in attrs:
            if attr in ("href", "src") and val is not None:
                self.links.append((tag, attr, val))


def is_external_or_ignored(url: str) -> bool:
    """Returns True if the URL is external, anchor-only, or non-file scheme."""
    u = url.strip()
    if not u or u.startswith("#"):
        return True
    low_u = u.lower()
    if any(low_u.startswith(p) for p in IGNORE_PREFIXES):
        return True
    return False


def clean_link_target(raw_url: str) -> str:
    """Strips query parameters and fragment identifiers, unquotes URL encoding."""
    # Strip fragment and query parameters
    url_without_frag = raw_url.split("#")[0]
    url_clean = url_without_frag.split("?")[0]
    return urllib.parse.unquote(url_clean.strip())


def discover_html_files(base_dir: str):
    """Walks base_dir and yields paths of all HTML files, excluding hidden/ignored dirs."""
    html_files = []
    for root, dirs, files in os.walk(base_dir):
        # Exclude ignored directories in-place
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        rel_root = os.path.relpath(root, base_dir)
        if rel_root != "." and any(part in EXCLUDE_DIRS for part in rel_root.split(os.sep)):
            continue

        for f in files:
            if f.endswith(".html"):
                html_files.append(os.path.join(root, f))
    return sorted(html_files)


def verify_structural_counts(base_dir: str):
    """Verifies that base_dir matches expected file counts for themes, apps, pages, index.html."""
    errors = []
    actual_counts = {}

    root_index = os.path.join(base_dir, "index.html")
    actual_counts["root_index"] = 1 if os.path.isfile(root_index) else 0
    if actual_counts["root_index"] != EXPECTED_COUNTS["root_index"]:
        errors.append(f"Root index.html missing at {root_index}")

    for category in ("themes", "apps", "pages"):
        cat_dir = os.path.join(base_dir, category)
        if not os.path.isdir(cat_dir):
            actual_counts[category] = 0
            errors.append(f"Directory missing: {cat_dir}")
        else:
            cat_files = [f for f in os.listdir(cat_dir) if f.endswith(".html") and os.path.isfile(os.path.join(cat_dir, f))]
            actual_counts[category] = len(cat_files)
            expected = EXPECTED_COUNTS[category]
            if actual_counts[category] != expected:
                errors.append(
                    f"Structural count mismatch in '{category}/': expected {expected}, found {actual_counts[category]}"
                )

    return (len(errors) == 0, actual_counts, errors)


def audit_links_in_directory(base_dir: str):
    """
    Scans all HTML files in base_dir, parses href/src relative links,
    and checks if target files exist on disk.
    """
    html_files = discover_html_files(base_dir)
    total_files = len(html_files)
    total_links = 0
    broken_links = []

    for html_file in html_files:
        rel_html_path = os.path.relpath(html_file, base_dir)
        file_dir = os.path.dirname(html_file)

        parser = HTMLLinkExtractor()
        try:
            with open(html_file, "r", encoding="utf-8", errors="ignore") as f:
                parser.feed(f.read())
        except Exception as e:
            broken_links.append({
                "source_file": rel_html_path,
                "tag": "N/A",
                "attr": "N/A",
                "raw_link": "N/A",
                "resolved_path": "N/A",
                "error": f"Failed to read file: {e}"
            })
            continue

        for tag, attr, raw_url in parser.links:
            if is_external_or_ignored(raw_url):
                continue

            cleaned_url = clean_link_target(raw_url)
            if not cleaned_url:
                # Link was self-referential query/fragment (e.g. href="#")
                continue

            total_links += 1
            resolved_target = os.path.normpath(os.path.join(file_dir, cleaned_url))

            if not os.path.exists(resolved_target):
                broken_links.append({
                    "source_file": rel_html_path,
                    "tag": tag,
                    "attr": attr,
                    "raw_link": raw_url,
                    "resolved_path": resolved_target,
                    "error": "Target file does not exist"
                })

    return {
        "total_files": total_files,
        "total_links": total_links,
        "broken_links": broken_links,
        "passed": len(broken_links) == 0
    }


def run_sync_script(sync_script_path: str):
    """Executes the sync_showcase.sh script and captures return code and output."""
    if not os.path.exists(sync_script_path):
        return False, f"Sync script not found at {sync_script_path}", -1

    try:
        proc = subprocess.run(
            ["bash", sync_script_path],
            capture_output=True,
            text=True,
            check=False
        )
        output = proc.stdout + ("\nSTDERR:\n" + proc.stderr if proc.stderr else "")
        return proc.returncode == 0, output, proc.returncode
    except Exception as e:
        return False, f"Execution failed: {e}", -1


def main():
    print("=" * 70)
    print("🔍 SHOWCASE REPOSITORY LINK AUDIT & SYNC VERIFICATION")
    print("=" * 70)

    all_passed = True
    overall_errors = []

    # -------------------------------------------------------------------------
    # STEP 1: Verify Source Structural File Counts
    # -------------------------------------------------------------------------
    print(f"\n[1/4] Checking source structural file counts ({SRC_SHOWCASE_DIR})...")
    src_struct_ok, src_counts, src_struct_errs = verify_structural_counts(SRC_SHOWCASE_DIR)
    print(f"      Themes: {src_counts.get('themes', 0)}/{EXPECTED_COUNTS['themes']}")
    print(f"      Apps:   {src_counts.get('apps', 0)}/{EXPECTED_COUNTS['apps']}")
    print(f"      Pages:  {src_counts.get('pages', 0)}/{EXPECTED_COUNTS['pages']}")
    print(f"      Index:  {src_counts.get('root_index', 0)}/{EXPECTED_COUNTS['root_index']}")

    if src_struct_ok:
        print("   ✅ Source structural file counts MATCH expected values.")
    else:
        print("   ❌ Source structural file counts FAILED:")
        for err in src_struct_errs:
            print(f"      - {err}")
            overall_errors.append(f"Source Structure: {err}")
        all_passed = False

    # -------------------------------------------------------------------------
    # STEP 2: Audit Relative Links in Source Directory
    # -------------------------------------------------------------------------
    print(f"\n[2/4] Auditing relative links in source HTML files...")
    src_audit = audit_links_in_directory(SRC_SHOWCASE_DIR)
    print(f"      Scanned HTML files: {src_audit['total_files']}")
    print(f"      Internal relative links checked: {src_audit['total_links']}")
    print(f"      Broken links found: {len(src_audit['broken_links'])}")

    if src_audit['passed']:
        print("   ✅ Source link audit PASSED (100% link integrity).")
    else:
        print("   ❌ Source link audit FAILED with broken links:")
        for b in src_audit['broken_links']:
            err_msg = f"In {b['source_file']}: <{b['tag']} {b['attr']}=\"{b['raw_link']}\"> -> '{b['resolved_path']}' not found"
            print(f"      - {err_msg}")
            overall_errors.append(f"Source Link: {err_msg}")
        all_passed = False

    # -------------------------------------------------------------------------
    # STEP 3: Execute Sync Script
    # -------------------------------------------------------------------------
    print(f"\n[3/4] Executing sync script ({SYNC_SCRIPT_PATH})...")
    sync_ok, sync_output, sync_code = run_sync_script(SYNC_SCRIPT_PATH)

    if sync_ok:
        print(f"   ✅ Sync script executed successfully (exit code {sync_code}).")
    else:
        print(f"   ❌ Sync script execution FAILED (exit code {sync_code}):")
        for line in sync_output.strip().split("\n"):
            print(f"      {line}")
        overall_errors.append(f"Sync Script execution failed with exit code {sync_code}")
        all_passed = False

    # -------------------------------------------------------------------------
    # STEP 4: Verify Target Directory Structure & Links
    # -------------------------------------------------------------------------
    print(f"\n[4/4] Verifying target synchronized directory ({DST_SHOWCASE_DIR})...")
    if not os.path.isdir(DST_SHOWCASE_DIR):
        print(f"   ❌ Target directory does not exist: {DST_SHOWCASE_DIR}")
        overall_errors.append(f"Target directory {DST_SHOWCASE_DIR} missing")
        all_passed = False
    else:
        dst_struct_ok, dst_counts, dst_struct_errs = verify_structural_counts(DST_SHOWCASE_DIR)
        print(f"      Target Themes: {dst_counts.get('themes', 0)}/{EXPECTED_COUNTS['themes']}")
        print(f"      Target Apps:   {dst_counts.get('apps', 0)}/{EXPECTED_COUNTS['apps']}")
        print(f"      Target Pages:  {dst_counts.get('pages', 0)}/{EXPECTED_COUNTS['pages']}")
        print(f"      Target Index:  {dst_counts.get('root_index', 0)}/{EXPECTED_COUNTS['root_index']}")

        if dst_struct_ok:
            print("   ✅ Target structural file counts MATCH expected values.")
        else:
            print("   ❌ Target structural file counts FAILED:")
            for err in dst_struct_errs:
                print(f"      - {err}")
                overall_errors.append(f"Target Structure: {err}")
            all_passed = False

        dst_audit = audit_links_in_directory(DST_SHOWCASE_DIR)
        print(f"      Target Scanned HTML files: {dst_audit['total_files']}")
        print(f"      Target Internal links checked: {dst_audit['total_links']}")
        print(f"      Target Broken links found: {len(dst_audit['broken_links'])}")

        if dst_audit['passed']:
            print("   ✅ Target link audit PASSED (100% link integrity).")
        else:
            print("   ❌ Target link audit FAILED with broken links:")
            for b in dst_audit['broken_links']:
                err_msg = f"In {b['source_file']}: <{b['tag']} {b['attr']}=\"{b['raw_link']}\"> -> '{b['resolved_path']}' not found"
                print(f"      - {err_msg}")
                overall_errors.append(f"Target Link: {err_msg}")
            all_passed = False

    # -------------------------------------------------------------------------
    # FINAL SUMMARY
    # -------------------------------------------------------------------------
    print("\n" + "=" * 70)
    if all_passed:
        print("🎉 SUMMARY RESULT: PASSED (100% Verification & Sync Success)")
        print("=" * 70)
        sys.exit(0)
    else:
        print("💥 SUMMARY RESULT: FAILED")
        print(f"   Total failure issues: {len(overall_errors)}")
        for err in overall_errors:
            print(f"   - {err}")
        print("=" * 70)
        sys.exit(1)


if __name__ == "__main__":
    main()
