Title: The hanging attribute
Date: 2022-07-12
Category: Blog
Tags: abstractions, python


I have not practiced writing for the long time, so this might be not my best text, but here we go.

The problem I named "The hanging attribute" can be highlighted with the following example.
Let's assume that we have a class Item which we sell:
``` python
class Item:
    item_id: int
    price: float
    category: str
    name: str
    dimensions: {"weight": x, "volume": y}

```

And we want to have ability to select stuff.

(note: often people do client-side selection, we do it server-side)

Here we have some options:


1) Selection abstraction
``` python
from collections import defaultdict

selection = defaultdict(int)

item_id = 1
quantity = 5
selection[item_id] += quantity

```
2) SelectedItem abstraction
``` python
class SelectedItem(Item):
    quantity: int
```

How to choose which option to pick?
I have hard times in finding the traits that make one option be more attractive over another.


Let's write some user-code of server-side selection (some pseudo code involved):

1) Selection abstraction
``` python
items: list[Item] = get_items_from_db(...)
send_items_to_client(items)
# ...
selected_item_id, selected_quantity = receive_selection()
selection[selected_item_id] = selected_quantity


```
2) SelectedItem abstraction
``` python
items: list[Item] = get_items_from_db(...)
send_items_to_client(items)
# ...
selectable_items = make_selectable_items(items)  # default quantity == 0
selected_item_id, selected_quantity = receive_selection()
selected_item = [i for i in selectable_items if i.item_id == selected_item_id][0]
selected_item.quantity = selected_quantity

```
Given that both solutions lack input validation, so the second option seems a little more complicated.

Let's now add a constrain - we want some rules being calculated on top off current selection. 
For example we want to limit `max_weight` of the order to be below 100 kilos.
Let's extend the code:

1) Selection abstraction
``` python
items: list[Item] = get_items_from_db(...)
send_items_to_client(items)
# ...
selected_item_id, selected_quantity = receive_selection()
selection[selected_item_id] = selected_quantity
# ...

quantity = int  # for better signature readability

selected_items: list[tuple[Item, quantity]] = []

for selected_item_id, selected_quantity in selection.items():
    selected_item = get_item_by_id(selected_item_id)
    selected_items.append((selected_item, selected_quantity))

selected_weight = sum(item.dimensions.weight * q for item, q in selected_items)
if selected_weight > max_weight:
    raise SelectedWeightError()

```
2) SelectedItem abstraction

``` python
items: list[Item] = get_items_from_db(...)
send_items_to_client(items)
# ...
selectable_items = make_selectable_items(items)  # default quantity == 0
selected_item_id, selected_quantity = receive_selection()
selected_item = [i for i in selectable_items if i.item_id == selected_item_id][0]
selected_item.quantity = selected_quantity
# ...
selected_weight = sum(item.dimensions.weight * item.quantity for item in selected_items)
if selected_weight > max_weight:
    raise SelectedWeightError()

```
So we seem to benefit from SelectedItem as long as we need to operate on Item's attributes and on quantity at the same time. Packing quantity and Item together seems to be wanted.

In my opinion we went to `selected_items` way more straight forward in `2)` snippet.  
You might argue :
>Hey, I could have written a short way to make SelectedItem out of snippet `1)`

And actually I won't persuade you in the opposite. What I wanted to state that SelectedItem abstraction seems beneficial as it couples together Item and quantity.

So a way to reasons about this is in terms of coupling - we are likely to use Item and quantity together, so -

# Don't let quantity attribute hang in the tuple - time to create SelectedItem
<br>
<br>
[1]
I have made small search on this problem and found a reference to a similar problem at [refactoring.guru](https://refactoring.guru/smells/feature-envy). Don't hesitate to check it.


<!-- next idea: let's assume that we have 2 Items which have exclusive selection -->

