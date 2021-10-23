#!/usr/bin/env python3
from time import time
try:
    import numpy as np
except ImportError:
    print('Install numpy')
    quit()
try:
    from rich import print
except ImportError:
    pass


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
sudoku = np.matrix(puzzle)
start_time = 0
end_time = 0


def print_sudoku():
    puzzle = sudoku.tolist()
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
            print(f"{s}{puzzle[x][y]} ", end = '')
    print('\n')


def check(row, column, value):
    if value in sudoku[row,:]:
        return False
    for i in range(9):
        if value == sudoku[i,column]:
            return False
    blk_row = (row//3)*3
    blk_column = (column//3)*3
    for x in range(blk_row, blk_row + 3):
        for y in range(blk_column, blk_column + 3):
            if sudoku[x,y] == value:
                return False
    return True

def solve():
    global sudoku
    for row in range(9):
        for column in range(9):
            if not sudoku[row, column]:
                for value in range(1,10):
                    if check(row, column, value):
                        sudoku[row, column] = value
                        solve()
                        sudoku[row, column] = 0
                return
    global end_time, start_time
    end_time = time()
    print_sudoku()
    if 'y' not in input("\nTry to find another solution ? : ").lower():
        quit()
    start_time += time() - end_time


def main():
    global sudoku, start_time
    print(sudoku)
    if 'n' not in input("Get puzzle from file ? : ").lower():
        file_path = input("Enter file name : ")
        if not file_path:
            file_path = 'sudoku1.txt'
        with open(file_path) as file:
            for i, line in enumerate(file.readlines()):
                puzzle[i] = [ int(x) for x in line.split() ]
        sudoku = np.matrix(puzzle)
        print(sudoku)
    while 'n' in input("Use defined sudoku ? : ").lower():
        for i in range(9):
            puzzle[i] = [int(x) for x in input(f"Enter row {i + 1} : ")]
            while len(puzzle[i]) < 9:
                puzzle[i].append(0)
            while len(puzzle[i]) > 9:
                puzzle[i].pop(-1)
        sudoku = np.matrix(puzzle)
        print(sudoku)
    start_time = time()
    try:
        solve()
    except KeyboardInterrupt:
        print(sudoku)
        quit()
    finally:
        if end_time:
            tat = abs(end_time - start_time)
            print(f"Time Required = {round(tat,4)} seconds")
        else:
            print("Invalid puzzle")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        quit()
