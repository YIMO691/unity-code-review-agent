using System.Collections.Generic;
using System.Linq;
using UnityEngine;

public class LinqLateUpdate : MonoBehaviour
{
    private readonly List<int> values = new List<int>();

    private void LateUpdate()
    {
        var visible = values.Where(value => value > 0).ToList();
    }
}
