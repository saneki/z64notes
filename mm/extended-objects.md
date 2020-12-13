Extended Objects
================

Standard object table:
- Address: `0x801C2740`
- End:     `0x801C3B58`
- Entries: `0x283` (or `643` decimal)

Functions which access the object table for loading object data:
- `0x8012F2E0`: when loading a new area.
- `0x8012F698`: when unpausing.
- `0x8012F73C`: when loading an item from a shop.
- `0x8012F4FC`: same as above?
  - Function signature: `0x8012F4FC(z2_obj_ctxt_t *ctxt)`
  - Only seems to do something if (signed) object index is less than 0.
  - ... in which case it calculates the actual index as `0 - index`, similar to some graphic indexes?
- `0x80755CC0`: load `get-item`.


```cs
        /*
        private void lol(int index, byte graphic, short obj, Item item)
        {
            RomData.GetItemList[index].Index = graphic;
            RomData.GetItemList[index].Object = obj;
            ItemSwapUtils.UpdateShop(item, item, new List<MessageEntry>());
        }

        private void lol2()
        {
            // ;-;
            lol(0xBB, 0xB5, 0x285, Item.ShopItemTradingPostGreenPotion);
            lol(0xBC, 0x13, 0x283, Item.ShopItemTradingPostShield);
            lol(0xBD, 0x4F, 0x286, Item.ShopItemTradingPostFairy);
            lol(0xBE, 0x4F, 0x287, Item.ShopItemTradingPostStick);
            lol(0xBF, 0x4F, 0x288, Item.ShopItemTradingPostArrow30);
            lol(0xC0, 0x4F, 0x289, Item.ShopItemTradingPostNut10);
            lol(0xC1, 0x4F, 0x28A, Item.ShopItemTradingPostArrow50);
            lol(0xCD, 0xB5, 0x284, Item.ShopItemTradingPostRedPotion);
        }
        */
```
