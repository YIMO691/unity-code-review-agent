# Unity 代码审计规则库

## U001：Update 中疑似频繁 GetComponent

### 现象

在 `Update`、`LateUpdate` 或 `FixedUpdate` 方法体内发现 `GetComponent` 系列调用。

### 为什么可能有问题

高频组件查找可能带来不必要的性能开销，也常常说明引用缓存和生命周期设计不够清晰。

### 推荐修改方式

优先在 `Awake` 或 `Start` 中缓存组件引用，并在高频逻辑中复用缓存。

### 容易误报的情况

- 代码只在调试条件下执行。
- 方法名匹配正确，但实际调用频率被外部条件限制。
- 该对象生命周期短且调用频率极低。

## U002：帧循环中疑似使用 LINQ

### 现象

在 `Update`、`LateUpdate` 或 `FixedUpdate` 中发现 `.Where()`、`.Select()`、`.ToList()`、`.FirstOrDefault()` 等疑似 LINQ-to-objects 调用。

### 为什么可能有问题

LINQ 在 Unity 帧循环中可能产生 GC 分配或隐藏迭代成本，尤其是 `.ToList()` 会立即分配新集合。

### 推荐修改方式

若位于性能敏感路径，考虑显式循环、缓存结果，或只在数据变化时重新计算。若是 R3/UniRx 反应式链，应按响应式生命周期审查，而不是按 LINQ-to-objects 审查。

### 容易误报的情况

- R3/UniRx 等反应式库的 `.Where()`、`.Select()` 操作符。
- 代码只在加载、初始化或编辑器工具中运行。
- 数据规模很小且不处于帧循环。

## U003：疑似事件注册，需检查解绑

### 现象

发现 `AddListener` 或 `+=`。

### 为什么可能有问题

如果生命周期结束时未解绑，可能造成重复回调、引用残留或访问已销毁对象。

### 推荐修改方式

检查 `OnDisable` 或 `OnDestroy` 中是否存在对应 `RemoveListener` 或 `-=`。

### 容易误报的情况

- 生命周期和对象同生同灭。
- 解绑由基类或统一事件管理器处理。

## U004：疑似 Resources.Load 使用

### 现象

发现 `Resources.Load` 或 `Resources.LoadAsync`。

### 为什么可能有问题

`Resources` 目录可能让资源引用、包体控制和释放策略变得不透明。

### 推荐修改方式

确认项目是否允许使用 `Resources`。如果项目采用 Addressables 或自定义资源系统，应遵循统一策略。

### 容易误报的情况

- 原型项目或编辑器辅助工具。
- 加载的是少量稳定配置资源。

## U005：疑似 Addressables 加载，需检查释放策略

### 现象

发现 `Addressables.Load` 或 `LoadAssetAsync`，但当前文件未发现明显 `Release`。

### 为什么可能有问题

Addressables 加载后的句柄或实例通常需要明确释放，否则可能造成资源生命周期不清晰。

### 推荐修改方式

确认是否在合适生命周期调用 `Addressables.Release` 或 `Addressables.ReleaseInstance`，或说明资源由统一资源管理器托管。

### 容易误报的情况

- 释放逻辑在其他文件或资源管理服务中。
- 资源生命周期等同应用生命周期。
