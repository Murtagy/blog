Title: (Co)Variance in type checking
Date: 2022-12-21
Category: Blog
Tags: typing

Variance in mypy errors always confused me. I decided to dig into this a little and make things more clear for myself.

For the variance to make sense the language has to support inheritence or types extension.

Let's take off from [an example from mypy page](https://mypy.readthedocs.io/en/stable/generics.html?highlight=variance#variance-of-generic-types)


``` python3
from typing import Callable

class Employee:
    any_employee_attr = 0

class Manager(Employee):
    some_manager_thing = 1

class Boss(Manager):
    some_boss_thing = 2

# E(employee) -> M(anager) -> B(oss)
```


**covariance** - down the inheritance
  Manager is covariant to Employee

**contravariant** - up the inheritance
  Manager is contravariant to Boss

**invariant** - the only class
  Manager is invariant to itself

![covariance](/images/variance.png)

**Covariance** makes more sense in function's arguments

``` python3
def print_worker_details(worker: Employee):
    print(worker.any_employee_attr)

# all below should be valid calls:
print_worker_details(Employee())
print_worker_details(Manager())
print_worker_details(Boss())


```


Callable is an example of type that behaves **contravariant**
 in types of arguments, namely Callable[[Employee], int] is a subtype of Callable[[Manager], int]. 
To understand this, consider a function:


``` python3
def salaries(
    staff: list[Manager],
    accountant: Callable[[Manager], int]
) -> list[int]:
    return [accountant(s) for s in staff]


def accountant_E(e: Employee) -> int:
    return 100

def accountant_M(m: Manager) -> int:
    return 200 * m.some_manager_thing

def accountant_B(b: Boss) -> int:
    return 100 * b.some_boss_thing

# Callables are covariant
staff = [Manager()]
salaries(staff, accountant_E)  # valid   (least specific)
salaries(staff, accountant_M)  # valid   (mid specific)
salaries(staff, accountant_B)  # invalid (most specific)
# note bottom to top order (Employee to Boss)
```

The idea how I understand it is 
> "Less specific type should also work as far as inputs are in the same hierarchy".

So each Manager is an Employee too.
But I think that a manager would not be happy with a salary he receives...



**Lists are mutable**, 
so there is no guarantee that salaries function
would not modify the list and add a Manager to the list of Employees
that would break the type declaration of the input

**So lists are invariant**:


```python3
bosses = [Boss()]
managers = [Manager()]
employees = [Employee()]

salaries(bosses, accountant_M)  # invalid (most specific)
salaries(managers, accountant_M)  # valid (mid specific)
salaries(employees, accountant_M)  # invalid (least specific)
# note top to bottom order (Boss to Employee)

# the example from docs of mypy is great to show source of danger
class Shape:
    pass

class Circle(Shape):
    def rotate(self):
        ...

def add_one(things: list[Shape]) -> None:
    things.append(Shape())

my_things: list[Circle] = []
add_one(my_things)     # This may appear safe, but...
my_things[0].rotate()  # ...this will fail
```

Now when you see that mypy recommends you to use Sequence instead of a List, now you know why - **mutability**.

Let us see where **invariance** has it's use.
We want to create a clone function which clones Managers.
Sounds like a nice function, isn't it?
``` python3
def clone(clonee: Manager) -> Manager:
    return Manager(clonee)
```
This may lead to unexpected behaviour, as we did not really plan to make our Boss a manager. So we may want to tell that argument to `clone` function is invariant. 
And I am sure you will figure out yourself how exactly to do that, as you should be right on track in understanding variance.


Hope this article makes things clear. 
Adios!

### Links:

- [Code launch. Generics Type Variance Explained: covariance, contravariance and invariance](https://www.youtube.com/watch?v=sqCDZmN_zBw&list=WL&index=2) 
- [An example from mypy page](https://mypy.readthedocs.io/en/stable/generics.html?highlight=variance#variance-of-generic-types)