#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
knowledge_cache.py — 本地知识缓存
==================================
API 查到的东西自动存这里，下次直接在本地读，不再调 API。

使用流程：
    from knowledge_cache import kc
    
    # 查本地
    cached = kc.lookup("DeepSeek 超时问题")
    if cached:
        return cached
    
    # 没有才调 API
    result = web_search("DeepSeek 超时问题")
    kc.store("DeepSeek 超时问题", result, source="web_search")
    return result

存储位置: knowledge_cache/YYYY-MM-DD/主题名.md
"""

import os
import re
import sys
import json
from datetime import date, datetime
from pathlib import Path


BASE_DIR = Path(__file__).parent.resolve()
CACHE_DIR = BASE_DIR / "knowledge_cache"
INDEX_FILE = CACHE_DIR / "_index.json"


class KnowledgeCache:
    """本地知识缓存。自动按日期归类，按主题索引。"""
    
    def __init__(self):
        self.cache_dir = CACHE_DIR
        self.index = self._load_index()
    
    def _load_index(self) -> dict:
        """加载索引文件。不存在就新建。"""
        if INDEX_FILE.exists():
            try:
                with open(INDEX_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        return {"entries": []}
    
    def _save_index(self):
        """保存索引。"""
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        with open(INDEX_FILE, "w", encoding="utf-8") as f:
            json.dump(self.index, f, ensure_ascii=False, indent=2)
    
    def _topic_to_filename(self, topic: str) -> str:
        """把主题名转成文件名。"""
        safe = re.sub(r"[^\w\s-]", "", topic)
        safe = re.sub(r"[\s_]+", "_", safe.strip().lower())[:60]
        return f"{safe}.md"
    
    def lookup(self, query: str) -> str | None:
        """
        查本地缓存。返回匹配的内容，没有就 None。
        按主题名、关键词匹配。
        """
        query_lower = query.lower().strip()
        if not query_lower:
            return None
        
        best = None
        best_score = 0
        
        for entry in self.index["entries"]:
            score = 0
            # 精确匹配主题
            if query_lower in entry["topic"].lower():
                score += 3
            # 关键词匹配
            for kw in query_lower.split():
                if kw in entry["topic"].lower():
                    score += 1
                if kw in entry.get("keywords", "").lower():
                    score += 1
            
            if score > best_score:
                best_score = score
                best = entry
        
        if best and best_score >= 1:
            path = self.cache_dir / best["path"]
            if path.exists():
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                return f"[本地缓存] {best['topic']}\n\n{content}"
        
        return None
    
    def store(self, topic: str, content: str, source: str = "",
              keywords: str = ""):
        """
        存一条知识到本地缓存。
        
        Args:
            topic: 主题（用于搜索）
            content: 内容
            source: 来源（web_search, web_fetch 等）
            keywords: 额外关键词（逗号分隔）
        """
        today = str(date.today())
        date_dir = self.cache_dir / today
        date_dir.mkdir(parents=True, exist_ok=True)
        
        filename = self._topic_to_filename(topic)
        filepath = date_dir / filename
        
        # 内容
        lines = [
            f"# {topic}",
            f"",
            f"*缓存时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
            f"*来源: {source}*",
            f"*关键词: {keywords}*",
            f"",
            content,
        ]
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        
        # 更新索引（去重）
        rel_path = f"{today}/{filename}"
        self.index["entries"] = [
            e for e in self.index["entries"]
            if e.get("topic") != topic
        ]
        self.index["entries"].append({
            "topic": topic,
            "path": rel_path,
            "source": source,
            "cached_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "keywords": keywords,
        })
        
        # 按缓存时间降序
        self.index["entries"].sort(
            key=lambda e: e.get("cached_at", ""), reverse=True
        )
        
        self._save_index()
        return str(filepath)
    
    def search(self, query: str) -> list:
        """全文搜索所有缓存内容（不仅仅是索引）。"""
        query_lower = query.lower().strip()
        if not query_lower:
            return []
        
        results = []
        for entry in self.index["entries"]:
            path = self.cache_dir / entry["path"]
            if not path.exists():
                continue
            
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            if query_lower in content.lower():
                # 取摘要
                idx = content.lower().find(query_lower)
                start = max(0, idx - 60)
                end = min(len(content), idx + len(query) + 60)
                snippet = content[start:end].replace("\n", " ")
                
                results.append({
                    "topic": entry["topic"],
                    "cached_at": entry.get("cached_at", ""),
                    "snippet": snippet.strip(),
                    "path": entry["path"],
                })
        
        return results[:10]
    
    def stats(self) -> dict:
        """返回缓存统计。从磁盘实时读取。"""
        # 实时读磁盘索引
        if INDEX_FILE.exists():
            try:
                with open(INDEX_FILE, "r", encoding="utf-8") as f:
                    idx = json.load(f)
            except:
                idx = {"entries": []}
        else:
            idx = {"entries": []}
        
        total = len(idx["entries"])
        from collections import Counter
        sources = Counter(e.get("source", "unknown") for e in idx["entries"])
        
        # 计算真实文件大小（只算有对应文件的）
        real_size = 0
        for entry in idx["entries"]:
            fp = self.cache_dir / entry["path"]
            if fp.exists():
                real_size += fp.stat().st_size
        
        return {
            "total_entries": total,
            "by_source": dict(sources),
            "cache_dir_size": real_size,
        }


# 全局单例（方便 import 直接用）
kc = KnowledgeCache()


if __name__ == "__main__":
    # 自测
    print(f"缓存统计: {kc.stats()}")
    
    # 存一条测试
    path = kc.store(
        "DeepSeek 超时问题",
        "DeepSeek v4 flash 间歇性连接超时（model-call-started），通常在 2 分钟后重试成功。",
        source="web_search",
        keywords="DeepSeek, timeout, 超时",
    )
    print(f"已缓存: {path}")
    
    # 查
    cached = kc.lookup("DeepSeek timeout")
    if cached:
        print(f"查到: {cached[:80]}...")
    
    # 搜索
    results = kc.search("超时")
    print(f"搜索 '超时': {len(results)} 条")
