#!/usr/bin/env python3

class count:
    def __init__(self, count = 0):
        self._count = count
    def __str__(self):
        return str(self._count)
    def inc(self):
        self._count += 1
    def __del__(self):
        del self._count
class new_count(count):
    def dec(self):
        self._count -= 1

i = new_count(2)
print(i)
i.inc()
print(i)
i.dec()
print(i)
