using UnityEngine;
using UnityEngine.AddressableAssets;

public class AddressablesReleased : MonoBehaviour
{
    private object handle;

    private void Start()
    {
        handle = Addressables.LoadAssetAsync<Sprite>("icons/sword");
    }

    private void OnDestroy()
    {
        Addressables.Release(handle);
    }
}
