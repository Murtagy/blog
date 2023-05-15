Title: Simple code. Stabbing at polymorphism
Date: 2023-05-15
Category: Blog
Tags: simplicity, python


Uncle Bob and some other people claim that polymorphism is a default way to structure code.
I want to explore this idea a little bit.

Let's take the example from the book (Chapter 3 Functions, Switch Statements ),
I have transated the java code snippet into python:


```python

def calculatePay(e: Employee) -> Money:
    match e.type
        case EMPLOYEE_TYPE.COMMISSIONED:
            return calculateCommissionedPay(e);
        case EMPLOYEE_TYPE.HOURLY:
            return calculateHourlyPay(e);
        case EMPLOYEE_TYPE.SALARIED:
            return calculateSalariedPay(e);
        case _:
            raise InvalidEmployeeType(e.type)

```
According to the book:
> Due to:
> - First, it’s large, and when new employee types are added, it will grow
> - Second, it very clearly does more than one thing
> - Third, it violates the Single Responsibility Principle (SRP) because there is more than one reason for it to change
> - Fourth, it violates the Open Closed Principle (OCP) because it must change whenever new types are added
> - WORST, there are an unlimited number of other functions that will have the same structure. 
For example we could have:

``` python
def isPayday(e: Employee, date: datetime.date) -> bool:
    ...

def deliverPay(e: Employee, pay: Money) -> None:
    ... 
```


Let's explore what employee types mean? Probably:
- a COMMISSIONED employee is a sales person who receives a percent of what has been sold;
- a SALARIED employee is the one receiving a monthly salary, not really concentrated around the number of hours worked
- a HOURLY employee is the one receiving a paycheck for HOURs * RATE  

Uncle Bob sees `isPayday` and `deliverPay` and other potential funcitons as problematic probably due to those functions also having a structure around:

```python
def isPayday(e: Employee, date: datetime.date) -> bool:
    match e.type
        case EMPLOYEE_TYPE.COMMISSIONED:
            # at moment of sale
            return True
        case EMPLOYEE_TYPE.HOURLY:
            # weekly
            return date.weekday() == 0
        case EMPLOYEE_TYPE.SALARIED:
            # monthly
            return date.day == 1
        case _:
            raise InvalidEmployeeType(e.type)
```
And all those functions are suffering from the 4 reasons above.

The solution to the problem according to the book looks around this:


```python
class EmployeeBase:
    # arguments of functions were not specified, but I assume Bob thinks of extending each - e.g. accepting date as input, etc
    def isPayday() -> bool:
        raise NotImplemented() 

    def calulatePay() -> Money:
        raise NotImplemented() 

    def deliverPay(pay: Money) -> None:
        raise NotImplemented() 


class EmployeeFactory:
    def makeEmployee(r: EmployeeRecord) -> EmployeeBase:
        switch r.type:
            case COMMISSIONED:
                return CommissionedEmployee(r)
            case HOURLY:
                return HourlyEmployee(r)
            case SALARIED:
                return SalariedEmploye(r)
            case _:
                raise InvalidEmployeeType(r.type)
```

The main benefit of this system is that when we decide to add a new employee type - we do not have to change multiple functions, but have to implement only the methods of the `EmployeeBase`.
  
## Issues with this approach

I disagree with the structure conceptually - it is not an Employee who defines the payday and the pay calculated. And most certainly it does not deliver pay.

There are also structural issues:

- to answer the question - "what are the paydays of our employee types" - I have to jump into individual classes and see the logic of each. Same applies to - "how do we calculate the paychecks".
- the class has to accept as inputs all the context around it. See PROJECT example.
- when adding a Employee - we mix the data and the behaviour. Unlike actual companies - HR add people, Accoouting defines the pay procedures. 
- **what we do if the emoployee is both SALARIED and COMMISSIONED?**


**PROJECT:**
Let's for example introduce the new type of employee - `ProjectEmployee`, which is in charge of running the projects and receives pay 2 weeks after the project he runs is finished. 
So the payday function may look like:

```python
class ProjectBasedEmployee:
    def isPayday(project: Project, date: datetime.date) -> bool:
        if not project.is_finished():
            return False
        if date + datetime.timedelta(days=14) == project.finish_date:
            return True
        return False
```
It means that we have issues with use of the generic `employee.isPayDay()`. We no longer can call the same method despite the employee type. We have to reveal the type and get projects, or the function needs to be capable of access projects `ProjectStore` directly. So we either have to inject data (list of projects), dependency (a project store) or let sideeffects happen - function accesses ProjectStore directly. Same applies to COMMISION. 



## Solution

It is clear that concepts of "how we pay an Employee" is not the same concept as "what is an Employee". So we should structure our code according to business processes:


```python
# payroll.py

def isPayday(e: Employee, date: datetime.date, pay_type: PAY_TYPE) -> bool:
    match pay_type:
        case PAY_TYPE.COMMISSIONED:
            # at moment of sale
            return True
        case PAY_TYPE.HOURLY:
            # weekly
            return date.weekday() == 0
        case PAY_TYPE.SALARIED:
            # monthly
            return date.day == 1
        case _:
            assert_never(e.type)  # this makes new types being added not an issue (in type checked code)

def calculatePay(e: Employee) -> Money:
    match e.type
        case EMPLOYEE_TYPE.COMMISSIONED:
            sales = get_sales(e)
            return calculateCommissionedPay(e, sales);
        case EMPLOYEE_TYPE.HOURLY:
            return calculateHourlyPay(e);
        case EMPLOYEE_TYPE.SALARIED:
            return calculateSalariedPay(e);
        case _:
            assert_never(e.type)  # this makes new types being added not an issue (in type checked code)

...

```
So despite the reasons listed in the book :
- an emloyee can have multiple pay_types, e.g. an employee is both on salary and has the commision from sales;
- the functionality of accounting is placed in a single accounting file;
- we do not make the Employee master of it's own payroll. Which both matches business needs and is easier to navigate the concepts.

Of course at some points the logic of `isPayday` will be hidden into functions (like in `calculatePay`) and we will lose the ability to see all the logic in a single screen again. But that is not the main idea (although I am fine with keeping that in a single function for now).

Polymophism is a hint that we are putting a certain behaviour onto the object, while it might not be cohesive enough to the object and might have a great dependency on context around it.  
### **The key idea is that we should take great care not to introduce the abstractions which are mismatching the business needs unless there are obvious benefits from it. And those benefits are addressing complexity in different way than number of `switch`es** 
