# PROJECT RULES - For Claude Agents

**Project:** Mission Control
**Purpose:** Guide all future Claude agents working on this project
**Created:** 2025-10-17
**Authority:** Mike (Product Owner)

---

## CRITICAL: READ THIS FIRST

This document defines the rules for ALL Claude agents (including Claude Code, Claude Desktop, and BMAD agents) working on Mission Control. Following these rules ensures consistency, prevents confusion, and maintains project quality.

---

## 1. FILE ORGANIZATION RULES

### 1.1 Documentation Structure (STRICT)

**Root Level - ONLY These Files:**
```
D:\Mission Control/
├── README.md                  [Project overview - DO NOT MOVE]
├── PRODUCT-BACKLOG.md         [Active backlog - DO NOT MOVE]
├── .claudecontext.md          [THIS FILE - Agent rules]
└── [No other .md files allowed at root]
```

**docs/ Folder - Core Planning Documents:**
```
docs/
├── index.md                   [Documentation index]
├── bmm-workflow-status.md     [Current sprint/story status]
├── PRD.md                     [Product requirements]
├── epics.md                   [Epic definitions]
├── solution-architecture.md   [Architecture documentation]
├── project-overview.md        [Project summary]
└── source-tree-analysis.md    [Codebase analysis]
```

**docs/stories/ - ONLY Active Stories:**
```
docs/stories/
├── story-2.1.md               [Completed stories stay here for reference]
├── story-2.2.md
├── story-2.3.md
└── story-X.Y.md               [Future stories - filename format: story-{EPIC}.{NUM}-{slug}.md]
```

**docs/archive/ - All Sprint Artifacts:**
```
docs/archive/
├── sprint-summaries/          [Sprint planning, kickoff, retrospectives, summaries]
├── story-artifacts/           [Story implementation notes, design docs, variants]
├── qa-reports/                [QA plans, test results, status reports]
├── bug-fixes/                 [Bug fix summaries and reports]
└── misc/                      [Cleanup reports, audits, one-off documents]
```

### 1.2 File Placement Rules

**Rule 1.2.1:** NEVER create markdown files at project root except README.md, PRODUCT-BACKLOG.md, and .claudecontext.md

**Rule 1.2.2:** Sprint summaries ALWAYS go to `docs/archive/sprint-summaries/` (never root, never docs/)

**Rule 1.2.3:** Story files ONLY exist in `docs/stories/` - use format `story-{EPIC}.{NUM}-{slug}.md`

**Rule 1.2.4:** Story implementation notes, design alternatives, and artifacts go to `docs/archive/story-artifacts/`

**Rule 1.2.5:** QA reports and test results go to `docs/archive/qa-reports/`

**Rule 1.2.6:** Bug fix summaries go to `docs/archive/bug-fixes/`

**Rule 1.2.7:** All audit reports, cleanup summaries, and one-off docs go to `docs/archive/misc/`

---

## 2. STORY NUMBERING CONVENTION

### 2.1 Story Number Format

**Format:** `EPIC#.Story#` (e.g., Story 2.1, Story 3.5, Story 4.12)

**Examples:**
- Story 2.1 = First story in EPIC-2
- Story 3.5 = Fifth story in EPIC-3
- Story 4.12 = Twelfth story in EPIC-4

### 2.2 Story Filename Format

**Format:** `story-{EPIC}.{NUM}-{slug}.md`

**Examples:**
- `story-2.1-business-context-storage.md`
- `story-3.1-operator-agent-persona.md`
- `story-4.1-planner-agent-definition.md`

### 2.3 Current Story Status (As of 2025-10-17)

**EPIC-1 (Autonomous Agent Framework):**
- ✅ Story 1.6: Scheduled Task Execution (Complete)
- ✅ Story 1.7: Event Detection System (Complete)
- ✅ Story 1.8: Pattern Recognition Engine (Complete)
- ✅ Story 1.9: Context Gathering (Complete)

**EPIC-2 (Persistent Memory System):**
- ✅ Story 2.1: Business Context Storage (Complete)
- ✅ Story 2.2: Conversation History Logging (Complete)
- ✅ Story 2.3: Preference Learning System (Complete)
- 🔜 Story 2.4: Memory Loading on Startup (Next if continuing EPIC-2)
- 🔜 Story 2.5: Memory Pruning Strategy (Planned)

