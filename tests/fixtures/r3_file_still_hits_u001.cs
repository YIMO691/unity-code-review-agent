using R3;
using UnityEngine;

public class R3FileStillHitsU001 : MonoBehaviour
{
    private readonly ReactiveProperty<int> hp = new ReactiveProperty<int>(100);

    private void Update()
    {
        var group = GetComponent<CanvasGroup>();
        hp.Where(value => value <= 30).Subscribe(value => Debug.Log(value));
    }
}
