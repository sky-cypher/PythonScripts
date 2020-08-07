#!/usr/bin/env python3

class Number:
    def __init__(self, value = 0):
        self.value = value
    def __del__(self):
        del self.value
    def __str__(self):
        return str(self.value)
    def __add__(self, other):
        return self.value + other.value
    def __truediv__(self, other):
        return self.value / other.value

x, y = number(5), number(2)
print("x =", x, "\ny =",y)
z = x + y
print("x + y =", z)
z = x / y
print("x / y =", z)
