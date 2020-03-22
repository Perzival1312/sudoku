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

import os, sys, readline, copy
import pygame as pg
from pygame.locals import *

if not pg.font: print('Warning, fonts disabled')
if not pg.mixer: print('Warning, sound disabled')

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

    # get box based on coordinate pair
    if isinstance(box, tuple):
        for key, value in box_coords.items():
            if box in value:
                box = key

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

def solver(board):
    '''
        return the solved given board 
    '''
    # get all coordinates of not filled in numbers
    # try to place 1-9 in those coords
    #     via row, col, and box checker
    # while not board_checker

    # create and array and populate it with coordinates of spots without numbers
    unplaced_nums = []
    for i_r, row in enumerate(board):
        for i_c, col in enumerate(row):
            if col == 0:
                unplaced_nums.append((i_r, i_c))

    while not board_checker(board):
        # prolly wont happen but conditional to catch misplaced number...
        if len(unplaced_nums) == 0:
            print('something fucked up')
            break
        to_remove = []
        for coords in unplaced_nums:
            possible_nums = []
            # find what numbers might work in each square
            # possible optimization of storing these in a dict
            # with the cood as the key and possible nums as the value
            # are tuples hashable?
            for num in range(1, 10):
                if not row_checker(board, num, coords[0]):
                    if not col_checker(board, num, coords[1]):
                        if not box_checker(board, num, (coords)):
                            possible_nums.append(num)
            # if there is only one possible number set that in the board
            # and set that coordinate pair to be removed from the list
            if len(possible_nums) == 1:
                board[coords[0]][coords[1]] = possible_nums[0]
                to_remove.append(coords)
        # remove all newly placed coordinates
        for coord in to_remove:
            unplaced_nums.remove(coord)
    return board

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

def main_game_loop_func_cli(board):
    # board is not solved... keep playing
    while not board_checker(board):
        printer(board)
        num = input_validator('What is the number you wish to place on the board? ')
        row = input_validator('What row is that number to go in? ')
        col = input_validator('What column is that number to go in? ')
        replace(board, num, row, col)
    # board is solved!
    printer(board)
    print('\nYou have successfully completed this Sudoku puzzle!!')

def main_game_loop_func_pygame(board):
    # pygame keycode and corresponding number
    NUM_KEYS = {49:1, 50:2, 51:3, 52:4, 53:5, 54:6, 55:7, 56:8, 57:9}
    # size of sudoku boxes
    r_size = 50
    # initialize pygame and all necassary modules
    pg.init()
    # window size
    screen = pg.display.set_mode((11*r_size, 13*r_size))
    # window title
    pg.display.set_caption('SuDoKu')
    # pg.mouse.set_visible(0)
    # generate white background surface
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))
    # Draw title inside of window
    if pg.font:
        font = pg.font.Font(None, 36)
        text = font.render("SuDoKu!", 1, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width()/2)
        background.blit(text, textpos)
    # Draw updated screen with text
    screen.blit(background, (0, 0))
    pg.display.flip()
    # initialize clock
    clock = pg.time.Clock()
    # all of the squares for the sudoku grid
    border_rects = []
    for y in range(1, 10):
        for x in range(1, 10):
            border_rects.append(pg.rect.Rect((x+x*r_size, y+y*r_size),(r_size, r_size)))
    # drawing the squares
    for rect in border_rects:
        pg.draw.rect(background, [0,0,0], rect, 2)
    # generate solver button and text
    solver_button = pg.rect.Rect((background.get_width()/2)-r_size, 11*r_size, r_size*2, r_size)
    pg.draw.rect(background, [0,0,0], solver_button, 3)
    if pg.font:
        font = pg.font.Font(None, 36)
        text = font.render("Solve!", 1, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width()/2, centery=11.5*r_size)
        background.blit(text, textpos)
    # store previously clicked rect initialized as false
    prev_clicked = 0
    while 1:
        # 60 fps max
        clock.tick(60)
        for event in pg.event.get():
            # Exit events
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            # mouse-click handling
            if event.type == pg.MOUSEBUTTONUP:
                # revert the previously state changed square
                if prev_clicked:
                    pg.draw.rect(background, [250,250,250], prev_clicked)
                    pg.draw.rect(background, [0,0,0], prev_clicked, 2)
                # get mouse position
                pos = pg.mouse.get_pos()
                # find square mouse click is in
                clicked_sqr = [s for s in border_rects if s.collidepoint(pos)]
                # ensure that a square was actually clicked and not something off the board
                if clicked_sqr != []:
                    # save clicked square so that the state status can be reset
                    prev_clicked = clicked_sqr[0]
                    # set state of clicked square
                    pg.draw.rect(background, [200,200,200], clicked_sqr[0])
                # solve button logic
                if solver_button.collidepoint(pos):
                    solver(board)
            # getting the number pressed to change the clicked sqr to
            if event.type == KEYDOWN and event.key in NUM_KEYS.keys():
                # get the number that corresponds to the pygame keycode
                num = NUM_KEYS[event.key]
                # get the box that was clicked
                abs_pos = border_rects.index(prev_clicked)
                # get the row/col within the board
                row = abs_pos//9
                col = abs_pos%9
                # update number in board
                board[row][col] = num

        # Flatten the board array for easier number placement
        # bc the square list is only 1D
        board_nums = []
        for row in board:
            board_nums.extend(row)
        # Draw in the numbers
        if pg.font:
            font = pg.font.Font(None, 36)
            for ind, sqr in enumerate(border_rects):
                text = font.render(str(board_nums[ind]), 1, (10, 10, 10))
                # position number in the center of all the squares
                textpos = text.get_rect(centerx=sqr.x+(sqr.width/2), centery=sqr.y+(sqr.height/2))
                background.blit(text, textpos)
        # redraws updated screen
        screen.blit(background, (0, 0))
        pg.display.flip()
        # change screen to win state!
        if board_checker(board):
            # background.fill((0,0,0))
            pg.display.update()
            if pg.font:
                #  win statement text
                win_text = font.render("YOU WIN!!", 1, (0,0,0))
                win_textpos = win_text.get_rect(centerx=background.get_width()/2, 
                    centery=10.5*r_size)
                background.blit(win_text, win_textpos)
    # friendly quitting
    pg.quit()

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
    [1,2,3,4,5,6,7,8,0],
    [4,5,6,7,8,9,1,0,3],
    [7,8,9,1,2,3,0,5,6],
    [2,3,4,5,6,0,8,9,1],
    [5,6,7,8,0,1,2,3,4],
    [8,9,1,0,3,4,5,6,7],
    [3,4,0,6,7,8,9,1,2],
    [6,0,8,9,1,2,3,4,5],
    [0,1,2,3,4,5,6,7,8]]

    main_game_loop_func_pygame(b3)
    # printer(solver(b3))
