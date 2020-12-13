Snippet to unhide all spoiler text:

```js
document.querySelectorAll('.spoiler').forEach(x => x.classList.remove('spoiler'));
```

```cs
public static void DumpGetItemInfoToCVS(string filename)
{
    var dict = new Dictionary<string, (byte, byte, byte, ushort)>();
    for (int i = 0; i < (int)Item.MundaneItemSeahorse; i++)
    {
        var item = (Item)i;
        var index = item.GetItemIndex();
        if (index.HasValue && !dict.ContainsKey(item.Name()))
        {
            var gi = RomData.GetItemList[index.Value];
            dict.Add(item.Name(), (gi.ItemGained, gi.Type, gi.Index, gi.Object));
        }
    }
    var sorted = from entry in dict orderby entry.Value ascending select entry;
    using (var writer = new StreamWriter(filename))
    {
        writer.WriteLine("Item, Type, Graphic, Object, Name");
        foreach (var entry in sorted)
        {
            var name = entry.Key;
            var tuple = entry.Value;
            writer.WriteLine("{0:X2}, {1:X2}, {2:X2}, {3:X4}, {4}", tuple.Item1, tuple.Item2, tuple.Item3, tuple.Item4, name);
        }
    }
}
```

```cs
// Test pluralized names.
var nameSet = new HashSet<string>();
var names = ((Item[])Enum.GetValues(typeof(Item))).Select(x => x.Name()).Where(x => x != null);
foreach (var name in names)
{
    nameSet.Add(name);
}
var plurals = nameSet.ToArray().Select(x => MessageUtils.GetPlural(x)).ToList();
plurals.Sort();
foreach (var plural in plurals)
{
    Console.WriteLine($"Plural: {plural}");
}
```
