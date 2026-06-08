# InventoryView 人工验证记录

本记录基于 Claude Code 专业审查迁移而来，待用户最终确认。

| # | 文件 | 行号 | 规则 | 命中代码 | 判断 | 说明 |
|---|---|---:|---|---|---|---|
| 1 | `examples/InventoryView.cs` | 17 | U003 | `refreshButton.onClick.AddListener(RefreshAll);` | 有效 | OnEnable 注册但无 OnDisable 解绑，反复启用时可能重复注册。 |
| 2 | `examples/InventoryView.cs` | 18 | U003 | `PlayerEvents.InventoryChanged += RefreshAll;` | 有效 | 静态事件持有订阅者引用，未解绑是高置信度内存泄漏/重复回调风险。 |
| 3 | `examples/InventoryView.cs` | 23 | U001 | `var canvasGroup = GetComponent<CanvasGroup>();` | 有效 | 帧循环中每帧查找组件，应缓存到 Awake/Start。 |
| 4 | `examples/InventoryView.cs` | 27 | U002 | `var visibleItems = items.Where(item => item.IsVisible).ToList();` | 有效 | Update 中 Where + ToList 会产生每帧分配，应改为缓存、显式循环或数据变化时计算。 |
| 5 | `examples/InventoryView.cs` | 36 | U004 | `var prefab = Resources.Load<GameObject>("Inventory/ItemCell");` | 需上下文 | 是否有问题取决于项目资源策略；与 Addressables 混用是架构信号。 |
| 6 | `examples/InventoryView.cs` | 37 | U005 | `var iconHandle = Addressables.LoadAssetAsync<Sprite>("icons/sword");` | 有效 | 句柄为局部变量且无释放路径，高置信度资源生命周期风险。 |

## 发布说明

`reports/InventoryView_review.md` 是扫描器生成物，重新运行扫描会覆盖其中的人工验证表。本文件作为稳定人工验证样例保存在 `docs/` 中，适合纳入 GitHub 仓库。
