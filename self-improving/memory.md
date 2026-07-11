# HOT Memory — Learned Patterns

> Auto-loaded on every session. ≤100 lines max.

## Execution Rules (from reasoning-upgrade)
- **失败两次就停**：不无脑重试。第一次失败要分析原因，第二次换个方案。
- **压缩大型输出**：>500 chars 的输出先压缩再读。不直接读 3MB 原始文本。
- **报告前验证**：改代码就跑测试，改配置就验证原命令。不能验证的就说不能。
- **工具调用前先想需要什么结果**：不"随便试试"。

## Self-Improving Rules (from self-improving)
- 每次被纠正后写进 `corrections.md`
- 同一个模式出现 3 次 → 提升为规则
- 30 天未使用的规则 → 降级到 WARM
- SOUL.md 每月 review

## 本地优先铁律 (2026-07-06)
- **调 API 前先查缓存**：knowledge_cache.py + 记忆文件 + 本地知识库
- **查到结果直接回**：不装模作样再搜一遍
- **查了就存**：每次 web_search / web_fetch 完，自动 kc.store()
- **用完清理**：临时脚本、测试文件、自测数据，做完就删

## UltronCore 集成 (2026-07-06)
- **检查类问题直接 import UltronCore**：不再手动翻文件跑命令
- **20ms 出结果**比你翻日记快得多
- **有告警再说**，没异常就安静
