using UnityEngine;

public class EventSubscriptionVsAccumulation : MonoBehaviour
{
    private int hitCount;

    private void OnEnable()
    {
        PlayerEvents.InventoryChanged += Refresh;
    }

    private void Update()
    {
        hitCount += 1;
    }

    private void Refresh()
    {
    }
}

public static class PlayerEvents
{
    public static event System.Action InventoryChanged;
}
