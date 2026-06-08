using UnityEngine;
using UnityEngine.UI;

public class AddListenerRemoved : MonoBehaviour
{
    [SerializeField] private Button button;

    private void OnEnable()
    {
        button.onClick.AddListener(Refresh);
    }

    private void OnDisable()
    {
        button.onClick.RemoveListener(Refresh);
    }

    private void Refresh()
    {
    }
}
