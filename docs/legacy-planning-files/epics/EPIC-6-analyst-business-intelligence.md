# EPIC-6: Analyst (Business Intelligence Agent)

**Status:** Not Started
**Priority:** P2 (Medium - Intelligence Layer)
**Epic Owner:** Technical Lead
**Business Value:** Data-driven insights - helps understand what's working, what's not, and why

---

## Epic Goal

Build the Analyst agent (Data) that tracks metrics, identifies trends, and surfaces insights. This agent:
- Tracks key business metrics autonomously
- Identifies trends and anomalies
- Answers data questions instantly
- Surfaces insights proactively
- Helps define what to measure
- Creates simple dashboards

---

## Success Criteria

- [ ] User can define metrics to track
- [ ] Metrics updated regularly (manual or automated)
- [ ] Trends identified automatically
- [ ] Weekly metrics review is useful
- [ ] At least one proactive insight per week
- [ ] User makes data-informed decisions

---

## Key Capabilities

### 1. Metrics Definition
Help user define what to track:
- Revenue metrics (MRR, ARR, growth rate)
- Customer metrics (acquisition, churn, LTV)
- Operational metrics (conversion rates, cycle times)
- Financial metrics (burn rate, runway, margins)
- Custom metrics (user-defined)

### 2. Data Tracking
- Manual entry (user provides numbers)
- Automated (integrations if available)
- Historical tracking
- Trend calculation

### 3. Trend Analysis
Automatically detect:
- Growth/decline trends
- Anomalies (unexpected spikes/drops)
- Patterns (seasonal, cyclical)
- Correlations between metrics

### 4. Insights Generation (Autonomous)
Proactively surface:
- "Revenue up 15% this month"
- "Churn rate increasing - investigate?"
- "Conversion rate highest on Tuesdays"
- "Runway down to 8 months - time to fundraise?"

### 5. Dashboard Creation
Simple visual dashboards:
- Key metrics at a glance
- Trend lines
- Status indicators (on-track, at-risk)
- Comparison to goals/targets

### 6. Data Storytelling
Explain what numbers mean:
- Not just "revenue is $50K"
- But "Revenue is $50K, up 20% from last month, on track for Q4 goal of $200K"

---

## Agent Personality

**Name:** Data (default, customizable)
**Icon:** 📈

**Persona:**
- Data scientist turned business analyst
- Finds patterns others miss
- Numbers tell stories
- Curious about "why" behind metrics
- Pragmatic about measurement ("perfect is enemy of good")
- Celebrates wins visible in data

**Communication Style:**
- Clear data visualizations
- Context with every number
- "Here's what I see" phrasing
- Asks probing questions about anomalies
- Translates complex data to simple insights
- Always includes "so what?" (implication)

---

## Autonomous Behaviors

### Scheduled Tasks
```yaml
scheduled:
  - day: "Monday"
    time: "06:00"
    action: "generate_weekly_metrics_report"
    output: "Weekly metrics for Chief of Staff briefing"

  - day: "First of Month"
    time: "09:00"
    action: "generate_monthly_report"
    output: "Monthly metrics deep-dive"

  - frequency: "daily"
    action: "check_metrics_for_anomalies"
    output: "Flag unusual changes"
```

### Event Monitors
```yaml
events:
  - trigger: "metric_drops_20_percent"
    action: "investigate_and_notify"
    message: "[Metric] dropped 20% - need to investigate?"

  - trigger: "metric_hits_goal"
    action: "celebrate"
    message: "🎉 You hit your [metric] goal!"

  - trigger: "trend_reversal"
    action: "flag_pattern_change"
    message: "[Metric] trend reversed - from growing to declining"

  - trigger: "7_days_no_metric_update"
    action: "remind"
    message: "Haven't updated metrics in 7 days - need data"

  - trigger: "runway_below_6_months"
    action: "urgent_alert"
    message: "⚠️ Runway critical - only X months left"
```

### Learning Behaviors
```yaml
learns:
  - "Which metrics user cares about most"
  - "Normal variance vs real anomaly"
  - "Reporting preference" (detail level, visualization style)
  - "Decision triggers" (what numbers drive actions)
```

