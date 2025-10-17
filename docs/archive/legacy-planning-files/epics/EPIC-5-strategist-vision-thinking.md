# EPIC-5: Strategist (Vision & Strategic Thinking Agent)

**Status:** Not Started
**Priority:** P2 (Medium - Strategic Layer)
**Epic Owner:** Product Lead
**Business Value:** Long-term thinking partner - challenges assumptions, spots opportunities, ensures daily work aligns with vision

---

## Epic Goal

Build the Strategist agent (Vision) as a strategic thinking partner. This agent:
- Helps articulate and refine long-term vision
- Evaluates new opportunities systematically
- Challenges strategic assumptions
- War-games potential futures
- Ensures tactical work ladders up to strategy
- Facilitates monthly strategic reviews

---

## Success Criteria

- [ ] User can articulate clear long-term vision
- [ ] Opportunity evaluation provides useful framework
- [ ] Agent challenges thinking productively
- [ ] Monthly strategic reviews yield insights
- [ ] User feels strategic clarity (not just tactical busy-ness)
- [ ] Agent notices strategic drift

---

## Key Capabilities

### 1. Vision Definition
Help user articulate:
- **Why** the business exists (purpose)
- **What** success looks like (3-year, 5-year, 10-year)
- **Who** the business serves (ideal customer)
- **How** the business wins (competitive advantage)
- **Values** that guide decisions

### 2. Opportunity Evaluation
When new opportunities arise:
- Strategic fit assessment
- Resource requirements
- Risk/reward analysis
- Timing considerations
- Go/No-Go recommendation with reasoning

### 3. Scenario Planning
War-game potential futures:
- "What if we pivot to enterprise?"
- "What if competitor X launches Y?"
- "What if we raise funding vs bootstrapping?"
- Map out implications, identify decision points

### 4. Strategic Review (Monthly)
Scheduled check-ins:
- Are we still aligned with vision?
- What's changing in the market?
- What opportunities are we missing?
- What assumptions need challenging?

### 5. Competitive Intelligence
(If user provides data):
- Track competitor moves
- Identify market trends
- Spot threats early
- Suggest strategic responses

### 6. Strategic Drift Detection (Autonomous)
Notices when:
- Daily work doesn't align with stated strategy
- Decisions contradict stated values
- User considering opportunity outside core focus
- Goals don't ladder up to vision

---

## Agent Personality

**Name:** Vision (default, customizable)
**Icon:** 🔭

**Persona:**
- Experienced startup founder turned advisor
- Thinks 3-5 years out while staying practical
- Socratic method - asks questions that provoke insight
- Challenges sacred cows
- Pattern recognition across industries
- "What does winning look like?" is favorite question

**Communication Style:**
- Thoughtful, sometimes pauses to think
- Asks "why" repeatedly (5 whys method)
- Uses analogies and examples from other companies
- Comfortable with ambiguity and complexity
- Challenges gently but persistently
- Celebrates strategic clarity

---

## Autonomous Behaviors

### Scheduled Tasks
```yaml
scheduled:
  - day: "Last Friday of Month"
    time: "14:00"
    action: "prompt_strategic_review"
    output: "Monthly strategic check-in invitation"

  - day: "First of Quarter"
    time: "09:00"
    action: "strategic_alignment_check"
    output: "Do quarterly goals align with vision?"

  - frequency: "weekly"
    action: "scan_for_strategic_drift"
    output: "Flag misalignments to Chief of Staff"
```

### Event Monitors
```yaml
events:
  - trigger: "user_mentions_new_opportunity"
    action: "capture_for_evaluation"
    message: "Want to evaluate this opportunity together?"

  - trigger: "3_decisions_contradict_stated_strategy"
    action: "flag_strategic_drift"
    message: "I'm noticing a pattern - let's discuss strategy"

  - trigger: "competitor_mentioned_3_times"
    action: "suggest_competitive_analysis"

  - trigger: "goal_added_outside_focus_areas"
    action: "question_strategic_fit"

  - trigger: "major_market_event"  # If monitoring enabled
    action: "assess_strategic_implications"
```

### Learning Behaviors
```yaml
learns:
  - "User's decision-making values" (e.g., "Prioritizes growth over profit")
  - "Strategic blind spots" (areas user doesn't naturally consider)
  - "Risk tolerance" (conservative vs aggressive)
  - "Effective conversation depth" (high-level vs detailed analysis)
  - "Which frameworks resonate" (e.g., Blue Ocean, Jobs To Be Done)
```

---

## Core Workflows

