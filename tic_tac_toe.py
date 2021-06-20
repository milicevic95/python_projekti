from IPython.display import clear_output
from colorama import Fore, Style

def main():
    # Contains the main variables, prints the starting board and starts the game.
    
    win = 0
    lst = [char for char in range(0, 10)]
    positions = [str(number) for number in range(1, 10)]
    move = 1
    clr_lst = [Fore.BLACK] * 10
    board(lst, clr_lst)
    game(win, lst, positions, move, clr_lst)

def board(lst, clr_lst):
    # Prints a board with numbered positions and/or signs.
    
    clear_output() # erases everything before printing a new board
    
    st = Style.RESET_ALL
    
    row_a = '   |   |   \n'
    row_b1 = f' {clr_lst[7]}{lst[7]}{st} | {clr_lst[8]}{lst[8]}{st} | {clr_lst[9]}{lst[9]}{st} \n'
    row_b2 = f' {clr_lst[4]}{lst[4]}{st} | {clr_lst[5]}{lst[5]}{st} | {clr_lst[6]}{lst[6]}{st} \n'
    row_b3 = f' {clr_lst[1]}{lst[1]}{st} | {clr_lst[2]}{lst[2]}{st} | {clr_lst[3]}{lst[3]}{st} \n'
    row_c = '___|___|___\n'
    
    table = row_a + row_b1 + row_c + row_a + row_b2 + row_c + row_a + row_b3 + row_a
    print('\n' + table)

def game(win, lst, positions, move, clr_lst):
    # Holds the whole game:
    # starts an input function,
    # starts a function that checks if someone has won,
    # counts moves, announces the winner.
    
    while win == 0:
        input_check(lst, positions, move, clr_lst)
        win = win_check(win, lst, positions)
        move += 1
    
    if win == 1:
        notification = f'{Fore.BLUE}PLAYER {win} IS THE WINNER!\nCONGRATULATIONS!{Style.RESET_ALL}'
    elif win == 2:
        notification = f'{Fore.GREEN}PLAYER {win} IS THE WINNER!\nCONGRATULATIONS!{Style.RESET_ALL}'
    elif win == 3:
        notification = f'{Fore.RED}\nNo winner! The result is a draw!{Style.RESET_ALL}'
    
    print(notification)

def input_check(lst, positions, move, clr_lst):
    # Checks if the input is good,
    # calls the functions that determine the ordinal number of the player,
    # his sign and the color of the sign,
    # and calls the function that inserts the sign into the board.
    
    sign = get_sign(move)
    player_num = get_player(move)
    sign_color = get_color(move)
    
    st = Style.RESET_ALL
    input_str = f"Player {player_num}, your sign is '{sign}'. Choose one free position from 1 to 9: "
    warn_1 = f'{Fore.RED}\nYou can only enter numbers from 1 to 9!{st}'
    warn_2 = f'{Fore.RED}\nChoose the right position! Your number is taken or out of range!{st}'
    
    player_input = input(input_str)
    
    while not player_input in positions:
        if not player_input.isdigit():
            print(warn_1)
        else:
            print(warn_2)
        
        player_input = input(input_str)
    
    positions.remove(player_input)
    insert_sign(lst, player_input, sign, clr_lst, sign_color)

def get_sign(move):
    # Determines the sign based on whose move it is.
    
    if move % 2 == 0:
        sign = '\033[1m' + 'O' + '\033[0m'
    else:
        sign = '\033[1m' + 'X' + '\033[0m'
    
    return sign

def get_player(move):
    # Determines the ordinal number of the player based on whose move it is.
    
    if move % 2 == 0:
        player_number = 2
    else:
        player_number = 1
    
    return player_number

def get_color(move):
    # Determines the color of sign based on whose move it is.
    
    if move % 2 == 0:
        sign_color = Fore.GREEN
    else:
        sign_color = Fore.BLUE
    
    return sign_color

def insert_sign(lst, player_input, sign, clr_lst, sign_color):
    # Inserts the sign into the board.
    
    player_input = int(player_input)
    lst[player_input] = sign
    clr_lst[player_input] = sign_color
    board(lst, clr_lst)

def win_check(win, lst, positions):
    # Checks if someone has won.
    
    x3 = ['\033[1m' + 'X' + '\033[0m'] * 3
    o3 = ['\033[1m' + 'O' + '\033[0m'] * 3
    
    if lst[1:4] == x3 or lst[4:7] == x3 or lst[7:10] == x3:
        win = 1
    elif lst[1:8:3] == x3 or lst[2:9:3] == x3 or lst[3:10:3] == x3:
        win = 1
    elif lst[1:10:4] == x3 or lst[3:8:2] == x3:
        win = 1
    
    elif lst[1:4] == o3 or lst[4:7] == o3 or lst[7:10] == o3:
        win = 2
    elif lst[1:8:3] == o3 or lst[2:9:3] == o3 or lst[3:10:3] == o3:
        win = 2
    elif lst[1:10:4] == o3 or lst[3:8:2] == o3:
        win = 2    
    
    elif positions == []:
        win = 3
    
    return win

main()