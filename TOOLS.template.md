# TOOLS.template.md — Local Notes

Skills define *how* tools work. This file is for *your* specifics — the stuff that's unique to your setup.

## Installed Skills (example)

| Skill | Path | Purpose |
|-------|------|---------|
| reasoning-upgrade | `skills/reasoning-upgrade/SKILL.md` | Reasoning, execution & verification rules |
| self-improving | `skills/self-improving/SKILL.md` | Self-reflection, error learning, tiered memory |
| tavily | `skills/tavily/SKILL.md` | AI-optimized web search |
| agent-browser | `skills/{{BROWSER_SKILL_DIR}}/SKILL.md` | Browser automation |
| find-skills | `skills/{{FIND_SKILLS_DIR}}/SKILL.md` | Discover new skills |
| skill-vetter | `skills/{{VETTER_SKILL_DIR}}/SKILL.md` | Security check before install |

*Add your own skills following the same pattern.*

## What Goes Here

Things like:
- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- API keys / environment variable names (not values)
- Any environment-specific setup

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

## Directory Structure (expected)

```
woodyard/
├── skills/               # Installed skills (each in its own dir)
├── memory/               # Daily notes + long-term memory
├── scripts/              # Utility scripts
├── self-improving/       # Execution improvement logs
├── restore_backups/      # Auto-backups for self-healing
├── SOUL.md               # Agent personality
├── AGENTS.template.md    # Workspace conventions
├── HEARTBEAT.template.md # Heartbeat procedures
├── self_check.py         # Startup health check
├── woodward/             # Self-check & self-heal module
├── uqlm_scorer.py        # Hallucination detection
└── knowledge_cache.py    # API result caching
```

---

*Template placeholders: `{{BROWSER_SKILL_DIR}}`, `{{FIND_SKILLS_DIR}}`, `{{VETTER_SKILL_DIR}}` — replace with your actual skill directory names.*