**EPIC-3 (Operator Agent):**
- 🔜 Story 3.1: Create Operator Agent (Next if starting EPIC-3)
- 🔜 Story 3.2-3.10: TBD

**EPIC-4 (Planner Agent):**
- 🔜 Story 4.1: Create Planner Agent (Next if starting EPIC-4)
- 🔜 Story 4.2-4.10: TBD

### 2.4 Story Numbering Rules

**Rule 2.4.1:** Stories are numbered sequentially WITHIN their epic

**Rule 2.4.2:** NEVER renumber completed stories (git history is sacred)

**Rule 2.4.3:** If stories are implemented out of order, accept the numbering and document the deviation

**Rule 2.4.4:** New stories use the next available number in their epic (e.g., if Story 3.5 exists, next is 3.6)

**Rule 2.4.5:** Story numbers in git commits must match story file names

---

## 3. SPRINT & WORKFLOW RULES

### 3.1 Sprint Documentation

**Rule 3.1.1:** Sprint planning docs go to `docs/archive/sprint-summaries/sprint-{N}-planning.md`

**Rule 3.1.2:** Sprint kickoff docs go to `docs/archive/sprint-summaries/sprint-{N}-kickoff.md`

**Rule 3.1.3:** Daily summaries go to `docs/archive/sprint-summaries/sprint-{N}-day-{D}-summary.md`

**Rule 3.1.4:** Sprint retrospectives go to `docs/archive/sprint-summaries/sprint-{N}-retrospective.md`

**Rule 3.1.5:** Sprint status reports go to `docs/archive/sprint-summaries/sprint-{N}-status-report.md`

### 3.2 Story Workflow Stages

**Story Lifecycle:**
1. **Draft** - Story created in `docs/stories/story-X.Y.md` with "Status: Draft"
2. **Ready** - SM approves story (Status: Ready)
3. **In Progress** - DEV implements (Status: In Progress)
4. **Ready for Review** - Implementation complete, awaiting review (Status: Ready for Review)
5. **Done** - User approved, tests passing (Status: Done)

**Rule 3.2.1:** Story status MUST be updated in the story file header

**Rule 3.2.2:** Story status MUST be updated in PRODUCT-BACKLOG.md

**Rule 3.2.3:** Story status MUST be updated in bmm-workflow-status.md

### 3.3 Current Sprint Status (As of 2025-10-17)

**Completed Sprints:**
- ✅ Sprint 1: EPIC-2 Memory System (16 points, 100% complete)
- ✅ Sprint 2: EPIC-1 Autonomous Behaviors (29 points, 100% complete)

**Current Status:**
- Sprint 3: Awaiting Mike's decision on priority (EPIC-3 Operator vs. EPIC-4 Planner vs. finish EPIC-1/2)

**Progress:**
- **Delivered:** 45 story points
- **Remaining:** ~260 story points
- **Completion:** 15-17% of project

---

## 4. GIT COMMIT RULES

### 4.1 Commit Message Format

**Format:** `Story X.Y: [Brief description]`

**Examples:**
- `Story 2.1: Business Context Storage - Implementation Complete`
- `Story 2.2 APPROVED: Conversation History Logging Complete`
- `Story 2.3: Context XML generated for Preference Learning`

**Rule 4.1.1:** All story-related commits MUST reference the story number

**Rule 4.1.2:** Commit messages should indicate story stage (DRAFTED, APPROVED, COMPLETE, etc.)

**Rule 4.1.3:** Bug fixes reference the affected story or use format `Bug Fix: [description]`

### 4.2 What to Commit

