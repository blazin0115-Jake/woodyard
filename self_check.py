# Woodyard � An open workspace for autonomous AI agents
# Copyright (C) 2026 blazin0115-Jake
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
self_check.py — 启动自检 + 运行时自省
======================================
自动运行在每次会话启动和心跳中，零外部依赖。

启动自检：验证核心文件完整
运行时自省：检查近期错误、更新记忆
"""

import sys
import os
import json
import re
from datetime import date, datetime
from pathlib import Path


BASE_DIR = Path(__file__).parent.resolve()
CORE_FILES = {
    "SOUL.md": ["执行优先级", "反幻觉铁律"],
    "MEMORY.md": ["Identity", "About Aromix", "OpenClaw Setup", "Lessons Learned"],
    "self-improving/memory.md": ["Execution Rules", "Self-Improving", "本地优先", "UltronCore"],
    "HEARTBEAT.md": ["Orbit_Bot Memory Update", "Ultron Auto-Tasks", "Knowledge Cache"],
}


def check_file(filepath: str, must_contain: list = None) -> dict:
    """检查单个文件是否存在、大小、关键内容。"""
    p = Path(filepath)
    result = {"exists": False, "size": 0, "lines": 0, "missing_keywords": []}

    if not p.exists():
        result["missing_keywords"] = ["文件不存在"]
        return result

    result["exists"] = True
    result["size"] = p.stat().st_size
    with open(p, "r", encoding="utf-8") as f:
        content = f.read()
    result["lines"] = content.count("\n") + 1

    if must_contain:
        for kw in must_contain:
            if kw not in content:
                result["missing_keywords"].append(kw)

    return result


def startup_check() -> list:
    """
    启动自检。验证核心文件完整性。
    返回告警列表（如果全通过则返回空列表）。
    """
    alerts = []

    for rel_path, keywords in CORE_FILES.items():
        full_path = BASE_DIR / rel_path
        status = check_file(str(full_path), keywords)

        if not status["exists"]:
            alerts.append(f"[自检] {rel_path} 不存在")
        elif status["missing_keywords"]:
            alerts.append(f"[自检] {rel_path} 缺少: {', '.join(status['missing_keywords'])}")
        elif status["size"] < 50:
            alerts.append(f"[自检] {rel_path} 过小 ({status['size']}B)")

    return alerts


def check_recent_corrections(days: int = 3) -> list:
    """
    检查近期是否有未处理的纠正记录。
    返回需要关注的纠正条目。
    """
    corrections_path = BASE_DIR / "self-improving" / "corrections.md"
    if not corrections_path.exists():
        return []

    with open(corrections_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 找近日的条目
    recent = []
    for line in content.split("\n"):
        for d in range(days):
            from datetime import timedelta
            target = (date.today() - timedelta(days=d)).isoformat()
            if target in line and len(line.strip()) > 10:
                recent.append(line.strip())

    return recent


def check_accumulated_errors() -> list:
    """
    检查 error 标记文件或日志中的累积错误。
    """
    errors = []
    today_path = BASE_DIR / "memory" / f"{date.today().isoformat()}.md"
    if today_path.exists():
        with open(today_path, "r", encoding="utf-8") as f:
            content = f.read()
        # 找 error/失败/超时 关键词
        for keyword in ["超时", "失败", "error", "Error", "ERROR"]:
            if keyword in content:
                for line in content.split("\n"):
                    if keyword in line and len(line.strip()) > 10:
                        errors.append(line.strip()[:100])
                        break  # 每类只记一条
    return errors


def full_check() -> dict:
    """
    全量自检。每次会话启动时调用。
    返回结构化检查报告。
    """
    alerts = []

    # 1. 文件完整性
    file_alerts = startup_check()
    alerts.extend(file_alerts)

    # 2. 近期纠正
    corrections = check_recent_corrections(days=3)
    if corrections:
        alerts.append(f"[自检] 近期有 {len(corrections)} 条未处理的纠正")

    # 3. 累积错误
    errors = check_accumulated_errors()
    if errors:
        alerts.append(f"[自检] 今日日志中有 {len(errors)} 条错误/超时记录")

    return {
        "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "all_clear": len(alerts) == 0,
        "alerts": alerts,
        "stats": {
            "files_checked": len(CORE_FILES),
            "corrections_found": len(corrections),
            "errors_found": len(errors),
        },
    }


def self_reflection() -> dict:
    """
    运行时自省。心跳中调用。
    检查过去几小时的行为，更新记忆。
    """
    today = date.today().isoformat()
    today_path = BASE_DIR / "memory" / f"{today}.md"

    notes = []
    if today_path.exists():
        with open(today_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 统计今天的活动
        heartbeats = content.count("Heartbeat")
        user_interactions = content.count("Aromix")
        decisions = content.count("决策") + content.count("决定") + content.count("暂定")
        errors = content.count("错误") + content.count("失败") + content.count("超时")

        notes.append(f"心跳 {heartbeats} 次")
        notes.append(f"用户交互 {user_interactions} 次")
        notes.append(f"决策 {decisions} 条")
        notes.append(f"错误 {errors} 条")

        reflection = {
            "reflected_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "today": today,
            "summary": ", ".join(notes),
            "has_issues": errors > 0,
        }
    else:
        reflection = {
            "reflected_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "today": today,
            "summary": "今日尚无日志",
            "has_issues": False,
        }

    return reflection


# ──────────────────────────────────────────────
# 自动重启恢复系统（300秒内）
# ──────────────────────────────────────────────

# 核心配置文件列表（SOUL/MEMORY/规则/心跳）
CONFIG_FILES = [
    "SOUL.md",
    "MEMORY.md",
    "HEARTBEAT.md",
    "self-improving/memory.md",
    "self-improving/corrections.md",
]

# 恢复备份目录
RESTORE_DIR = BASE_DIR / "restore_backups"


def backup_configs() -> dict:
    """
    备份核心配置文件到 restore_backups/ 目录。
    每次启动/心跳自动执行。保留最近 5 份。
    """
    RESTORE_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results = {"backed_up": [], "failed": [], "timestamp": timestamp}

    for rel_path in CONFIG_FILES:
        src = BASE_DIR / rel_path
        if not src.exists():
            results["failed"].append(rel_path)
            continue

        safe_name = rel_path.replace("/", "_").replace("\\", "_")
        dst = RESTORE_DIR / f"{timestamp}_{safe_name}"

        import shutil
        shutil.copy2(src, dst)
        results["backed_up"].append(rel_path)

    # 清理旧备份（保留最近 5 份）
    all_backups = sorted(RESTORE_DIR.glob("*"))
    backup_groups = {}
    for b in all_backups:
        name = "_".join(b.name.split("_")[1:])  # 去掉时间戳
        backup_groups.setdefault(name, []).append(b)

    for name, backups in backup_groups.items():
        if len(backups) > 5:
            for old in backups[:-5]:
                old.unlink()

    return results


def recover_from_backup(target_rel: str) -> dict:
    """
    从最近的备份恢复单个文件。
    Args:
        target_rel: 相对路径（如 "SOUL.md"）
    Returns:
        {"success": bool, "message": str}
    """
    safe_name = target_rel.replace("/", "_").replace("\\", "_")
    candidates = sorted(RESTORE_DIR.glob(f"*_{safe_name}"), reverse=True)

    if not candidates:
        return {"success": False, "message": f"没有可用的备份: {target_rel}"}

    src = candidates[0]
    dst = BASE_DIR / target_rel

    import shutil
    shutil.copy2(src, dst)

    # 验证恢复后的文件可读
    try:
        with open(dst, "r", encoding="utf-8") as f:
            content = f.read()
        if len(content) < 50:
            return {"success": False, "message": f"恢复后文件过小 ({len(content)}B)"}
    except Exception as e:
        return {"success": False, "message": f"恢复后读取失败: {e}"}

    return {"success": True, "message": f"{target_rel} 已从备份恢复"}


def auto_restart(timeout_seconds: int = 300) -> dict:
    """
    自动重启系统：检测损坏 → 从备份恢复 → 验证 → 重启 UltronCore。
    必须在 timeout_seconds 内完成。
    
    返回:
        {"status": "ok"|"error"|"partial", "recovered": [...], "failed": [...], "duration_ms": ...}
    """
    import time
    import shutil
    start = time.time()

    result = {"status": "ok", "recovered": [], "failed": [], "duration_ms": 0}

    # 阶段 1: 自检
    check = full_check()
    if check["all_clear"]:
        result["status"] = "ok"
        result["duration_ms"] = round((time.time() - start) * 1000, 1)
        return result

    # 阶段 2: 备份当前配置（恢复前的最后快照）
    backup_configs()

    # 阶段 3: 逐文件恢复
    for rel_path in CONFIG_FILES:
        if time.time() - start > timeout_seconds * 0.9:
            result["failed"].append(f"{rel_path} (超时)")
            break

        filepath = BASE_DIR / rel_path
        if not filepath.exists() or filepath.stat().st_size < 50:
            r = recover_from_backup(rel_path)
            if r["success"]:
                result["recovered"].append(rel_path)
            else:
                result["failed"].append(rel_path)

    # 阶段 4: 最终验证
    final_check = full_check()
    if final_check["all_clear"]:
        result["status"] = "ok"
    elif result["recovered"] and not result["failed"]:
        result["status"] = "ok"
    elif result["recovered"]:
        result["status"] = "partial"
    else:
        result["status"] = "error"

    result["duration_ms"] = round((time.time() - start) * 1000, 1)

    # 超时检查
    if time.time() - start > timeout_seconds:
        result["status"] = "error"
        result["failed"].append("超过 300 秒限制")

    return result


if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    print("=== 启动自检 ===")
    result = full_check()
    if result["all_clear"]:
        print(f"全部通过 ({result['stats']['files_checked']} 文件)")
    else:
        for a in result["alerts"]:
            print(f"  {a}")

    print()
    print("=== 运行时自省 ===")
    ref = self_reflection()
    print(f"  今日: {ref['summary']}")

    print()
    print("=== 备份配置 ===")
    bk = backup_configs()
    print(f"  已备份 {len(bk['backed_up'])} 个文件")

    print()
    print("=== 自动重启测试 ===")
    restart = auto_restart(timeout_seconds=300)
    print(f"  状态: {restart['status']}")
    print(f"  恢复: {restart['recovered']}")
    print(f"  耗时: {restart['duration_ms']}ms")
