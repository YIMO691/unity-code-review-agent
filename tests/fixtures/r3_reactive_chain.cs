using R3;
using UnityEngine;

public class R3ReactiveChain : MonoBehaviour
{
    private readonly ReactiveProperty<int> hp = new ReactiveProperty<int>(100);

    private void Start()
    {
        hp
            .Where(value => value <= 30)
            .Subscribe(value => Debug.Log(value));
    }
}
