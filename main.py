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
    board checker
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

'''
Dani suggestion/approval...
I think a sudoku game would be within scope for this intensive,
and the solver could be your bike or car, approved
'''


import pygame

def parse_input(input):
    '''Take the input string from the command line and convert it into something usable'''
    usable = []
    return usable

def row_checker(board, num, row):
    '''Check if the number (num) is in the specified row (row)'''
    if num in board[row-1]:
        return False
    return True

def col_checker(board, num, col):
    '''Check if the number (num) is in the specified column (col)'''
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

    find specific box placement in board array:
    
    ciel(box/3) = row
    box%3 = col

    (row-1)*3 = west boundary
    (row*3)-1 = east boundary

    (col-1)*3 = north boundary
    (col*3)-1 = south boundary



    OR

    maually store all coordinates of the board in a dict where key is box number
    and theres a list of coordinates as the values
    ^ Should that be hard coded in or algorithmically created at every startup?
    well if were only doing 9x9 it wouuld be fine to hard code it 
    but that looks atrocious...
    
    '''
    pass

def board_checker(board):
    '''Final check to make sure that the board is properly solved'''
    pass

def printer(board):
    '''Print the board to the terminal formatted in a TBD way'''
    pass