**Rule 4.2.1:** Commit code changes as they occur (don't batch multiple stories)

**Rule 4.2.2:** Commit documentation updates separately from code

**Rule 4.2.3:** Use conventional commit prefixes for non-story work:
- `docs:` for documentation-only changes
- `test:` for test-only changes
- `refactor:` for code refactoring
- `fix:` for bug fixes

---

## 5. TESTING RULES

### 5.1 Test Requirements

**Rule 5.1.1:** Every story MUST have automated tests

**Rule 5.1.2:** Tests go in `mission-control/tests/` directory

**Rule 5.1.3:** Test files use format `test_{feature}.py` (e.g., `test_memory.py`, `test_preferences.py`)

**Rule 5.1.4:** Minimum test coverage: 80% for story acceptance

**Rule 5.1.5:** All tests must pass before story marked "Done"

### 5.2 Test Naming

**Format:** `test_{feature}_{scenario}` or `test_{function}_{condition}__{expected}`

**Examples:**
- `test_load_business_context_with_missing_file`
- `test_update_preference_with_invalid_category__returns_false`
- `test_analyze_conversation_for_preferences__explicit_detection`

---

## 6. DOCUMENTATION UPDATE RULES

### 6.1 Required Updates Per Story

When completing a story, MUST update:

**Rule 6.1.1:** Update story file (`docs/stories/story-X.Y.md`) with:
- Status: Done
- Completion date
- Implementation summary
- Test results
- Git commit references

**Rule 6.1.2:** Update `PRODUCT-BACKLOG.md` with:
- Story completion checkmark (✅)
- Actual points delivered
- Sprint progress percentage
- Epic completion status

**Rule 6.1.3:** Update `docs/bmm-workflow-status.md` with:
- Current story/sprint status
- Next action
- Progress metrics
- Decision log entry

**Rule 6.1.4:** Update `docs/index.md` if:
- New major documentation added
- File structure changed
- New epic started

---

## 7. BMAD WORKFLOW RULES

### 7.1 Workflow Execution

**Rule 7.1.1:** Follow BMAD workflows in order: create-story → story-ready → story-context → dev-story → story-approved

**Rule 7.1.2:** NEVER skip story-ready validation (SM approval required)

**Rule 7.1.3:** ALWAYS generate story-context XML before dev-story

**Rule 7.1.4:** Mark story "Done" only after user (Mike) approval via story-approved workflow

### 7.2 Agent Roles

**Bob (Scrum Master):** Validates stories, runs story-ready workflow, manages sprint planning

**DEV Agent:** Implements stories, runs dev-story workflow, creates tests

**Mike (Product Owner):** Approves stories, sets priorities, makes architectural decisions

**Rule 7.2.1:** Respect role boundaries - don't have DEV approve stories, don't have SM write code

**Rule 7.2.2:** When in doubt about priority, ask Mike (Product Owner)

---

## 8. COMMUNICATION RULES

### 8.1 When to Ask Mike

**ASK Mike for:**
- Priority decisions (which epic/story to do next)
- Architectural decisions (technology choices, design patterns)
- Story acceptance (is the implementation good enough?)
- Scope changes (should this story include X feature?)
- Timeline adjustments (need more time on this sprint?)

**DON'T ASK Mike for:**
- Implementation details (function names, variable choices)
- Test structure (how to organize tests)
- Documentation formatting (markdown style choices)
- File organization within established rules

### 8.2 Communication Style

**Rule 8.2.1:** Be direct and concise (Mike prefers clarity over verbosity)

**Rule 8.2.2:** Present options with recommendations ("Option A: X, Option B: Y. I recommend A because Z")

**Rule 8.2.3:** Don't apologize for normal development challenges (bugs happen, that's why we test)

**Rule 8.2.4:** Celebrate wins briefly, then move forward ("Story 2.1 complete! Moving to 2.2...")

---

## 9. QUALITY STANDARDS

### 9.1 Code Quality

**Rule 9.1.1:** All code must have docstrings (function-level minimum)

**Rule 9.1.2:** All code must handle errors gracefully (no unhandled exceptions in production paths)

**Rule 9.1.3:** All code must have type hints (Python 3.13+ style)

**Rule 9.1.4:** All functions return meaningful values (bool for success/fail, dict for data, None intentionally)

### 9.2 Documentation Quality

**Rule 9.2.1:** Story files must be complete (all sections filled, no TBD placeholders in Done stories)

**Rule 9.2.2:** Code comments explain WHY, not WHAT (the code shows what, comments explain why this approach)

**Rule 9.2.3:** README files are up-to-date (installation instructions, usage examples, current features)

---

## 10. EMERGENCY PROCEDURES

### 10.1 When Things Go Wrong

**If you break the build:**
1. Fix it immediately (priority over all other work)
2. Document the fix in `docs/archive/bug-fixes/`
3. Add regression test to prevent recurrence
4. Update bmm-workflow-status.md with incident