### User-Initiated Workflows
1. **vision-session** - Define/refine long-term vision
2. **opportunity-eval** - Evaluate specific opportunity
3. **scenario-planning** - War-game a potential future
4. **strategic-review** - Monthly big-picture check
5. **competitive-analysis** - Understand positioning
6. **strategy-conversation** - Open-ended strategic thinking

### Autonomous Workflows
1. **strategic-drift-monitor** - Continuous alignment check
2. **monthly-review-prep** - Prepare for strategic review
3. **opportunity-backlog-review** - Periodically review captured opportunities

---

## Vision Session Workflow (Detailed)

```markdown
<workflow name="vision-session">

<step n="1" goal="Understand current state">
Let's start with where you are today.

Tell me about your business:
- What do you do?
- Who do you serve?
- What's working?
- What's not working?

I'm not judging, just understanding context.

<template-output>current_state</template-output>
</step>

<step n="2" goal="Purpose - the WHY">
Now the deeper question: WHY does this business exist?

Not "to make money" - that's a result.

What problem in the world are you solving?
What change are you trying to make?
What would be lost if this business didn't exist?

Take your time. This is the foundation.

<template-output>purpose</template-output>
<invoke-task halt="true">{project-root}/bmad/core/tasks/adv-elicit.xml</invoke-task>
</step>

<step n="3" goal="10-Year Vision - the WHAT">
Okay, now let's dream a bit.

It's 2035. Your business has succeeded beyond your wildest dreams.

What does that look like?
- How big is it? (Revenue, customers, team)
- What's different about the world?
- How do people describe your company?
- What are you known for?

Be specific. Paint the picture.

<template-output>ten_year_vision</template-output>
<invoke-task halt="true">{project-root}/bmad/core/tasks/adv-elicit.xml</invoke-task>
</step>

<step n="4" goal="3-Year Picture">
10 years is far. Let's make it concrete.

It's 2028 (3 years from now). You're on track to that 10-year vision.

What's true about your business?
- Revenue and profit?
- Number of customers?
- Team size?
- Product/service offerings?
- Market position?

Write it in present tense: "We have..."

<template-output>three_year_picture</template-output>
</step>

<step n="5" goal="Ideal Customer - the WHO">
Who are you building this for?

Not "everyone" - that's no one.

Describe your ideal customer in vivid detail:
- Demographics? (age, income, location, role)
- Psychographics? (values, fears, aspirations)
- Behaviors? (how they work, what frustrates them)
- Why do they choose you over alternatives?

<template-output>ideal_customer</template-output>
<invoke-task halt="true">{project-root}/bmad/core/tasks/adv-elicit.xml</invoke-task>
</step>

<step n="6" goal="Competitive Advantage - the HOW">
Why will you win?

Not "we'll work harder" - everyone works hard.

What's your unfair advantage?
- Unique insight about the market?
- Proprietary technology/process?
- Network effects?
- Brand/reputation?
- Team expertise?

What can you do that's hard for competitors to copy?

<template-output>competitive_advantage</template-output>
</step>

<step n="7" goal="Values - the FILTER">
What values guide your decisions?

These aren't aspirational posters - these are the principles you use when facing tough choices.

Examples:
- "Transparency over comfort" (we share bad news openly)
- "Long-term over short-term" (we turn down revenue that doesn't fit)
- "Customer success over growth" (we won't scale until product is excellent)

What are your 3-5 core values?

<template-output>core_values</template-output>
</step>

<step n="8" goal="Strategy - the FOCUS">
Given everything we've discussed, what should you focus on?

What will you do?
What will you NOT do?

Strategy is as much about what you say NO to.

<template-output>strategic_focus</template-output>
</step>

<step n="9" goal="Reality Check">
Okay, let's test this.

Based on this vision:
- Does your current goal set align?
- Are you saying NO to the right things?
- Is your team structured correctly?
- Are you investing in the right areas?

What needs to change to align with this vision?

<template-output>alignment_check</template-output>
</step>

<step n="10" goal="Generate Vision Document">
Excellent work. This is deep thinking.

I'm generating your Strategic Vision document...

[Agent creates structured document]

Saved to: {output_folder}/Strategic-Vision.md

I'll check in monthly to ensure we're staying aligned.

And when you're considering new opportunities, I'll evaluate them against this vision.

<template-output>vision_document</template-output>
</step>

</workflow>
```

---

## Opportunity Evaluation Workflow

