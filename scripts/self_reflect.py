"""
Self-Reflection Script — runs every 30 minutes.
- Reads corrections.md for known mistakes
- Reads recent session logs (last 2 hours) for potential errors
- Produces a reflection report

Zero API calls, zero dependencies (os, re, datetime only).
"""

import os
import re
import datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORRECTIONS_PATH = os.path.join(BASE, "self-improving", "corrections.md")
MEMORY_PATH = os.path.join(BASE, "memory")
LOG_PATH = os.path.join(BASE, "local_storage", "logs")  # if exists

REPORT = []

def read_corrections():
    """Read known mistakes and patterns."""
    if os.path.exists(CORRECTIONS_PATH):
        with open(CORRECTIONS_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return "No corrections log found."

def check_recent_memory():
    """Any mistakes mentioned in today's memory file?"""
    today = datetime.date.today().isoformat()
    today_path = os.path.join(MEMORY_PATH, f"{today}.md")
    if os.path.exists(today_path):
        with open(today_path, "r", encoding="utf-8") as f:
            content = f.read()
        # Look for "我错了", "mistake", "error", "翻车", "傻" patterns
        patterns = [r"(?i)(mistake|error|wrong|翻车|错[了误]|傻|fail|should have|shouldn't|不要|不该)"]
        hits = []
        for p in patterns:
            for m in re.finditer(p, content):
                start = max(0, m.start() - 50)
                end = min(len(content), m.end() + 50)
                hits.append(content[start:end].replace("\n", " "))
        if hits:
            return hits
    return None

def generate_report():
    corrections = read_corrections()
    recent_errors = check_recent_memory()

    REPORT.append("【每30分钟自动自省报告】")
    REPORT.append(f"时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    REPORT.append("")
    REPORT.append("=== 已知模式检查 ===")
    REPORT.append(corrections)

    if recent_errors:
        REPORT.append("")
        REPORT.append("⚠️ 今日记录中发现潜在问题:")
        for h in recent_errors[:3]:
            REPORT.append(f"  • ...{h}...")

    REPORT.append("")
    REPORT.append("=== 行动建议 ===")
    REPORT.append("- 回答前先确认用户的实际情况和条件")
    REPORT.append("- 不要在没有Cue的情况下直接假设用户有特定资源")
    REPORT.append("- 方案被否定后先停下来问清楚，再给出新方案")

    return "\n".join(REPORT)

if __name__ == "__main__":
    import sys
    import time
    sys.stdout.reconfigure(encoding='utf-8')

    max_retries = 2
    delay = 3  # seconds

    for attempt in range(1 + max_retries):
        if attempt > 0:
            time.sleep(delay)
            print(f"[RETRY] 第{attempt}次重试...", file=sys.stderr)
        try:
            report = generate_report()
            print(report)
            break
        except Exception as e:
            if attempt < max_retries:
                continue
            else:
                print(f"[ERR] 自省脚本失败 (已重试{max_retries}次): {e}", file=sys.stderr)
                sys.exit(1)
