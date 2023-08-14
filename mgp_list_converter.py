#!/usr/bin/env python3

import re, sys, subprocess

if len(sys.argv) != 2:
    print("Check Arguments")
    exit(0)

subprocess.run(
        f"pdftotext {sys.argv[1]} grahak-list.txt",
        shell=True)

lines = []
with open("grahak-list.txt") as file:
        lines = file.readlines()
subprocess.run("rm grahak-list.txt", shell=True)

print("Sr. no\tName\tQuantity\tRemark")
for index, line in enumerate(lines):
        if re.search(r'^\d+\s+\D+', line):
                print(line[:line.index(' ')],
                      line[line.index(' ') + 1 :].replace('\n', ''),
                      lines[index - 3],
                      sep='\t', end=''
                      )


