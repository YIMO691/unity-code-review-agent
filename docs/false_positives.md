# 误报记录

本文件用于人工验证后记录误报和需上下文的情况。

| 日期 | 文件 | 规则 | 命中代码 | 判断 | 原因 | 后续规则调整 |
|---|---|---|---|---|---|---|
| 2026-06-08 | `projects/verified/R3Demo/Assets/Scripts/Runtime/ReactiveHealth.cs` | U002 | `.Where(hp => hp <= warningThreshold)` | 误报 | Claude Code 验证认为这是 R3 `Observable.Where()` 反应式操作符，位于初始化链，不是 LINQ-to-objects 帧循环分配。 | U002 改为只检查 `Update` / `LateUpdate` / `FixedUpdate`，并在 `using R3;` / `using UniRx;` 文件中排除该规则。 |
| 2026-06-08 | `projects/verified/R3Demo/Assets/Scripts/Runtime/ReactiveHealth.cs` | U002 | `.Where(hp => hp > warningThreshold)` | 误报 | 同上，属于 R3 反应式链。 | 同上。 |
| 2026-06-08 | `projects/verified/R3Demo/Assets/Scripts/Runtime/ReactiveHealth.cs` | U002 | `.Where(hp => hp <= 0)` | 误报 | 同上，属于 R3 反应式链。 | 同上。 |
