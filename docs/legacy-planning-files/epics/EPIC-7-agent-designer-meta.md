# EPIC-7: Agent Designer (Meta-Capability)

**Status:** Not Started
**Priority:** P3 (Lower - Advanced Feature)
**Epic Owner:** Technical Lead
**Business Value:** Self-extending system - create custom specialist agents on-demand for any business function

---

## Epic Goal

Build the Agent Designer workflow that allows users to create custom specialist agents dynamically. This enables:
- Define new agent for any business function
- Generate agent specification automatically
- Deploy agent to Mission Control team instantly
- Extend system without coding

**This is the "meta" capability that makes Mission Control infinitely extensible.**

---

## Success Criteria

- [ ] User can design custom agent through conversation
- [ ] Agent specification generated automatically
- [ ] New agent deploys and works immediately
- [ ] At least one custom agent created successfully
- [ ] User understands how to create more agents
- [ ] System maintains quality/consistency

---

## Key Capabilities

### 1. Agent Design Conversation
Guide user through defining:
- What role/function does agent serve?
- What expertise does agent need?
- What personality/communication style?
- What workflows/commands should agent have?
- What should agent know (sidecar files)?

### 2. Specification Generation
Automatically create:
- Agent YAML definition
- Persona (role, identity, communication style, principles)
- Menu commands
- Sidecar files (if needed)
- Integration points with other agents

### 3. Agent Deployment
- Save agent to module
- Update agent manifest
- Make available immediately
- Test basic functionality

### 4. Quality Assurance
Ensure new agents:
- Follow Mission Control patterns
- Integrate with memory system
- Have clear responsibilities
- Don't duplicate existing agents

---

## Use Cases

### Example 1: CFO Agent
**User Need:** "I need help with financial planning and budgeting"

**Agent Designer Creates:**
- **Role:** Chief Financial Officer
- **Expertise:** Financial modeling, budgeting, cash flow, fundraising
- **Personality:** Conservative, asks tough questions about spending
- **Workflows:**
  - monthly-budget-review
  - cash-flow-projection
  - fundraising-prep
  - expense-analysis
- **Sidecar:** Financial rules, company financial history
- **Autonomous:** Monitors burn rate, alerts when runway < 6 months

### Example 2: Sales Agent
**User Need:** "I need help managing sales pipeline and closing deals"

**Agent Designer Creates:**
- **Role:** VP of Sales
- **Expertise:** Pipeline management, deal strategy, objection handling
- **Personality:** Optimistic but realistic, competitive, coach-like
- **Workflows:**
  - pipeline-review
  - deal-strategy
  - outreach-planning
  - win-loss-analysis
- **Autonomous:** Tracks deal stages, reminds of follow-ups

### Example 3: HR/People Agent
**User Need:** "I need help with hiring and team development"

**Agent Designer Creates:**
- **Role:** Head of People
- **Expertise:** Recruiting, onboarding, performance management, culture
- **Personality:** Empathetic, process-oriented, culture guardian
- **Workflows:**
  - role-definition
  - candidate-evaluation
  - onboarding-plan
  - performance-review
  - team-survey
- **Autonomous:** Reminds of performance reviews, tracks hiring pipeline

---

## Agent Design Workflow

```markdown
<workflow name="agent-designer">

<step n="1" goal="Identify need">
What business function do you need help with?

Examples:
- Financial planning (CFO)
- Sales management (VP Sales)
- Marketing strategy (CMO)
- Product development (CPO)
- People/HR (Head of People)
- Customer success
- Operations

Or something else?

<template-output>function</template-output>
</step>

<step n="2" goal="Define role">
Great, let's design a {function} agent for you.

What should this agent do?

Be specific about:
- Main responsibilities
- Key decisions this agent helps with
- Types of conversations you'll have
- What success looks like

<template-output>role_definition</template-output>
<invoke-task halt="true">{project-root}/bmad/core/tasks/adv-elicit.xml</invoke-task>
</step>

<step n="3" goal="Define expertise">
What expertise should this agent have?

Think about:
- Domain knowledge (what should they know deeply?)
- Frameworks/methodologies (what tools should they use?)
- Industry experience
- Specific skills

<template-output>expertise</template-output>
</step>

<step n="4" goal="Design personality">
What personality works best for this role?

Consider:
- Communication style (formal vs casual, direct vs diplomatic)
- Approach (analytical vs intuitive, cautious vs aggressive)
- Values (what does this agent optimize for?)
- Quirks (anything that makes them memorable?)

Examples:
- CFO: "Conservative, asks tough questions, protects cash"
- Sales: "Optimistic, competitive, coach-like"
- HR: "Empathetic, process-oriented, culture guardian"

<template-output>personality</template-output>
</step>

<step n="5" goal="Define workflows">
What workflows should this agent facilitate?

What are the main processes or conversations?

For a CFO example:
- monthly-budget-review
- cash-flow-projection
- fundraising-prep
- expense-analysis

What does your {function} agent need?

<template-output>workflows</template-output>
<invoke-task halt="true">{project-root}/bmad/core/tasks/adv-elicit.xml</invoke-task>
</step>

<step n="6" goal="Autonomous behaviors">
Should this agent work autonomously?

What should it monitor or track?
When should it proactively notify you?

For a CFO example:
- Monitor burn rate daily
- Alert when runway < 6 months
- Remind of monthly financial review
- Flag large unexpected expenses

What about your agent?

<template-output>autonomous_behaviors</template-output>
</step>

<step n="7" goal="Domain knowledge">
Does this agent need specialized knowledge?

This would go in sidecar files:
- Methodologies/frameworks
- Company-specific context
- Historical decisions
- Best practices

Should we create sidecar files for this agent?

<template-output>sidecar_decision</template-output>
</step>

<step n="8" goal="Integration points">
How does this agent work with others?

- Should Chief of Staff route certain questions here?
- Does this agent need data from Analyst?
- Should this agent inform Planner about goals?
- Link to Operator for tasks?

<template-output>integrations</template-output>
</step>

<step n="9" goal="Generate agent specification">
Excellent! I have everything I need.

Generating agent specification...

[Agent creates:
- Agent YAML file
- Persona definition
- Menu commands
- Sidecar files (if needed)
- Integration hooks]

Agent Name: {suggested_name}
Icon: {suggested_icon}
Module: mission-control/agents/{agent_id}

Review the specification:

{display agent spec}

Look good?

<template-output>agent_spec</template-output>
</step>

<step n="10" goal="Deploy agent">
<check if="user approves">
  <action>Save agent files</action>
  <action>Update agent manifest</action>
  <action>Test basic loading</action>

  🎉 Your {agent_name} agent is ready!

  You can now:
  - Load the agent: @{agent_file}
  - Try commands: *help
  - Chief of Staff will route questions automatically

  Want to create workflows for this agent now, or later?

  <template-output>deployment_complete</template-output>
</check>

<check if="user wants changes">
  <goto step="9">Let's revise</goto>
</check>
</step>

<step n="11" goal="Create first workflow (optional)">
Let's create one workflow to get started.

Which workflow from your list should we build first?

{display workflow list}

[Agent guides through workflow creation using workflow-creation-guide patterns]

<template-output>first_workflow</template-output>
</step>

</workflow>
```

