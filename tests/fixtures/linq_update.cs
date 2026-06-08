using System.Collections.Generic;
using System.Linq;
using UnityEngine;

public class LinqUpdate : MonoBehaviour
{
    private readonly List<int> values = new List<int>();

    private void Update()
    {
        var visible = values.Where(value => value > 0).ToList();
    }
}
