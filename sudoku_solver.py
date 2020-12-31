#!/usr/bin/env python3
from colorama import Fore, Style, init
from time import sleep, time
from os import system

'''
puzzle = [
        [0, 1, 8, 9, 0, 0, 0, 0, 0],
        [5, 2, 0, 0, 4, 0, 0, 0, 3],
        [0, 0, 0, 0, 0, 3, 5, 1, 0],
        [0, 0, 0, 0, 9, 0, 0, 5, 0],
        [8, 0, 0, 0, 0, 0, 0, 0, 2],
        [0, 7, 0, 0, 1, 0, 0, 0, 0],
        [0, 9, 2, 6, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 5, 0, 0, 8, 6],
        [0, 0, 0, 0, 0, 4, 1, 2, 0],]
'''

puzzle = [ [ y*0 for y in range(9) ] for x in range(9) ]
init(autoreset = True)
start_time = 0
end_time = 0
display_time = 0.0

def check(row, column, value):
    if value in puzzle[row][:]:
        return False
    for i in range(9):
        if value == puzzle[i][column]:
            return False
    blk_row = (row//3)*3
    blk_column = (column//3)*3
    for x in range(blk_row, blk_row + 3):
        for y in range(blk_column, blk_column + 3):
            if puzzle[x][y] == value:
                return False
    return True

def print_puzzle(row = None, column = None, add = None, final = False):
    global display_time
    display_time += delay
    sleep(delay)
    system('clear')
    not final and print('\n' * 6)
    for x in range(9):
        if x % 3 :
            print('\n\t', end = '')
        else: 
            print(f'\n\t{"-" * 23}\n\t', end = '')
        for y in range(9):
            if y % 3 :
                s = ""
            else:
                s = "| "
            if (row == x and y == column) or final:
                if add or end_time:
                    print(f"{s}{Fore.GREEN}{puzzle[x][y]} ", end = '')
                else:
                    print(f"{s}{Fore.RED}{puzzle[x][y]} ", end = '')
            else:
                if not puzzle[x][y]:
                    print(f"{s}{Fore.BLUE}{puzzle[x][y]} ", end = '')
                else:
                    print(f"{s}{Fore.YELLOW}{puzzle[x][y]} ", end = '')
    print('\n')
    
def solve():
    global puzzle
    for row in range(9):
        for column in range(9):
            if not puzzle[row][column]:
                for value in range(1,10):
                    if check(row, column, value):
                        puzzle[row][column] = value
                        print_puzzle(row, column, True)
                        solve()
                        puzzle[row][column] = 0
                        print_puzzle(row, column, False)
                return 
    print_puzzle()
    global end_time, start_time
    end_time = time()
    if 'n' in input("\ncontinue ? : ").lower():
        raise KeyboardInterrupt
    start_time += time() - end_time


if __name__ == "__main__":
    try:
        delay = float(input("Enter delay in seconds : "))
    except ValueError:
        delay = 0.01
    print_puzzle()
    while 'n' in input("Use defined sudoku ? : ").lower():
        for i in range(9):
            puzzle[i] = [int(x) for x in input(f"Enter row {i + 1} : ")]
            if 9 != len(puzzle[i]):
                puzzle[i] = [ x*0 for x in range(9) ]
                continue
        print_puzzle()
    start_time = time()
    try:
        solve()
    except KeyboardInterrupt:
        print_puzzle(final = True)
        quit()
    finally:
        if end_time:
            tat = end_time - start_time
            print(f"Time Required = {round(tat,4)} seconds\
                    \nDisplay time = {round(display_time, 4)}\
                    \nNet time = {round(tat - display_time, 4)}")

