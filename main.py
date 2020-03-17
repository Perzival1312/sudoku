'''
input:
    string type, empty spots are '0'
    comma delimited str of ints?
    single large int?

functions:
    convert input into list of lists --> [[r1], [r2], ...[r9]]
    row checker
    column checker
    box checker
    replace func (prolly custom?) <-- look this up...
    print the solved board out

output:
    solved board
    no brackets
    spaces between numbers
    possibly add lines

next:
    implement with pygame for better visuals
    optimization!


'''





import pygame
print('Hello, World!')

def parse_input(input):
    usable = []
    return usable

def row_checker(board, num, row):
    if num in board[row-1]:
        return False
    return True

def col_checker(board, num, col):
    for row in board:
        if num == row[col+1]:
            return False
    return True

def box_checker(board, num, box):
    '''
    box definition:
        b1  b2  b3
        b4  b5  b6
        b7  b8  b9

    floor(box/3), box%3 = row, col - of the specific box
    
    '''

    pass

def printer(board):
    pass
