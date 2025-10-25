# Story 3.7: Productivity Pattern Learning

**Epic:** EPIC-3 - Operator (Daily Execution Agent)
**Story Points:** 8
**Priority:** P1
**Status:** In Progress
**Sprint:** Sprint 6 (post-EPIC-5R)

---

## User Story

**As a user**, I want Omega to analyze my task completion patterns and surface productivity insights so that I can understand my work rhythms and optimize my daily execution.

---

## Acceptance Criteria

### AC1: Task Completion Pattern Analysis
- Analyze task completion over time (daily, weekly trends)
- Identify peak productivity times/days
- Detect completion patterns by priority level
- Calculate velocity trends

### AC2: Insight Generation
- Generate 3+ actionable insights per week
- Insights based on actual completion data
- Suggestions for optimization (best times for high-priority tasks, etc.)

### AC3: Integration with Weekly Prep
- Pattern insights included in weekly prep workflow
- Historical pattern data available for review
- Trends visualized in briefings

---

## Technical Implementation

**Leverage Existing Infrastructure:**
- Pattern detection system (Story 1.8: src/patterns/)
- Task repository (EPIC-5R)
- Weekly summary generation (Story 3.6)

**New Components:**
- Domain service: TaskPatternAnalyzer
- Use case: AnalyzeProductivityPatternsUseCase
- Integration: Weekly prep workflow enhancement

---

## Definition of Done

- [ ] TaskPatternAnalyzer domain service created
- [ ] AnalyzeProductivityPatternsUseCase implemented
- [ ] 5+ tests passing
- [ ] Pattern insights integrated with weekly summary
- [ ] Committed to git

---

**Status:** Core implementation (minimal viable)
**Estimated Effort:** 8 points (1-2 days)
