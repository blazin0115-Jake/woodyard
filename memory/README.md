# memory/ — Tiered Memory System

Woodyard uses a **three-tier memory architecture** to balance recency, durability, and continuous improvement.

## The Three Tiers

```
┌──────────────────────────────────┐
│  Tier 1: Daily Notes             │
│  memory/YYYY-MM-DD.md            │
│  Raw logs — what happened today   │
├──────────────────────────────────┤
│  Tier 2: Long-Term Memory        │
│  MEMORY.md                        │
│  Curated wisdom — distilled from  │
│  daily notes over time            │
├──────────────────────────────────┤
│  Tier 3: Self-Improving           │
│  self-improving/                  │
│  Execution lessons — what works,  │
│  what doesn't, corrections        │
└──────────────────────────────────┘
```

### Tier 1 — Daily Notes (`memory/YYYY-MM-DD.md`)
- Created per session, one file per day
- Raw factual logs: decisions made, context captured, events that happened
- Short, high-signal entries — not a full transcript
- Survives session restarts for later review

### Tier 2 — Long-Term Memory (`MEMORY.md`)
- Reviewed and updated periodically (weekly or more often)
- Distilled from daily notes — the curated essence
- Identity, preferences, recurring context, key decisions
- **Only loaded in main session** (direct user chat), not shared contexts

### Tier 3 — Self-Improving (`self-improving/`)
- Compound execution quality over time
- `corrections.md` — explicit user corrections
- `memory.md` — reusable global rules
- `domains/<domain>.md` — domain-specific lessons
- `projects/<project>.md` — project-specific overrides
- Inferred rules are marked tentative until human validation

## Design Principles

1. **Recency first** — Daily notes are the freshest signal
2. **Distillation, not duplication** — MEMORY.md is a summary, not a log
3. **Domain isolation** — Keep lessons scoped to prevent cross-domain interference
4. **Tentative → confirmed** — AI-inferred rules start tentative, only hardened by human validation
5. **Write to survive** — "Mental notes" don't survive restarts. Files do.

## Usage Flow

```
Session start → Read today's + yesterday's daily notes
              → Read MEMORY.md (main session only)
              → Load relevant self-improving lessons
              → Execute
Session end   → Write to daily notes what happened
```

---

*The `memory/` directory in this repository is a structural template. Actual daily notes contain personal conversation history and are not included in the public repository.*