**If you realize story numbering is wrong:**
1. STOP - don't renumber anything
2. Document the discrepancy in bmm-workflow-status.md
3. Ask Mike for guidance
4. Accept reality (numbering doesn't have to be perfect)

**If documentation conflicts arise:**
1. Git history is the source of truth for code
2. PRODUCT-BACKLOG.md is the source of truth for status
3. bmm-workflow-status.md is the source of truth for current sprint
4. When conflicts exist, prioritize in that order

---

## 11. FORBIDDEN ACTIONS

**NEVER:**
- ❌ Create markdown files at project root (except README.md, PRODUCT-BACKLOG.md, .claudecontext.md)
- ❌ Renumber completed stories
- ❌ Rewrite git history (no force push, no amend of pushed commits)
- ❌ Skip tests because "it's simple code"
- ❌ Mark story Done without user (Mike) approval
- ❌ Start new epic without Mike's explicit approval
- ❌ Delete archive files (they're historical records)
- ❌ Modify story files after they're marked Done (create new story instead)

---

## 12. PREFERRED ACTIONS

**ALWAYS:**
- ✅ Read .claudecontext.md before starting work (this file!)
- ✅ Check bmm-workflow-status.md for current sprint/story
- ✅ Update all three docs (story file, backlog, workflow status) when completing stories
- ✅ Write tests FIRST (TDD preferred but not required)
- ✅ Commit frequently with good messages
- ✅ Ask Mike when uncertain about priorities
- ✅ Archive artifacts to proper folders
- ✅ Follow BMAD workflows in sequence

---

## 13. PROJECT-SPECIFIC CONTEXT

### 13.1 Project Goals

Mission Control is an **autonomous AI executive team** that:
- Provides structured accountability (daily/weekly/quarterly check-ins)
- Offers ad-hoc strategic thinking
- Surfaces proactive intelligence
- Maintains persistent memory
- Extends itself via custom agents

**Key Differentiator:** Autonomous agents that work FOR the user, not just respond TO the user.

### 13.2 Technology Stack

- **Language:** Python 3.13+
- **AI Framework:** Claude Agent SDK
- **Methodology:** BMAD Method patterns
- **CLI Framework:** Rich (for formatted output)
- **Testing:** pytest
- **Memory:** File-based JSON/JSONL (no database for MVP)
- **Platform:** Windows primary, cross-platform compatible

### 13.3 Architecture Principles

1. **Modular Monolith:** Single application, clean module boundaries
2. **File-Based Storage:** JSON for state, JSONL for logs
3. **Hook-Driven:** Events trigger hooks, hooks call functions
4. **Agent-Based:** 6 specialist agents (Chief of Staff + 5 subagents)
5. **Test-First:** High test coverage, automated validation
6. **Privacy-First:** All data local, no external calls except Claude API

---

## 14. QUICK REFERENCE

### File Goes Where?

| Document Type | Location |
|---------------|----------|
| Sprint planning | `docs/archive/sprint-summaries/sprint-{N}-planning.md` |
| Sprint retrospective | `docs/archive/sprint-summaries/sprint-{N}-retrospective.md` |
| Story file (active) | `docs/stories/story-{EPIC}.{NUM}-{slug}.md` |
| Story implementation notes | `docs/archive/story-artifacts/story-{EPIC}.{NUM}-{description}.md` |
| QA report | `docs/archive/qa-reports/qa-{description}.md` |
| Bug fix summary | `docs/archive/bug-fixes/bug-{description}.md` |
| Audit/cleanup report | `docs/archive/misc/{description}.md` |
| Core planning doc | `docs/{name}.md` (e.g., PRD.md, epics.md) |

### What to Update When?

| Action | Update These |
|--------|-------------|
| Complete story | Story file, PRODUCT-BACKLOG.md, bmm-workflow-status.md |
| Complete sprint | All three above + create sprint retrospective |
| Start new story | bmm-workflow-status.md (Next Action field) |
| Change priority | PRODUCT-BACKLOG.md (Epic Overview, Sprint Planning) |
| Fix bug | Create bug fix doc, reference in commits |

---

## 15. COMPLIANCE VERIFICATION

Before considering any work "done," verify:

- [ ] All files in correct locations per Section 1
- [ ] Story numbered correctly per Section 2
- [ ] All required docs updated per Section 6
- [ ] Tests written and passing per Section 5
- [ ] Git commits follow format per Section 4
- [ ] No forbidden actions committed per Section 11
- [ ] User (Mike) approval obtained if required

---

**This document is AUTHORITATIVE for all Claude agents working on Mission Control.**

**Last Updated:** 2025-10-17
**Next Review:** When project structure significantly changes
**Authority:** Mike (Product Owner)

---

*"Good systems make compliance easy. This document makes it explicit."*
