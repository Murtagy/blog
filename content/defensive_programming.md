Title: Defensive programming (WIP)
Date: 2022-10-28
Category: Blog
Tags: abstractions, python

This post is not finished and up for editions yet.

"Design for change".
I have read this quite a few times, although I have never understood it.
...

Let's tell that we have a following code snippet

```
class Status(enum.Enum):
    NOT_STARTED = enum.auto()
    IN_PROGRESS = enum.auto()
    SUCCESS = enum.auto()
    FAILURE = enum.auto()


FINISHED = [Status.SUCCESS, Status.FAILURE]
NOT_FINISHED = [Status.NOT_STARTED, Status.IN_PROGRESS]
```

How good is the following code?
Seems to be pretty decent - we use enums instead of strings or other literals. We also make an easy way to check if a certain status is finished or not.

Though let's assume that someone is adding a new flow 
Status now can be AWAITING_CONFIRMATION before SUCCESS.
So someone goes into code and adds a new enum value and updates some parts of the code to treat this status.
It might be not that obvious that FINISHED and/or other places require a change.

