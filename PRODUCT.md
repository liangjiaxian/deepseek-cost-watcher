# Product

## Register

product

## Users

Developers and engineering managers who use DeepSeek APIs in production. Their context is operational — checking cost trends, investigating spikes, reconciling daily spend, configuring alerts. They work in a mix of environments: a dim room at 2am during an incident, or a bright office during morning standup. They need answers fast, not exploration.

## Product Purpose

DeepSeek Monitor tracks API usage and cost across accounts in real time. It surfaces balance trends, per-model cost breakdowns, daily/weekly reports, and scheduler health. Success is a developer spending under 10 seconds to answer "what did we spend yesterday and is anything broken."

## Brand Personality

Precise, unfussy, serious. Voice is concise and numeric — labels not sentences. Tone is neutral and factual; the interface never exaggerates. The personality is "the tool disappears into the task."

## Anti-references

- Over-designed "SaaS landing page" dashboards with gradient stats and glass cards
- Dark-first tools that use dark blue as a lazy default (Datadog, Grafana style)
- Cluttered DevOps UIs with 47 widgets, each screaming for attention
- White-label admin panels with rounded corners on everything and heavy shadows

## Design Principles

1. **Answers, not dashboards.** Every screen answers one question. If it answers two, split it. If it answers zero, remove it.
2. **Numbers first.** Data is typography. Values get the strongest weight and the most space. Labels and decorations are visually subordinate.
3. **Dark is for flow, light is for context.** Dark mode suits prolonged use and low-light monitoring. Light mode suits shared review and daytime reading. Neither is default; the user chooses.
4. **Earned familiarity.** Standard navigation, standard affordances, standard component vocabulary. The interface is trustworthy because nothing surprises.
5. **No state anxiety.** Every loading state has a skeleton. Every empty state teaches. Every error state offers recovery. The user is never left wondering whether the tool is working.

## Accessibility & Inclusion

- WCAG 2.2 AA minimum for both themes
- Reduced motion media query respected; only essential transitions retained
- High contrast not required as a separate mode — the light theme already serves situational contrast needs
