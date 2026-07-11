# HEARTBEAT.template.md

## ⚠️ Heartbeat — First Thing
**Each heartbeat restart, run `python self_check.py` first.**
Then proceed with other checks.

## Quick Checks (rotate 2-4x/day)
- Email — any urgent unread?
- Calendar — upcoming events in next 24-48h?
- Weather — relevant if going out?

## Knowledge Cache — API Result Caching
**Auto-run after every `web_search` / `web_fetch`.**
```
from knowledge_cache import kc
kc.store(topic, content, source="web_search")
```
- Store results on fetch, read locally next time
- Clean up temp files immediately after use

## Optional: Custom Project Updates (embedded in heartbeat)
**Run in your agent's heartbeat session only, avoid external schedulers.**
Example pattern:
```
python your_project_script.py --check  # check if stale
# Returns STALE → run full update
# Returns FRESH → skip
```

Guard conditions (prevent hangs):
- Session running >30 seconds
- Last check >2 hours ago
- Not during quiet hours (23:00-07:00)

## Woodward Auto-Tasks (runs with heartbeat)
**Import-based, zero overhead in same process.**
Alert `{{OWNER_NAME}}` on findings.

Flow (inside heartbeat):
```
from woodward import Woodward
core = Woodward()
alerts = core.auto_tasks(skip_if_recent=True)
if alerts:
    # notify owner
```

Tasks:
- **audit_backups()** — Check backup count, age, cleanup needs
- **daily_report()** — Daily log distillation, health score
- **health_check()** — Memory integrity + backup existence + error accumulation

Guard conditions:
- Session running >30 seconds
- Last run >2 hours ago
- Not during quiet hours (23:00-07:00)

## Self-Check (session start + heartbeat)
**On start:** `python self_check.py` → verify SOUL/MEMORY/self-improving/HEARTBEAT integrity
   - Issues found → `auto_restart()` auto-recover → reload → notify `{{OWNER_NAME}}`
   - All within 300 seconds
**On heartbeat:** `from self_check import self_reflection; self_reflection()` → check recent anomalies
- Alert on findings
- Silent on pass

## Self-Improving Check (weekly)
- Read `skills/self-improving/heartbeat-rules.md`
- Check if `self-improving/memory.md` needs compaction
- If nothing changed since last check → HEARTBEAT_OK

## Memory Maintenance (weekly)
- Review recent `memory/YYYY-MM-DD.md` for notable events
- Update `MEMORY.md` with distilled learnings
- Remove outdated info

---

*Template placeholders: `{{OWNER_NAME}}` — replace with your values.*
