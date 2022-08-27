#!/usr/bin/env python3

import re
import sys
import subprocess
from rich.console import Console
from rich.table import Table

if len(sys.argv) != 2:
    print("Check Arguments")
    exit(0)

subprocess.run(
        f"pdftotext {sys.argv[1]} grahak-bill.txt",
        shell=True)

table = Table(title="grahak-bill",show_lines=True)

table.add_column("Name")
table.add_column("Amount", style="green")
table.add_column("Bags", style="yellow")

total = 0

def calculate_bill(bill, ignore = 0):
        bill = float(bill)
        temp = (bill - ignore) / 100
        temp = round(temp,2)
        temp *= 100
        temp *= 0.03
        bill += temp
        bill = int(bill)
        global total
        total += bill
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
        bags_bill = re.findall(r'[0-9]+\s\|\s[0-9]+\.[0-9]', content)
        bill = [ x.split()[-1] for x in bags_bill ]
        bags = [ x.split()[0] for x in bags_bill ]

        for n, b, ba in zip(names, bill, bags):
                if 'AARTI' in n:
                        continue
                table.add_row(
                        ''.join(
                            [ x.capitalize() + ' ' for x in n.split()]
                        ),
                        calculate_bill(b),
                        ba
                        )

console = Console()
console.print(table)
print("\nTotal :", total)

subprocess.run("rm grahak-bill.txt", shell=True)
