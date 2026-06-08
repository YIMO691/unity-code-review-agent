using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.AddressableAssets;
using UnityEngine.UI;

public class InventoryView : MonoBehaviour
{
    [SerializeField] private Button refreshButton;
    [SerializeField] private Transform itemRoot;

    private readonly List<ItemData> items = new List<ItemData>();
    private int hitCount;

    private void OnEnable()
    {
        refreshButton.onClick.AddListener(RefreshAll);
        PlayerEvents.InventoryChanged += RefreshAll;
    }

    private void Update()
    {
        var canvasGroup = GetComponent<CanvasGroup>();
        canvasGroup.alpha = items.Count > 0 ? 1f : 0.5f;
        hitCount += 1;

        var visibleItems = items.Where(item => item.IsVisible).ToList();
        if (visibleItems.Count > 20)
        {
            RefreshAll();
        }
    }

    private void RefreshAll()
    {
        var prefab = Resources.Load<GameObject>("Inventory/ItemCell");
        var iconHandle = Addressables.LoadAssetAsync<Sprite>("icons/sword");

        foreach (var item in items)
        {
            Instantiate(prefab, itemRoot);
        }
    }
}

public static class PlayerEvents
{
    public static event System.Action InventoryChanged;
}

public class ItemData
{
    public bool IsVisible;
}
