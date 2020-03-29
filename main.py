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
# readline prevents NULL from being submitted via cli
import os, sys, readline, random, copy, math
import pygame as pg
from pygame.locals import *

sys.setrecursionlimit(10000)

box_coords = {1: [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)], 
2: [(0, 3), (0, 4), (0, 5), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5)], 
3: [(0, 6), (0, 7), (0, 8), (1, 6), (1, 7), (1, 8), (2, 6), (2, 7), (2, 8)], 
4: [(3, 0), (3, 1), (3, 2), (4, 0), (4, 1), (4, 2), (5, 0), (5, 1), (5, 2)], 
5: [(3, 3), (3, 4), (3, 5), (4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5)], 
6: [(3, 6), (3, 7), (3, 8), (4, 6), (4, 7), (4, 8), (5, 6), (5, 7), (5, 8)], 
7: [(6, 0), (6, 1), (6, 2), (7, 0), (7, 1), (7, 2), (8, 0), (8, 1), (8, 2)], 
8: [(6, 3), (6, 4), (6, 5), (7, 3), (7, 4), (7, 5), (8, 3), (8, 4), (8, 5)], 
9: [(6, 6), (6, 7), (6, 8), (7, 6), (7, 7), (7, 8), (8, 6), (8, 7), (8, 8)]}

if not pg.font: print('Warning, fonts disabled')
if not pg.mixer: print('Warning, sound disabled')

