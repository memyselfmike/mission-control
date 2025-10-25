# Story 8.3: Architecture Documentation

Status: Draft

## Story

As a **Developer (including future AI agents coding Mission Control)**,
I want **comprehensive architecture documentation with diagrams and migration guides**,
so that **I can understand the Hexagonal Architecture and contribute effectively**.

## Acceptance Criteria

1. **AC1**: ARCHITECTURE-V2.md updated with complete Hexagonal Architecture description (all 4 layers documented)
2. **AC2**: Architecture includes ASCII art or mermaid diagrams showing layer dependencies
3. **AC3**: All domain entities, value objects, and services documented with purpose and relationships
4. **AC4**: Repository pattern explained with implementation examples
5. **AC5**: Migration guide for remaining epics (EPIC-3 Part 2, EPIC-4, EPIC-5, EPIC-6, EPIC-7)
6. **AC6**: Feature flag system documented (USE_NEW_ARCHITECTURE and Strangler Fig pattern)
7. **AC7**: ADR (Architecture Decision Record) created for Hexagonal Architecture adoption

## Tasks / Subtasks

- [ ] Task 1: Update ARCHITECTURE-V2.md structure (AC1)
  - [ ] 1.1: Add "Overview" section with Hexagonal Architecture introduction
  - [ ] 1.2: Add "Layer Descriptions" section (Domain, Application, Infrastructure, Presentation)
  - [ ] 1.3: Add "Dependency Rules" section (strict inward-only dependencies)
  - [ ] 1.4: Add "Current State" section (what's implemented, what's legacy)
- [ ] Task 2: Create architecture diagrams (AC2)
  - [ ] 2.1: Create high-level Hexagonal Architecture diagram (ASCII art)
  - [ ] 2.2: Create layer dependency diagram
  - [ ] 2.3: Create example flow diagram (user request → presentation → application → domain → infrastructure)
  - [ ] 2.4: Add diagrams to ARCHITECTURE-V2.md
- [ ] Task 3: Document domain layer (AC3)
  - [ ] 3.1: Document all value objects (Priority, Status, EnergyLevel, Context, TimeBlock)
  - [ ] 3.2: Document Task entity (fields, behavior methods, factory methods)
  - [ ] 3.3: Document domain services (TaskPrioritizationService, EnergyMatchingService, TimeBlockingService)
  - [ ] 3.4: Document domain events (BaseEvent, TaskEvents)
  - [ ] 3.5: Create domain relationship diagram
- [ ] Task 4: Document repository pattern (AC4)
  - [ ] 4.1: Explain repository pattern benefits
  - [ ] 4.2: Document repository interfaces (ITaskRepository, IMemoryRepository, etc.)
  - [ ] 4.3: Document JSON implementations
  - [ ] 4.4: Provide code examples for creating/using repositories
  - [ ] 4.5: Explain how to add new repositories
- [ ] Task 5: Create migration guide (AC5)
  - [ ] 5.1: Identify remaining legacy code to migrate
  - [ ] 5.2: Provide step-by-step migration approach for each EPIC
  - [ ] 5.3: Document refactoring patterns (procedural → OOP)
  - [ ] 5.4: Explain how to migrate workflows.py, morning_briefing.py, eod_wrapup.py
  - [ ] 5.5: Create checklist for future stories
- [ ] Task 6: Document feature flag system (AC6)
  - [ ] 6.1: Explain Strangler Fig pattern
  - [ ] 6.2: Document USE_NEW_ARCHITECTURE flag
  - [ ] 6.3: Document config.py usage
  - [ ] 6.4: Provide examples of dual-path routing
  - [ ] 6.5: Explain rollout strategy
- [ ] Task 7: Create ADR for Hexagonal Architecture (AC7)
  - [ ] 7.1: Create docs/architecture/adr/ADR-009-hexagonal-architecture.md
  - [ ] 7.2: Document context (why we needed refactoring)
  - [ ] 7.3: Document decision (Hexagonal Architecture chosen)
  - [ ] 7.4: Document consequences (benefits and trade-offs)
  - [ ] 7.5: Document status (accepted, implemented in EPIC-5R)

## Dev Notes

### Architecture Context

**Layer:** Documentation (No code changes, pure documentation story)
**Pattern:** No tests required (documentation story)
**Purpose:** Enable future developers (human and AI) to understand and extend the architecture

### Documentation Structure