---

## Metrics Data Model

```yaml
metric:
  id: "METRIC-001"
  name: "Monthly Recurring Revenue (MRR)"
  category: "revenue"  # revenue, customer, operational, financial
  unit: "dollars"
  frequency: "monthly"  # daily, weekly, monthly

  current_value: 15000
  previous_value: 12500
  change_percent: 20
  trend: "up"  # up, down, flat

  goal:
    target: 20000
    timeframe: "Q4 2025"
    progress_percent: 75

  history:
    - date: "2025-10-01"
      value: 15000
    - date: "2025-09-01"
      value: 12500
    - date: "2025-08-01"
      value: 11000

  insights:
    - "Up 20% MoM - strong growth"
    - "On track for Q4 goal of $20K"
    - "Need $5K more growth in 2 months"

  status: "on_track"  # on_track, at_risk, off_track
  last_updated: "2025-10-14"
  updated_by: "manual"  # manual, automated, integration
```

---

## Core Workflows

### User-Initiated Workflows
1. **metrics-setup** - Define what to track
2. **metric-update** - Enter new data
3. **weekly-review** - Review metrics together
4. **deep-dive** - Investigate specific metric
5. **dashboard-create** - Build custom dashboard
6. **trend-analysis** - Understand pattern

### Autonomous Workflows
1. **weekly-report-generator** - Monday morning summary
2. **anomaly-detector** - Continuous monitoring
3. **insight-generator** - Surface patterns
4. **goal-progress-tracker** - Check metrics vs goals

---

## Metrics Setup Workflow

```markdown
<workflow name="metrics-setup">

<step n="1" goal="Understand business">
Let's figure out what you should be measuring.

Tell me about your business model:
- How do you make money?
- What's your growth stage?
- What keeps you up at night?

<template-output>business_context</template-output>
</step>

<step n="2" goal="Suggest core metrics">
Based on that, here are metrics I recommend tracking:

**Revenue Metrics:**
- Monthly Revenue
- Revenue Growth Rate

**Customer Metrics:**
- New Customers Acquired
- Customer Churn Rate
- Customer Lifetime Value (LTV)

**Operational Metrics:**
- Conversion Rate
- Average Deal Size

**Financial Metrics:**
- Monthly Burn Rate
- Cash Runway

Do these make sense? What would you add/remove?

<template-output>recommended_metrics</template-output>
</step>

<step n="3" goal="Define each metric">
For each metric, let's define:
- How do you calculate it?
- How often will you update it?
- What's your goal/target?
- Where does the data come from?

<template-output>metric_definitions</template-output>
<invoke-task halt="true">{project-root}/bmad/core/tasks/adv-elicit.xml</invoke-task>
</step>

<step n="4" goal="Set update cadence">
How often will you update these?

I suggest:
- Revenue metrics: Monthly
- Customer metrics: Monthly
- Financial metrics: Monthly
- Operational metrics: Weekly (if available)

I'll remind you if metrics go stale.

<template-output>update_cadence</template-output>
</step>

<step n="5" goal="Historical baseline">
Do you have historical data?

If yes, let's input last 3-6 months so I can establish trends.
If no, no problem - we'll start tracking from today.

<template-output>historical_data</template-output>
</step>

<step n="6" goal="Create dashboard">
Perfect. I'm creating your Metrics Dashboard.

Saved to: {output_folder}/Metrics-Dashboard.md

I'll update this automatically as you provide data.

Every Monday, I'll include key metrics in your briefing.

<template-output>dashboard</template-output>
</step>

</workflow>
```

---

## Weekly Metrics Review Workflow

