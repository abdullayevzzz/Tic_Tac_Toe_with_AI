# write your code here
import random
table = []
state = ''
player_move = 'X'
players = ['user', 'easy']


def create_table():
    global table
    #  initial_input = input('Enter the cells: ')
    table = [['_'] * 3 for i in range(3)]
    initial_input = '_' * 9
    for i in range(3):
        for j in range(3):
            table[i][j] = (initial_input[i * 3 + j])


def table_printer():
    print('-' * 9)
    for i in range(3):
        row = ''
        for char in table[i]:
            if char == '_':
                char = ' '
            row += char + ' '
        print('| ', row, '|', sep='')
    print('-' * 9)


def transpose_table():
    transposed_table = [['_'] * 3 for i in range(3)]
    for i in range(3):
        for j in range(3):
            transposed_table[j][i] = table[i][j]
    return transposed_table


def status_printer(test=0):
    x_wins = False
    o_wins = False
    for i in range(0, 3):
        if all(char == 'X' for char in table[i]) or all(char == 'X' for char in transpose_table()[i]):
            x_wins = True
            break
    if all(table[i][i] == 'X' for i in range(0, 3)) or all(table[2 - i][i] == 'X' for i in range(0, 3)):
        x_wins = True
    for i in range(0, 3):
        if all(char == 'O' for char in table[i]) or all(char == 'O' for char in transpose_table()[i]):
            o_wins = True
            break
    if all(table[i][i] == 'O' for i in range(0, 3)) or all(table[2 - i][i] == 'O' for i in range(0, 3)):
        o_wins = True
    if x_wins:
        if not test:
            print('X wins')
        return 'finished'
    if o_wins:
        if not test:
            print('O wins')
        return 'finished'
    if any(['_' in row for row in table]):
        # print('Game not finished')
        return 'not_finished'
    else:
        if not test:
            print('Draw')
        return 'finished'


def find_player_move():
    global player_move
    x_count = 0
    o_count = 0
    for row in table:
        x_count += row.count('X')
        o_count += row.count('O')
    if x_count > o_count:
        player_move = 'O'


def get_user_input(move):
    global table
    while True:
        try:
            user_input = input('Enter the coordinates: ')
            coordinates = [int(coordinate) for coordinate in (''.join(user_input).split(' '))]
        except ValueError:
            print('You should enter numbers!')
            continue
        if not all([coordinate in range(1, 4) for coordinate in coordinates]):
            print('Coordinates should be from 1 to 3!')
            continue
        if table[coordinates[0] - 1][coordinates[1] - 1] != '_':
            print('This cell is occupied! Choose another one!')
            continue
        else:
            table[coordinates[0] - 1][coordinates[1] - 1] = move
            break


def get_comp_input(move, level='easy'):
    global table
    available_coordinates = [[i, j] for i in range(3) for j in range(3) if table[i][j] == '_']
    if level == 'medium':
        print('Making move level "medium"')
        for selected_coordinates in available_coordinates:
            table[selected_coordinates[0]][selected_coordinates[1]] = move
            if status_printer(test=1) == 'finished':
                return
            else:
                table[selected_coordinates[0]][selected_coordinates[1]] = '_'
        for selected_coordinates in available_coordinates:
            table[selected_coordinates[0]][selected_coordinates[1]] = 'X' if move == 'O' else 'O'
            if status_printer(test=1) == 'finished':
                table[selected_coordinates[0]][selected_coordinates[1]] = move
                return
            else:
                table[selected_coordinates[0]][selected_coordinates[1]] = '_'
    elif level == 'easy':
        print('Making move level "easy"')
    selected_coordinates = random.choice(available_coordinates)
    table[selected_coordinates[0]][selected_coordinates[1]] = move


def command_handler():
    global player_move
    global players
    inp = input('Input command: ').split()
    if len(inp) == 1 and inp[0] == 'exit':
        quit()
    elif len(inp) == 3 and inp[0] == 'start' and all(item in ['user', 'easy', 'medium'] for item in inp[1:3]):
        players[0] = inp[1]
        players[1] = inp[2]
    else:
        print('Bad parameters!')
        command_handler()


create_table()
command_handler()
table_printer()
# find_player_move()
while True:
    get_user_input('X') if players[0] == 'user' else get_comp_input('X', players[0])
    table_printer()
    if status_printer() == 'finished':
        break
    get_user_input('O') if players[1] == 'user' else get_comp_input('O', players[1])
    table_printer()
    if status_printer() == 'finished':
        break
