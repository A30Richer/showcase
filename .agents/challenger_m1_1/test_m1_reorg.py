#!/usr/bin/env python3
import os
import sys
import unittest

SHOWCASE_DIR = '/root/ai-workspace/test/dashboard/showcase'

EXPECTED_THEMES = {
    'style_01_glassmorphic.html',
    'style_02_neumorphic.html',
    'style_03_cyberpunk.html',
    'style_04_neobrutalism.html',
    'style_05_clean_saas.html',
    'style_06_synthwave.html',
    'style_07_luxury_gold.html',
    'style_08_bento_grid.html',
    'style_09_claymorphism.html',
    'style_10_hacker_terminal.html'
}

EXPECTED_APPS = {
    'youtube_downloader.html',
    'vocal_remover.html',
    'second_brain.html',
    'shop_vouchers.html'
}

EXPECTED_PAGES = {
    'cute_quiz.html',
    'love_counter.html',
    'present_agy_cli.html',
    'website_design.html',
    'main.html'
}

ALL_MOVED_FILES = EXPECTED_THEMES | EXPECTED_APPS | EXPECTED_PAGES

class TestMilestone1Reorganization(unittest.TestCase):

    def test_themes_directory(self):
        path = os.path.join(SHOWCASE_DIR, 'themes')
        self.assertTrue(os.path.isdir(path), "themes/ directory does not exist")
        actual_files = set(os.listdir(path))
        self.assertEqual(actual_files, EXPECTED_THEMES, f"themes/ directory content mismatch. Missing: {EXPECTED_THEMES - actual_files}, Extra: {actual_files - EXPECTED_THEMES}")

    def test_apps_directory(self):
        path = os.path.join(SHOWCASE_DIR, 'apps')
        self.assertTrue(os.path.isdir(path), "apps/ directory does not exist")
        actual_files = set(os.listdir(path))
        self.assertEqual(actual_files, EXPECTED_APPS, f"apps/ directory content mismatch. Missing: {EXPECTED_APPS - actual_files}, Extra: {actual_files - EXPECTED_APPS}")

    def test_pages_directory(self):
        path = os.path.join(SHOWCASE_DIR, 'pages')
        self.assertTrue(os.path.isdir(path), "pages/ directory does not exist")
        actual_files = set(os.listdir(path))
        self.assertEqual(actual_files, EXPECTED_PAGES, f"pages/ directory content mismatch. Missing: {EXPECTED_PAGES - actual_files}, Extra: {actual_files - EXPECTED_PAGES}")

    def test_root_directory_cleanliness(self):
        root_files = set(os.listdir(SHOWCASE_DIR))
        # Ensure none of the 19 moved HTML files remain in root
        stray_in_root = root_files.intersection(ALL_MOVED_FILES)
        self.assertEqual(len(stray_in_root), 0, f"Moved files still present in root: {stray_in_root}")

        # Ensure required root components exist
        self.assertIn('index.html', root_files, "index.html missing from root")
        self.assertIn('themes', root_files, "themes/ missing from root")
        self.assertIn('apps', root_files, "apps/ missing from root")
        self.assertIn('pages', root_files, "pages/ missing from root")
        self.assertIn('assets', root_files, "assets/ missing from root")
        self.assertIn('reports', root_files, "reports/ missing from root")

    def test_file_non_empty(self):
        for rel_dir, files in [('themes', EXPECTED_THEMES), ('apps', EXPECTED_APPS), ('pages', EXPECTED_PAGES)]:
            for f in files:
                fpath = os.path.join(SHOWCASE_DIR, rel_dir, f)
                self.assertTrue(os.path.exists(fpath), f"{fpath} does not exist")
                self.assertGreater(os.path.getsize(fpath), 0, f"{fpath} is empty")

if __name__ == '__main__':
    unittest.main()
