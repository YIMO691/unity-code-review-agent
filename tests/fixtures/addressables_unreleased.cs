using UnityEngine;
using UnityEngine.AddressableAssets;

public class AddressablesUnreleased : MonoBehaviour
{
    private void Start()
    {
        var handle = Addressables.LoadAssetAsync<Sprite>("icons/sword");
    }
}