```
docs/
├── ARCHITECTURE-V2.md (primary architecture doc)
├── architecture/
│   ├── diagrams/
│   │   ├── hexagonal-overview.txt (ASCII art)
│   │   ├── layer-dependencies.txt (ASCII art)
│   │   └── example-flow.txt (ASCII art)
│   └── adr/
│       ├── ADR-001-project-structure.md (existing)
│       ├── ...
│       └── ADR-009-hexagonal-architecture.md (new)
├── epics.md (existing, reference for migration guide)
└── stories/ (existing, reference for implemented features)
```

### Key Concepts to Document

1. **Hexagonal Architecture (Ports & Adapters)**
   - Core domain isolated from external concerns
   - Dependency inversion (domain defines interfaces, infrastructure implements)
   - Testability (mock external dependencies)

2. **Four Layers**
   - **Domain**: Pure business logic (Task, Priority, etc.)
   - **Application**: Use cases and orchestration (PlanningService, BriefingService)
   - **Infrastructure**: External concerns (JSON storage, file I/O, API clients)
   - **Presentation**: User interface (CLI commands, formatters)

3. **Dependency Rules**
   - Domain depends on nothing
   - Application depends on Domain
   - Infrastructure depends on Domain (implements interfaces)
   - Presentation depends on Application and Domain
   - NO downward dependencies (Infrastructure cannot depend on Presentation)

4. **Strangler Fig Pattern**
   - Build new alongside old
   - Feature flag controls which path
   - Gradual migration, zero downtime
   - Remove old code when new validated

### ADR Template

```markdown
# ADR-009: Adopt Hexagonal Architecture

## Status
Accepted (2025-10-20)

## Context
[Explain architectural debt from Sprint 5 planning]

## Decision
[Explain Hexagonal/Clean Architecture choice]

## Consequences
### Benefits
- [List 8+ benefits]

### Trade-offs
- [List any downsides]

## Implementation
[Reference EPIC-5R phases and stories]
```

### Migration Guide Structure

For each remaining EPIC:
1. **Current State**: What's implemented in legacy code
2. **Target State**: What it should look like in new architecture
3. **Migration Steps**: Specific refactoring tasks
4. **Example Code**: Before/after comparison
5. **Testing Strategy**: How to ensure no regressions

### Code Examples to Include

**Before (Legacy - Procedural):**
```python
def create_task(task_dict: Dict[str, Any]) -> Dict[str, Any]:
    task_dict['created_at'] = datetime.now().isoformat()
    tasks = _load_tasks()
    tasks.append(task_dict)
    _save_tasks(tasks)
    return task_dict
```

**After (New - OOP with Repository):**
```python
def create_task(title: str, priority: Priority) -> Task:
    task = Task.create(title=title, priority=priority)
    repository.save(task)
    return task
```

### Diagrams to Create

**Hexagonal Overview (ASCII):**
```
┌─────────────────────────────────────────┐
│         Presentation Layer              │
│  (CLI commands, formatters, UI)         │
└─────────────┬───────────────────────────┘
              │
┌─────────────▼───────────────────────────┐
│        Application Layer                │
│  (Use cases, services, orchestration)   │
└─────────────┬───────────────────────────┘
              │
┌─────────────▼───────────────────────────┐
│           Domain Layer                  │
│  (Entities, value objects, services)    │
│  (Pure business logic, zero deps)       │
└─────────────┬───────────────────────────┘
              │
┌─────────────▼───────────────────────────┐
│       Infrastructure Layer              │
│  (Repositories, file I/O, external)     │
└─────────────────────────────────────────┘
```

### Project Structure Notes

**Purpose**: This story creates the definitive reference for:
- New developers joining the project
- AI agents coding Mission Control (using CLAUDE.md + ARCHITECTURE-V2.md)
- Future Mike reviewing code after time away
- External contributors understanding design decisions

**Self-Coding Ready**: After this story, Mission Control can code itself using:
1. CLAUDE.md (engineering standards)
2. ARCHITECTURE-V2.md (architectural patterns)
3. Story templates (feature specifications)

### References

- [Source: D:\Mission Control\mission-control\CLAUDE.md#Architecture Standards]
- [Source: D:\Mission Control\docs\epics.md#EPIC-5R]
- [Source: D:\Mission Control\docs\solution-architecture.md#Current Architecture]
- [Source: D:\Mission Control\PRODUCT-BACKLOG.md#Sprint Change Proposal]
- [Source: D:\Mission Control\docs\stories\story-5.1-domain-value-objects.md]
- [Source: D:\Mission Control\docs\stories\story-5.2-task-entity.md]
- [Source: D:\Mission Control\docs\stories\story-6.1-task-management-use-cases.md]

## Dev Agent Record

### Context Reference

<!-- Path(s) to story context XML will be added here by context workflow -->

### Agent Model Used

<!-- Will be filled during implementation -->

### Debug Log References

### Completion Notes List

### File List