```markdown
<workflow name="opportunity-eval">

<step n="1" goal="Describe opportunity">
Tell me about this opportunity.

What is it?
Who brought it to you?
What's the potential upside?

<template-output>opportunity_description</template-output>
</step>

<step n="2" goal="Strategic Fit">
Let's evaluate against your vision and strategy.

[Agent loads Strategic Vision document]

Your stated focus is: {strategic_focus}
Your ideal customer is: {ideal_customer}
Your competitive advantage is: {competitive_advantage}

How does this opportunity align?
- Does it serve your ideal customer?
- Does it leverage your advantage?
- Does it move you toward 3-year vision?

Score: 1-10 on strategic fit

<template-output>strategic_fit</template-output>
</step>

<step n="3" goal="Resource Requirements">
What would this require?
- Time (yours and team's)?
- Money (budget, investment)?
- People (hiring, reallocation)?
- Technology (new tools, platforms)?

Be realistic. Opportunity cost is real.

<template-output>resources</template-output>
</step>

<step n="4" goal="Risk Assessment">
What could go wrong?

Best case scenario?
Worst case scenario?
Most likely scenario?

Can you afford the worst case?

<template-output>risk_assessment</template-output>
</step>

<step n="5" goal="Timing">
Is this the right time?

- Market timing (is market ready?)
- Company readiness (do you have capacity?)
- Competitive timing (first mover vs fast follower?)

What happens if you wait 6 months?

<template-output>timing</template-output>
</step>

<step n="6" goal="Recommendation">
Based on this analysis:

**Strategic Fit:** {fit_score}/10
**Resource Impact:** {resources_summary}
**Risk Level:** {risk_level}
**Timing:** {timing_assessment}

My recommendation: {GO | NO-GO | MAYBE}

Reasoning: {explanation}

**If GO:**
- Do this first: {next_step}
- Success looks like: {success_criteria}
- Review in: {review_date}

**If NO-GO:**
- Why not now: {reasoning}
- Revisit when: {conditions}

**If MAYBE:**
- Need more information on: {questions}
- Run this experiment: {test_suggestion}

What do you think?

<template-output>recommendation</template-output>
</step>

</workflow>
```

---

## User Stories (High-Level)

1. **Vision Definition**
   - Articulate purpose (why)
   - Define long-term vision (10-year, 3-year)
   - Identify ideal customer
   - Clarify competitive advantage

2. **Opportunity Evaluation**
   - Systematic assessment framework
   - Strategic fit analysis
   - Go/No-Go recommendations

3. **Scenario Planning**
   - War-game potential futures
   - Map implications
   - Identify decision points

4. **Monthly Strategic Review**
   - Scheduled check-ins
   - Alignment assessment
   - Market/competitive updates

5. **Strategic Drift Detection**
   - Monitor decisions vs stated strategy
   - Flag misalignments
   - Prompt corrective conversations

6. **Competitive Analysis**
   - Understand market positioning
   - Track competitor moves
   - Suggest strategic responses

---

## Integration Points

**Memory System (EPIC-1):**
- Stores vision and strategy
- Tracks strategic decisions
- Learns user's strategic thinking patterns

**Planner Agent (EPIC-4):**
- Goals should align with strategic vision
- Quarterly planning informed by strategy

**Chief of Staff (EPIC-2):**
- Routes strategic questions to Vision
- Includes strategic insights in briefings

**Operator Agent (EPIC-3):**
- Daily work should ladder up to strategic goals

---

## Dependencies

- EPIC-1 (Autonomous Agent Framework) - Required
- Vision/strategy storage system
- Opportunity tracking system

---

## Risks & Mitigations

**Risk:** Strategic conversations too abstract, not actionable
**Mitigation:** Always end with concrete next steps

**Risk:** User doesn't have time for strategic thinking
**Mitigation:** Start with 30-min monthly reviews, expand if valuable

**Risk:** Agent's recommendations ignored
**Mitigation:** Track recommendations and outcomes, improve over time

---

## Acceptance Criteria for Epic

- [ ] User completes vision session successfully
- [ ] Vision document feels meaningful and useful
- [ ] Opportunity evaluation provides clear recommendation
- [ ] At least one strategic insight surfaced in first month
- [ ] User references vision when making decisions
- [ ] Monthly strategic reviews scheduled and completed

---

## Stories in Epic

- STORY-5.1: Strategist agent persona and definition
- STORY-5.2: Vision session workflow
- STORY-5.3: Vision document template
- STORY-5.4: Opportunity evaluation workflow
- STORY-5.5: Scenario planning workflow
- STORY-5.6: Monthly strategic review workflow
- STORY-5.7: Strategic drift detection (autonomous)
- STORY-5.8: Opportunity backlog management
- STORY-5.9: Competitive analysis framework
- STORY-5.10: Learning system for strategic patterns

---

## Estimated Effort

**Epic Total:** 30-40 story points (approx. 2-3 weeks)

**Complexity:** High - Strategic thinking is nuanced

**Value:** High - Differentiates busy-ness from meaningful progress
