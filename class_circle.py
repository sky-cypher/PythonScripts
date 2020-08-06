#!/usr/bin/env python3

from math import pi

class circle:
    def __init__(self, radius = 0.0):
        self.radius = radius
    def getdata(self, radius: float ):
        self.radius = radius
    def area(self):
        return pi * self.radius ** 2
    def circumference(self):
        return 2 * pi * self.radius
    def __del__(self):
        del self.radius
    def __str__(self):
        return f'''Test ...
Radius = {self.radius}
Area = {round(self.area(),2)}
Circumference = {round(self.circumference(),2)}
'''

if __name__ == "__main__" :
    circle = circle(3)
    print(circle)
