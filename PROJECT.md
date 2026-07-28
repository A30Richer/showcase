# Project: Showcase Directory Reorganization & Link Audit

## Architecture
- Directory layout:
  - `dashboard/showcase/`:
    - `index.html`: Portal landing page
    - `themes/`: Design style templates (`style_01_glassmorphic.html` through `style_10_hacker_terminal.html`)
    - `apps/`: Web application tools (`youtube_downloader.html`, `vocal_remover.html`, `second_brain.html`, `shop_vouchers.html`)
    - `pages/`: Interactive pages (`cute_quiz.html`, `love_counter.html`, `present_agy_cli.html`, `website_design.html`, `main.html`)
    - `assets/`: Shared assets (`images/`, etc.)
    - `reports/`: HTML report documents
  - Deployment sync script: `/root/ai-workspace/test/sync_showcase.sh` mirroring to `/root/ai-workspace/showcase`.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Directory Structure & Reorganization | Move 19 loose HTML files into `themes/`, `apps/`, `pages/` | M1 | Survey 1 |
| 2 | Root `index.html` Link Updates | Update 22 links to include folder prefixes (`themes/`, `apps/`, `pages/`) | M2 | Survey 2 |
| 3 | Theme HTML Link Updates | Update `website_design.html` links in 10 theme files to `../pages/website_design.html` | M2 | Survey 2 |
| 4 | App HTML Link Updates | Update `index.html` links in 4 app files to `../index.html` | M2 | Survey 2 |
| 5 | Page HTML Link Updates | Update links in 4 page files to `../index.html`, `../themes/`, `../reports/`, `../assets/` | M2 | Survey 2 |
| 6 | Report HTML Link Updates | Update `../main.html` links in 5 report files to `../pages/main.html` | M2 | Survey 2 |
| 7 | Sync Script Mirroring & Pruning | Update `sync_showcase.sh` with two-pass Python mirror sync & exclusions | M3 | Survey 3 |
| 8 | Link Verification Harness | Build `verify_showcase.py` and perform 100% link audit & sync verification | M4 | Survey 3 |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | M1: File Reorganization & Structural Move | Move HTML files to `themes/`, `apps/`, `pages/` | none | DONE |
| 2 | M2: Relative Path & Internal Link Updates | Update relative links across all 26 HTML files | M1 | DONE |
| 3 | M3: Sync Script Compatibility | Update `sync_showcase.sh` for mirror sync & exclusions | M1 | PLANNED |
| 4 | M4: Final Link Audit & E2E Validation | Create `verify_showcase.py` and run full E2E audit | M2, M3 | PLANNED |

## Interface Contracts
### HTML Page Navigation ↔ Directory Layout
- Root `index.html` refers to pages via `themes/<file>`, `apps/<file>`, `pages/<file>`, `reports/<file>`.
- Files in `themes/` refer to pages via `../pages/<file>` or `../index.html`.
- Files in `apps/` refer to pages via `../index.html` or `../pages/<file>`.
- Files in `pages/` refer to root via `../index.html`, themes via `../themes/<file>`, reports via `../reports/<file>`, assets via `../assets/<file>`.
- Files in `reports/` refer to main via `../pages/main.html`, sibling reports via `<file>`, assets via `../assets/<file>`.

## Code Layout
- Root source: `/root/ai-workspace/test/dashboard/showcase/`
- Target deployment: `/root/ai-workspace/showcase/`
- Sync script: `/root/ai-workspace/test/sync_showcase.sh`
- Verification script: `/root/ai-workspace/test/dashboard/showcase/verify_showcase.py`
