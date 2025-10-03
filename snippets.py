"""Learning snippets for recursion concepts"""

SNIPPETS = {
    "base_case": """
**Understanding Base Cases**

It's crashing because you forgot to add a base case. This is like a guardrail to prevent your recursive calls from going forever.

Let's say you make a call factorial(3).
We'll call factorial(3 - 1)
factorial(2 - 1)
factorial(1 - 1)
factorial(0 - 1)
...
and so on forever. Do you see the problem? We need to define where we should stop:

```python
def factorial(n):
    if n == 0:
        return 1
    if n == 1:
        return 1
```
""",

    "recursive_case": """
**Understanding Recursive Cases**

Think back to the definition of a factorial - factorial(n) = n * factorial(n - 1)
Does this give you a hint on how to calculate the factorial?

Here's the pattern:
```python
def factorial(n):
    if n == 0:
        return 1
    if n == 1:
        return 1
    return n * factorial(n - 1)
```
""",

    "trust_recursion": """
**Trust the Recursion**

You don't actually need to trace through every step of the recursive call. You just need to trust that factorial(n - 1) will return what you need. This concept is also fundamental to computer science and is called abstraction.

Think about your own car. When you ignite the engine, you don't actually need to think about all the internals of how the engine starts. You just trust that your car will turn on when you turn your key. Same here, you just trust that the call to factorial(n - 1) will give you what you need.
"""
}