---

## Agent Template Generation

The system generates a complete agent YAML:

```yaml
# {Function} Agent Definition
# Generated by Agent Designer: {date}

agent:
  metadata:
    id: "bmad/mission-control/agents/{agent_id}.md"
    name: "{Name}"
    title: "{Title}"
    icon: "{Icon}"
    module: "mission-control"
    custom_agent: true
    created: "{date}"
    created_by: "agent-designer"

  persona:
    role: "{Generated from user input}"
    identity: "{Generated from expertise and experience}"
    communication_style: "{Generated from personality}"
    principles:
      - "{Generated from values}"
      - "{Generated from approach}"

  critical_actions:
    - "Load into memory {project-root}/bmad/mission-control/config.yaml"
    - "Remember the user's name is {user_name}"
    - "ALWAYS communicate in {communication_language}"
    # Sidecar files if applicable
    # - critical: "MANDATORY"
    #   action: "Load COMPLETE file {agent-folder}/{sidecar_file}.md"

  autonomous_capabilities:
    scheduled_tasks:
      # Generated from autonomous behaviors
    event_monitors:
      # Generated from autonomous behaviors
    learning:
      # Standard learning behaviors

  menu:
    # Generated from workflows
    - trigger: "{workflow_1}"
      workflow: "{project-root}/bmad/mission-control/workflows/{workflow_1}/workflow.yaml"
      description: "{Description}"
```

---

## User Stories (High-Level)

1. **Agent Design Conversation**
   - Define role and function
   - Specify expertise
   - Design personality
   - Identify workflows

2. **Specification Generation**
   - Auto-generate agent YAML
   - Create persona
   - Define menu commands
   - Create sidecar files if needed

3. **Agent Deployment**
   - Save to module
   - Update manifests
   - Make immediately available

4. **Workflow Creation**
   - Guide through first workflow
   - Use workflow creation patterns
   - Link to agent menu

5. **Quality Assurance**
   - Validate agent definition
   - Check for duplicates
   - Ensure integration points

6. **Agent Management**
   - List custom agents
   - Edit/update agents
   - Disable/remove agents

---

## Integration Points

**Chief of Staff (EPIC-2):**
- Updates routing rules for new agents
- Includes new agents in briefings

**All Agents:**
- New agents integrate with memory system
- New agents can coordinate with existing agents

**Memory System (EPIC-1):**
- New agents use persistent memory
- Custom agent state tracked

---

## Dependencies

- EPIC-1 (Autonomous Agent Framework) - Required
- EPIC-2 (Chief of Staff) - For routing updates
- All 5 core agents operational first
- Understanding of agent patterns

---

## Risks & Mitigations

**Risk:** User creates too many redundant agents
**Mitigation:** Agent Designer checks for duplicates, suggests using existing

**Risk:** Generated agents are low quality
**Mitigation:** Template system ensures consistency, user reviews before deploy

**Risk:** Custom agents break system
**Mitigation:** Validation before deployment, sandbox testing

---

## Acceptance Criteria for Epic

- [ ] User completes agent design conversation
- [ ] Agent specification generated and looks reasonable
- [ ] New agent deploys successfully
- [ ] New agent loads and responds
- [ ] Chief of Staff routes to new agent correctly
- [ ] User creates at least one custom agent

---

## Stories in Epic

- STORY-7.1: Agent design workflow
- STORY-7.2: Agent specification generator
- STORY-7.3: Agent YAML template system
- STORY-7.4: Persona generation logic
- STORY-7.5: Workflow stub generation
- STORY-7.6: Sidecar file creation
- STORY-7.7: Agent deployment system
- STORY-7.8: Manifest update automation
- STORY-7.9: Agent validation/QA
- STORY-7.10: Custom agent management (list, edit, disable)

---

## Estimated Effort

**Epic Total:** 30-40 story points (approx. 2-3 weeks)

**Complexity:** High - Meta-programming, template generation

**Value:** Very High - Makes system infinitely extensible

---

## Future Enhancements

- **Agent Marketplace:** Share custom agents with community
- **Agent Templates:** Pre-built agents for common functions (CFO, VP Sales, CMO, etc.)
- **Agent Learning:** Custom agents improve over time
- **Team Agents:** Agents that coordinate multiple people
