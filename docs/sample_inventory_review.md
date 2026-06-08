# Sample InventoryView Review

This is the stable sample review used for GitHub display. The generated file under `reports/` is intentionally ignored and may be overwritten whenever the scanner runs.

## Scan Summary

- Rule version: `0.1.1`
- Input: `examples/InventoryView.cs`
- Findings: `6`
- Validation source: Claude Code professional review, pending final user confirmation.

## Findings

| # | Rule | Line | Code | Judgment | Notes |
|---|---|---:|---|---|---|
| 1 | U003 | 17 | `refreshButton.onClick.AddListener(RefreshAll);` | Valid | `OnEnable` registers without `OnDisable`; repeated enable/disable may duplicate listeners. |
| 2 | U003 | 18 | `PlayerEvents.InventoryChanged += RefreshAll;` | Valid | Static event subscriptions can retain destroyed views and cause repeated callbacks. |
| 3 | U001 | 23 | `var canvasGroup = GetComponent<CanvasGroup>();` | Valid | Frame-loop component lookup should be cached in `Awake` or `Start`. |
| 4 | U002 | 27 | `var visibleItems = items.Where(item => item.IsVisible).ToList();` | Valid | `Where + ToList` in `Update` can allocate every frame. |
| 5 | U004 | 36 | `var prefab = Resources.Load<GameObject>("Inventory/ItemCell");` | Needs context | Depends on the project resource policy; mixing `Resources` and Addressables is an architecture signal. |
| 6 | U005 | 37 | `var iconHandle = Addressables.LoadAssetAsync<Sprite>("icons/sword");` | Valid | The handle is local and has no visible release path. |

## Manual Review Reminder

Every finding is a suspicious signal, not a confirmed bug. A human reviewer should decide whether each finding is `valid`, `false positive`, or `needs context`.
