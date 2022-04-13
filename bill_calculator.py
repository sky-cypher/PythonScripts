#!/usr/bin/env python3

import re
from rich.console import Console
from rich.table import Table

IGNORE = 240

table = Table(title="grahak-bill")

table.add_column("Name")
table.add_column("Amount", style="green")

def calculate_bill(bill, ignore = 0):
        bill = float(bill)
        temp = (bill - ignore) / 100
        temp = round(temp,2)
        temp *= 100
        temp *= 0.03
        bill += temp
        bill = int(bill)
        return('\u20b9' + str(bill))

with open("grahak-bill.txt") as file:
        content = ""
        save = False
        for line in file.readlines():
                if save:
                        if re.search('^-',line):
                                # print(line)
                                save = False
                                break
                        content += ''.join(line)
                if not save and re.search('-?#', line):
                        save = True
                        # print(line)

        names = re.findall(r'[A-Z]+\s[A-Z]+\s[A-Z]+', content)
        bill = re.findall(r'[0-9]+\.[0-9]', content)
        for n, b in zip(names, bill):
                table.add_row(''.join([ x.capitalize() + ' ' for x in n.split()]),
                              calculate_bill(b , ignore = IGNORE))

console = Console()
console.print(table)

