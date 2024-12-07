# Copyright (c) 2024 Khiat Mohammed Abderrezzak
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Author: Khiat Mohammed Abderrezzak <khiat.dev@gmail.com>


"""
Advanced Runtime Type Safety with Symbolic Operators for Python Type Management.
"""


"""
`variable` Class Showcase

This Python class demonstrates a novel approach to enforcing runtime type safety
and redefining assignment operations using `<<` and `>>` operators.

### Idea:
- The `variable` class acts as a strongly typed container.
- The type is defined at initialization, ensuring that only values of the specified type can be assigned.
- The `<<` operator is used to assign a value or transfer data from another `variable` instance.
- The `>>` operator is used to transfer the current value of a `variable` instance to another instance of the same type.

### Vision:
- Explore new paradigms for type-safe programming in Python.
- Replace traditional assignment (`=`) with symbolic operators for expressive and controlled operations.
- Potential to evolve into a library supporting advanced type checks, constraints, or runtime type inference.

### Future Directions:
- Support for more complex types like generics (`List[int]`, `Dict[str, int]`).
- Integration with Python's static type system (`typing` module).
- Advanced error handling, constraints, and validators for assigned values.

"""

from typing import Any, Type


class Variable:
    """
    A strongly-typed container class that enforces runtime type checking and
    provides custom assignment operators.
    """

    def __init__(self, data_type: Type[Any]) -> None:
        """
        Initialize the variable with a specific data type.

        :param data_type: The type of the variable (e.g., int, str).
        :raises TypeError: If `data_type` is not a valid type.
        """
        if not isinstance(data_type, type):
            raise TypeError("`data_type` must be a valid Python type.")
        self.type = data_type
        self.data: Any = None

    def __rshift__(self, other: "Variable") -> None:
        """
        Transfer the current value to another `Variable` instance of the same type.

        :param other: Another `Variable` instance.
        :raises TypeError: If `other` is not a `Variable` instance or the types do not match.
        :raises ValueError: If the current variable's data is uninitialized.
        """
        if not isinstance(other, Variable):
            raise TypeError("Right operand must be a `Variable` instance.")
        if other.type != self.type:
            raise TypeError(
                f"Type mismatch: Cannot transfer {self.type.__name__} to {other.type.__name__}."
            )
        if self.data is None:
            raise ValueError("Cannot transfer uninitialized data.")
        other.data = self.data

    def __lshift__(self, value: Any) -> None:
        """
        Assign a value or transfer data from another `Variable` instance.

        :param value: The value to assign or another `Variable` instance.
        :raises TypeError: If the value's type does not match the variable's type.
        """
        expected_type = self.type  # Cache the type lookup to enhance performance
        if isinstance(value, Variable):
            if value.type != expected_type:
                raise TypeError(
                    f"Type mismatch: Cannot assign {value.type.__name__} to {expected_type.__name__}."
                )
            self.data = value.data
        elif not isinstance(value, expected_type):
            raise TypeError(
                f"Expected type {expected_type.__name__}, got {type(value).__name__}."
            )
        else:
            self.data = value

    def __str__(self) -> str:
        """
        Return a string representation of the variable's value.

        :return: The string representation of the variable's value, or details about its type if uninitialized.
        """
        return (
            str(self.data)
            if self.data is not None
            else f"Uninitialized variable of type {self.type.__name__}"
        )


# Demonstration of the `Variable` class
if __name__ == "__main__":
    # Create an integer variable and assign a value
    x = Variable(int)
    x << 3
    print(f"x: {x}")  # Output: x: 3

    # Create another integer variable and assign it the value of x
    y = Variable(int)
    y << x
    print(f"y: {y}")  # Output: y: 3

    # Update the value of x
    x << 4
    print(f"Updated x: {x}")  # Output: Updated x: 4
    print(f"y remains unchanged: {y}")  # Output: y remains unchanged: 3

    # Transfer the value of x to y
    x >> y
    print(f"After transfer, y: {y}")  # Output: After transfer, y: 4

    # Create a string variable and assign a value
    z = Variable(str)
    z << "hello, world"
    print(f"z: {z}")  # Output: z: hello, world

    # Demonstrate error handling explicitly
    try:
        z << 42  # Raises TypeError: Expected type str, got int
    except TypeError as e:
        print(f"Error: {e}")

    try:
        y << z  # Raises TypeError: Type mismatch: Cannot assign str to int
    except TypeError as e:
        print(f"Error: {e}")
