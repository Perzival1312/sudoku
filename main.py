'''
input:
    board:
        string type, empty spots are '0'
        comma delimited str of single/9digit ints?
        single large int?

    interactive solving:
        space or comma delimited? all? or (number coord1,coord2)
        or 3 seperate input calls? <-- this one call num, row, col
        number guessing:
            just a single int
        position:
            2 seperate ints

functions:
    convert board input into list of lists --> [[r1], [r2], ...[r9]]
    validate interactive cli game input
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


import pygame, string, os, readline

def parse_board(input):
    '''Take the input string from the command line and convert it into something usable'''
    usable = []
    return usable

def input_validator(input_string):
    '''Validate the integers given via the cli
    input_string - the prompt for the python inupt() function'''
    valid_input = False
    while not valid_input:
        try:
            testing_input = input(input_string)
            if not testing_input.isnumeric():
                print("Only numbers, please try again!")
            elif int(testing_input) < 1 or int(testing_input) > 9:
                print("Must be between 1 and 9")
            else:
                valid_input = True
                return int(testing_input)
        except EOFError:
            print("Not a number! Try again.")
            continue

def row_checker(board, num, row):
    '''Check if the number (num) is in the specified row (row)'''
    if num in board[row]:
        return True
    return False

def col_checker(board, num, col):
    '''Check if the number (num) is in the specified column (col)'''
    for row in board:
        if num == row[col]:
            return True
    return False

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
    and theres a list of coordinate tuples as the values
    ^ Should that be hard coded in or algorithmically created at every startup?
    well if were only doing 9x9 it wouuld be fine to hard code it 
    but that looks atrocious... so uh thats what imma do for speed stuff....
    wait is it actually faster? 
    TODO: test the speeds and write the algo to create this dict
    '''
    box_coords = {1: [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)], 
    2: [(0, 3), (0, 4), (0, 5), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5)], 
    3: [(0, 6), (0, 7), (0, 8), (1, 6), (1, 7), (1, 8), (2, 6), (2, 7), (2, 8)], 
    4: [(3, 0), (3, 1), (3, 2), (4, 0), (4, 1), (4, 2), (5, 0), (5, 1), (5, 2)], 
    5: [(3, 3), (3, 4), (3, 5), (4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5)], 
    6: [(3, 6), (3, 7), (3, 8), (4, 6), (4, 7), (4, 8), (5, 6), (5, 7), (5, 8)], 
    7: [(6, 0), (6, 1), (6, 2), (7, 0), (7, 1), (7, 2), (8, 0), (8, 1), (8, 2)], 
    8: [(6, 3), (6, 4), (6, 5), (7, 3), (7, 4), (7, 5), (8, 3), (8, 4), (8, 5)], 
    9: [(6, 6), (6, 7), (6, 8), (7, 6), (7, 7), (7, 8), (8, 6), (8, 7), (8, 8)]}
    coords = box_coords[box]
    for coord in coords:
        if num == board[coord[0]][coord[1]]:
            return True
    return False

def board_checker(board):
    '''Final check to make sure that the board is properly solved'''
    for i in range(1, 10):
        for c in range(9):
            if not (row_checker(board, i, c) and col_checker(board, i, c) and box_checker(board, i, c+1)):
                return False
    return True

def replace(board, num, row, col):
    '''Place the number (num) in the specified row (row)
     and column (col) within the board (board)'''
    board[row-1][col-1] = num

def printer(board):
    '''Print the board to the terminal formatted in a TBD way'''
    # clear the screen before printing the board
    os.system('clear')
    # length of row divider lines
    width = 45
    print('\n    ', end='')
    #print column numbers
    for i in range(1, 10):
        print('  ' + str(i) + ' ', end='')
        if i%3==0:
            print('    ', end='')
    # print top line of board
    print('\n\n    ' + '-'*width)
    for i, r in enumerate(board):
        # convert list of ints into string with spaces every 3 numbers
        stringed = ''
        for ind, num in enumerate(r):
            stringed += str(num) 
            if ind%3==2:
                stringed += ' '
        # print row number and row of numbers with dividers
        print(str(i+1) + '   | '+' | '.join(stringed))
        # print row sperator
        print('    ' +'-'*width)
        # print box seperator 
        if i%3==2 and i!=8:
            print('    '+'-'*width)

def main_game_loop_func(board):
    # board is not solved... keep playing
    while not board_checker(board):
        printer(board)
        num = input_validator('What is the number you wish to place on the board? ')
        row = input_validator('What row is that number to go in? ')
        col = input_validator('What column is that number to go in? ')
        replace(board, num, row, col)
    # board is solved!
    printer(board)
    print('\nYou have successfully Completed this Sudoku puzzle!!')



if __name__ == "__main__":
    # solved board
    b = [
    [1,2,3,4,5,6,7,8,9],
    [4,5,6,7,8,9,1,2,3],
    [7,8,9,1,2,3,4,5,6],
    [2,3,4,5,6,7,8,9,1],
    [5,6,7,8,9,1,2,3,4],
    [8,9,1,2,3,4,5,6,7],
    [3,4,5,6,7,8,9,1,2],
    [6,7,8,9,1,2,3,4,5],
    [9,1,2,3,4,5,6,7,8]]
    # wrong board
    b2 = [
    [1,2,3,4,5,6,7,8,9],
    [1,2,3,4,5,6,7,8,9],
    [1,2,3,4,5,6,7,8,9],
    [1,2,3,4,5,6,7,8,9],
    [1,2,3,4,5,6,7,8,9],
    [1,2,3,4,5,6,7,8,9],
    [1,2,3,4,5,6,7,8,9],
    [1,2,3,4,5,6,7,8,9],
    [1,2,3,4,5,6,7,8,9]]
    # almost solved board
    b3 = [
    [1,2,3,4,5,6,7,8,8],
    [4,5,6,7,8,9,1,2,3],
    [7,8,9,1,2,3,4,5,6],
    [2,3,4,5,6,7,8,9,1],
    [5,6,7,8,9,1,2,3,4],
    [8,9,1,2,3,4,5,6,7],
    [3,4,5,6,7,8,9,1,2],
    [6,7,8,9,1,2,3,4,5],
    [9,1,2,3,4,5,6,7,8]]

    # print(board_checker(b))
    # printer(b)
    main_game_loop_func(b3)