```markdown
<workflow name="weekly-metrics-review">

<step n="1" goal="Present this week's numbers">
Here are your key metrics for the week ending {date}:

**Revenue:**
- Monthly Revenue: $15,000 (↑ 20% vs last month)
- On track for Q4 goal: 75% progress

**Customers:**
- New Customers: 5 (target: 10, ⚠️ below goal)
- Churn: 2% (good, below 5% threshold)

**Operations:**
- Conversion Rate: 12% (↑ from 10% last week)
- Average Deal: $3,000 (↓ from $3,500)

**Financial:**
- Burn Rate: $8,000/month (stable)
- Runway: 12 months (healthy)

What stands out to you?

<template-output>metrics_presentation</template-output>
</step>

<step n="2" goal="Highlight insights">
Here's what I notice:

**🎉 Wins:**
- Revenue growing strongly (+20%)
- Conversion rate improving

**⚠️ Watch:**
- Customer acquisition below target (5 vs 10)
- Average deal size dropping

**🔍 Questions:**
- What's driving conversion rate improvement?
- Why are deals getting smaller?
- Should we focus on volume or deal size?

<template-output>insights</template-output>
</step>

<step n="3" goal="Investigate anomalies">
Let's dig into customer acquisition.

You're at 5 new customers vs target of 10.

What's the blocker?
- Lead generation?
- Conversion?
- Sales capacity?
- Something else?

<template-output>investigation</template-output>
</step>

<step n="4" goal="Actions">
Based on this review, what actions should we take?

Suggestions:
1. Investigate why deals are getting smaller
2. Review customer acquisition strategy
3. Celebrate the conversion rate win (what worked?)

What do you want to focus on?

<template-output>actions</template-output>
</step>

<step n="5" goal="Update goals if needed">
Any metrics goals need adjusting?

Sometimes reality teaches us our targets were wrong.

<template-output>goal_updates</template-output>
</step>

</workflow>
```

---

## User Stories (High-Level)

1. **Metrics Setup**
   - Define metrics to track
   - Set goals/targets
   - Establish update cadence

2. **Data Entry**
   - Manual metric updates
   - Historical data import
   - Bulk updates

3. **Dashboard Creation**
   - Visual metrics display
   - Trend lines
   - Status indicators

4. **Weekly Review**
   - Structured metrics review
   - Insight generation
   - Action identification

5. **Trend Analysis**
   - Identify patterns
   - Detect anomalies
   - Explain changes

6. **Proactive Insights**
   - Autonomous monitoring
   - Alert on anomalies
   - Surface correlations

7. **Integration (Future)**
   - Connect to data sources
   - Automated updates
   - Real-time tracking

---

## Integration Points

**Memory System (EPIC-1):**
- Stores all metrics and history
- Learns normal patterns

**Chief of Staff (EPIC-2):**
- Provides metrics for daily briefings
- Routes data questions to Analyst

**Planner Agent (EPIC-4):**
- Links metrics to goals
- Tracks goal progress via metrics

**Operator Agent (EPIC-3):**
- Provides task completion data

---

## Dependencies

- EPIC-1 (Autonomous Agent Framework) - Required
- Metrics storage system
- Trend calculation algorithms

---

## Risks & Mitigations

**Risk:** User doesn't have data to input
**Mitigation:** Start simple, help user establish tracking

**Risk:** Too many metrics = noise
**Mitigation:** Recommend 5-10 core metrics max

**Risk:** Insights ignored
**Mitigation:** Link insights to actions, track outcomes

---

## Acceptance Criteria for Epic

- [ ] User defines 5-10 core metrics
- [ ] Metrics tracked over time
- [ ] Weekly metrics review provides value
- [ ] At least one trend identified
- [ ] At least one proactive insight surfaces issue
- [ ] User references metrics when making decisions

---

## Stories in Epic

- STORY-6.1: Analyst agent persona and definition
- STORY-6.2: Metrics data model
- STORY-6.3: Metrics setup workflow
- STORY-6.4: Manual metric entry
- STORY-6.5: Dashboard generation
- STORY-6.6: Trend analysis algorithms
- STORY-6.7: Anomaly detection
- STORY-6.8: Weekly metrics review workflow
- STORY-6.9: Insight generation (autonomous)
- STORY-6.10: Integration framework (future)

---

## Estimated Effort

**Epic Total:** 25-35 story points (approx. 2 weeks)

**Complexity:** Medium - Data + visualization

**Value:** High - Data-driven decision making
