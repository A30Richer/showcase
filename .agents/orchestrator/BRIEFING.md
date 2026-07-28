# BRIEFING — 2026-07-28T14:37:52Z

## Mission
Reorganize dashboard/showcase into subdirectories (themes/, apps/, pages/), update all relative paths/links, and ensure sync_showcase.sh works seamlessly.

## 🔒 My Identity
- Archetype: teamwork_orchestrator
- Roles: orchestrator, user_liaison, human_reporter, successor
- Working directory: /root/ai-workspace/test/dashboard/showcase/.agents/orchestrator
- Original parent: top-level
- Original parent conversation ID: parent

## 🔒 My Workflow
- **Pattern**: Project Pattern
- **Scope document**: /root/ai-workspace/test/dashboard/showcase/PROJECT.md
1. **Decompose**: Survey codebase via 3 Explorers, create PROJECT.md, define milestones.
2. **Dispatch & Execute**:
   - **Direct (iteration loop)**: Explorer -> Worker -> Reviewer -> Challenger -> Auditor -> Gate.
3. **On failure**: Retry -> Replace -> Skip -> Redistribute -> Redesign -> Escalate.
4. **Succession**: Spawn count threshold 20.
- **Work items**:
  1. Survey & Architecture [done]
  2. M1: File Reorganization & Structural Move [done]
  3. M2: Relative Path & Link Updates [done]
  4. M3: Sync Script Compatibility & Verification [in-progress]
  5. M4: Final Link Audit & E2E Validation [pending]
- **Current phase**: 3 (Milestone 3 Execution)
- **Current focus**: Milestone 3 Worker execution (a13301dd-b52e-425c-9197-9d04a849e5c5)

## 🔒 Key Constraints
- NEVER write, modify, or create source code files directly.
- NEVER run build/test commands yourself — require workers to do so.
- NEVER investigate or explore the problem at the code level — dispatch Explorers for technical investigation.
- You MAY use file-editing tools ONLY for metadata/state files (.md) in your .agents/ folder.
- DO NOT CHEAT warning included in Worker prompt.
- Audit is a binary veto.

## Current Parent
- Conversation ID: parent
- Updated: not yet

## Key Decisions Made
- Dispatched worker_m3 to update sync_showcase.sh with two-pass Python mirror sync & exclusions.

## Team Roster
| Agent | Type | Work Item | Status | Conv ID |
|-------|------|-----------|--------|---------|
| worker_m3 | teamwork_preview_worker | Milestone 3 Sync Script Updates | in-progress | a13301dd-b52e-425c-9197-9d04a849e5c5 |

## Succession Status
- Succession required: no
- Spawn count: 16 / 20
- Pending subagents: a13301dd-b52e-425c-9197-9d04a849e5c5
- Predecessor: none
- Successor: not yet spawned

## Active Timers
- Heartbeat cron: task-11
- Safety timer: none

## Artifact Index
- /root/ai-workspace/test/dashboard/showcase/.agents/ORIGINAL_REQUEST.md — Original User Request
- /root/ai-workspace/test/dashboard/showcase/.agents/orchestrator/DISPATCH.md — Dispatch instructions
- /root/ai-workspace/test/dashboard/showcase/.agents/orchestrator/progress.md — Progress tracking
- /root/ai-workspace/test/dashboard/showcase/PROJECT.md — Project specification & milestone plan
- /root/ai-workspace/test/dashboard/showcase/.agents/orchestrator/GATE_STATUS.md — Milestone gate statuses
