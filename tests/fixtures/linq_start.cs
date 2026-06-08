using System.Collections.Generic;
using System.Linq;
using UnityEngine;

public class LinqStart : MonoBehaviour
{
    private readonly List<int> values = new List<int>();

    private void Start()
    {
        var visible = values.Where(value => value > 0).ToList();
    }
}