def parse_board(input):
    '''Take the input string from the command line and convert it into something usable'''
    usable = []
    temp = []
    for ind, num in enumerate(input):
        if (ind+1)%9 != 0:
            temp.append(int(num))
        else:
            temp.append(int(num))
            usable.append(temp)
            temp = []
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
    '''Return True if the number (num) is in the specified row (row)'''
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
    Checks if the number (num) is in the box (box)
    '''
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

def get_row(board, row):
    '''Return a list of all numbers placed within the specified row'''
    row_nums = []
    for num in board[row-1]:
        if num != 0:
            row_nums.append(num)
    return row_nums

def get_column(board, col):
    '''Return a list of all numbers placed within the specified column'''
    column = []
    for row in board:
        if row[col-1] != 0:
            column.append(row[col-1])
    return column

def get_box(board, box):
    '''Return a list of all numbers placed within the specified box'''
    box_nums = []
    coord_list = box_coords[box]
    for coords in coord_list:
        num = board[coords[0]][coords[1]]
        if num != 0:
            box_nums.append(num)
    return box_nums

def duplicate_checker(board):
    '''Checks rows, columns, and boxes for any duplicates 
    returns (the integer of the r/c/b, and a char of 'r','c','b') if there are duplicates
    returns (0, empty string) if there are no duplicates'''
    # possibly return the number that is duplicated
    for i in range(1, 10):
        row = get_row(board, i)
        col = get_column(board, i)
        box = get_box(board, i)
        if len(row) != len(set(row)):
            return (i, 'r')
        if len(col) != len(set(col)):
            return (i, 'c')
        if len(box) != len(set(box)):
            return (i, 'b')        
    return (0, '')

def generate_col(board, col):
    # generate numbers to go into the column
    col_pool = [1,2,3,4,5,6,7,8,9]
    placed = get_column(board, col)
    for num in placed:
        col_pool.remove(num)
    random.shuffle(col_pool)
    # garuntee no repeats in rows or boxes
    need_to_reshuffle = True
    while need_to_reshuffle:
        for ind, row in enumerate(board):
            if ind+1 < len(board):
                if row_checker(board, col_pool[ind], ind+1):
                    random.shuffle(col_pool)
                    need_to_reshuffle = True
                    check_box = False
                    break
            else:
                need_to_reshuffle = False
                check_box = True
                break
        if check_box:
            if box_checker(board, col_pool[0], math.ceil(col/3)) or box_checker(board, col_pool[1], math.ceil(col/3)):
                random.shuffle(col_pool)
                need_to_reshuffle = True
            else:
                need_to_reshuffle = False
    return col_pool

def generate_box(board, box):
    box_pool = [1,2,3,4,5,6,7,8,9]
    placed = get_box(board, box)
    for num in placed:
        box_pool.remove(num)
    return box_pool
    
def generate_row(board, row):
    row_pool = [1,2,3,4,5,6,7,8,9]
    placed = get_row(board, row)
    for num in placed:
        row_pool.remove(num)
    return row_pool

def fill_row(board, row, filler):
    while len(filler) != 0:
        for ind, spot in enumerate(board[row-1]):
            to_remove = []
            if spot == 0:
                for num in filler:
                    if not col_checker(board, num, ind) and not box_checker(board, num, (row, ind)):
                        board[row-1][ind] = num
                        to_remove.append(num)
                        break
                for num in to_remove:
                    filler.remove(num)
        if len(to_remove) == 0:
            break
    return board

def fill_col(board, col, filler):
    for ind, row in enumerate(board):
        if row[col-1] == 0:
            board[ind][col-1] = filler[ind-1]
    return board

def fill_box(board, box, filler):
    '''fill in the specified box with a list of numbers (filler)'''
    for coords in box_coords[box]:
        to_remove = []
        spot = board[coords[0]][coords[1]]
        if spot == 0:
            for num in filler:
                if not row_checker(board, num, coords[0]) and not col_checker(board, num, coords[1]):
                    board[coords[0]][coords[1]] = num
                    to_remove.append(num)
                    break
            for number in to_remove:
                filler.remove(number)
    return board

def generator():
    # start from solved and slowly subtract
    # randomly generate the first row and then
    # r1 --> c1 --> b1 --> c4 --> b2 --> c7 --> b3
    # r4 --> b4,5,6
    # r7 --> b7,8,9
    # pool of numbers
    init_pool = [1,2,3,4,5,6,7,8,9]
    # initialize empty board
    board = [[0, 0, 0, 0, 0, 0, 0, 0, 0], 
             [0, 0, 0, 0, 0, 0, 0, 0, 0], 
             [0, 0, 0, 0, 0, 0, 0, 0, 0], 
             [0, 0, 0, 0, 0, 0, 0, 0, 0], 
             [0, 0, 0, 0, 0, 0, 0, 0, 0], 
             [0, 0, 0, 0, 0, 0, 0, 0, 0], 
             [0, 0, 0, 0, 0, 0, 0, 0, 0], 
             [0, 0, 0, 0, 0, 0, 0, 0, 0], 
             [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    # 1st row
    board[0] = random.sample(init_pool, 9)
    # generate and place the 1st column
    c1_pool = generate_col(board, 1)
    board = fill_col(board, 1, c1_pool)
    # generate and place the first box
    b1_pool = generate_box(board, 1)
    board = fill_box(board, 1, b1_pool)
    # generate and place the 4th column
    c4_pool = generate_col(board, 4)
    board = fill_col(board, 4, c4_pool)
    # generate and place the second box
    b2_pool = generate_box(board, 2)
    board = fill_box(board, 2, b2_pool)
    # generate and place the 7th column
    c7_pool = generate_col(board, 7)
    board = fill_col(board, 7, c7_pool)
    # generate and place the third box
    b3_pool = generate_box(board, 3)
    board = fill_box(board, 3, b3_pool)
    # generate and place the 4th row
    r4_pool = generate_row(board, 4)
    board = fill_row(board, 4, r4_pool)
    # generate and place the fourth box
    b4_pool = generate_box(board, 4)
    board = fill_box(board, 4, b4_pool)
    # generate and place the fifth box
    b5_pool = generate_box(board, 5)
    board = fill_box(board, 5, b5_pool)
    # generate and place the sixth box
    b6_pool = generate_box(board, 6)
    board = fill_box(board, 6, b6_pool)
    # generate and place the 7th row
    r7_pool = generate_row(board, 7)
    board = fill_row(board, 7, r7_pool)
    # generate and place the seventh box
    b7_pool = generate_box(board, 7)
    board = fill_box(board, 7, b7_pool)
    # generate and place the eighth box
    b8_pool = generate_box(board, 8)
    board = fill_box(board, 8, b8_pool)
    # generate and place the ninth box
    b9_pool = generate_box(board, 9)
    board = fill_box(board, 9, b9_pool)
    # make sure generated ba\oard is solvable
    if not board_checker(board):
        board = generator()
    return board

def make_puzzle(board):
    prev_coords = (random.randint(0,8), random.randint(0,8))
    prev_num = board[prev_coords[0]][prev_coords[1]]
    board[prev_coords[0]][prev_coords[1]] = 0
    while solvable(board):
        prev_coords = (random.randint(0,8), random.randint(0,8))
        prev_num = board[prev_coords[0]][prev_coords[1]]
        board[prev_coords[0]][prev_coords[1]] = 0
    board[prev_coords[0]][prev_coords[1]] = prev_num
    return board

def solvable(board):
    board_copy = copy.deepcopy(board)
    if solver(board_copy) == False:
        return False
    else:
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
    unplaced_nums = {}
    for i_r, row in enumerate(board):
        for i_c, col in enumerate(row):
            if col == 0:
                unplaced_nums[(i_r, i_c)] = set()

    runs = 0
    while not board_checker(board):
        # prolly wont happen but conditional to catch unsolved board without any empty spaces
        if len(unplaced_nums) == 0:    
            print('something is messed up')
            break
        to_remove = []
        for coords in unplaced_nums.keys():
            possible_nums = set()
            # find what numbers might work in each square
            for num in range(1, 10):
                if not row_checker(board, num, coords[0]):
                    if not col_checker(board, num, coords[1]):
                        if not box_checker(board, num, (coords)):
                            if num not in possible_nums:
                                possible_nums.add(num)
                                unplaced_nums[coords].add(num)
            # if there is only one possible number set that in the board
            # and set that coordinate pair to be removed from the list
            if len(possible_nums) == 1:
                # set the spot on the board as the only value in the set of nums
                board[coords[0]][coords[1]] = next(iter(possible_nums))
                to_remove.append(coords)
                runs = 0
        runs += 1
        if runs == 5:
            return False
            # printer(board)
            # print('Unsolveable')
            # break
        # remove all newly placed coordinates
        for coord in to_remove:
            unplaced_nums.pop(coord)
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
    NUM_KEYS = {48:0, 49:1, 50:2, 51:3, 52:4, 53:5, 54:6, 55:7, 56:8, 57:9}
    # size of sudoku boxes
    r_size = 50
    # initialize pygame and all necassary modules
    pg.init()
    # window size
    screen = pg.display.set_mode((11*r_size, 13*r_size))
    # window title
    pg.display.set_caption('SuDoKu')
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

    # initialize clock
    clock = pg.time.Clock()
    
    # all of the squares for the sudoku grid
    border_rects = []
    for y in range(1, 10):
        for x in range(1, 10):
            border_rects.append(pg.rect.Rect((x+x*r_size, y+y*r_size),(r_size, r_size)))
    # drawing the squares
    for rect in border_rects:
        pg.draw.rect(background, [0,0,0], rect, 3)
        background.fill([250,250,250], rect=rect)
    
    # generate solver button and text
    solver_button = pg.rect.Rect((background.get_width()/2)-r_size, 11*r_size, r_size*2, r_size)
    pg.draw.rect(background, [0,0,0], solver_button, 3)
    if pg.font:
        font = pg.font.Font(None, 36)
        text = font.render("Solve!", 1, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width()/2, centery=11.5*r_size)
        background.blit(text, textpos)
    
    # generate box borders
    box_borders = []
    # outer border
    box_borders.append(pg.rect.Rect(r_size, r_size, 9+r_size*9, 9+r_size*9))
    # vertical border box
    box_borders.append(pg.rect.Rect(2+4*r_size, r_size, 4+3*r_size, 9+9*r_size))
    # horizontal border box
    box_borders.append(pg.rect.Rect(r_size, 2+4*r_size, 9+9*r_size, 4+3*r_size))
    
    # store previously clicked rect initialized as false
    prev_clicked = 0
    while 1:
        # 60 fps max
        clock.tick(60)
        # draw border boxes
        for box in box_borders:
            pg.draw.rect(background, [0,0,0], box, 6)

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
                    pg.draw.rect(background, [0,0,0], prev_clicked, 1)
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
                    for rect in border_rects:
                        background.fill([250,250,250], rect=rect)
                    solver(board)
                    printer(board)
            
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
                background.fill([250,250,250], rect=prev_clicked)

        # Flatten the board array for easier number placement
        # bc the square list is only 1D
        board_nums = []
        for row in board:
            board_nums.extend(row)
        # Draw in the numbers
        if pg.font:
            font = pg.font.Font(None, 36)
            for ind, sqr in enumerate(border_rects):
                # background.fill([250,250,250], rect=sqr)
                text = font.render(str(board_nums[ind]), 1, (10, 10, 10))
                # position number in the center of all the squares
                textpos = text.get_rect(centerx=sqr.x+(sqr.width/2), centery=sqr.y+(sqr.height/2))
                background.blit(text, textpos)
        # redraws updated screen
        screen.blit(background, (0, 0))
        pg.display.flip()
        
        # change screen to win state!
        if board_checker(board):
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
    if len(sys.argv) > 1:
        preparse_board = sys.argv[1:][0]
        board = parse_board(preparse_board)
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

    board = generator()
    printer(board)
    board = make_puzzle(board)
    printer(board)
    printer(solver(board))
    
    # main_game_loop_func_pygame(board)
    # printer(solver(b3))
    # printer(solver(board))
    # super hard brute force
    # 000000001000103085001020000000507000004000100090001000510000073002010000000040019
    # very hard brute force
    # 000060700400005803005003060010009000007020400000100020020700300103500009006040000
    # hard brute force
    # 008003700905700000030009000023004870000002000079380240000900020000007305006500400

    # 830029000090700060400010200048002019009000400120900350004060007050001020000350041
