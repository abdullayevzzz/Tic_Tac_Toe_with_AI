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
        return ['finished', 'X']
    if o_wins:
        if not test:
            print('O wins')
        return ['finished', 'O']
    if any(['_' in row for row in table]):
        # print('Game not finished')
        return ['not_finished', 'C']  # continue
    else:
        if not test:
            print('Draw')
        return ['finished', 'D']  # draw


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
            coordinates = [int(coordinate) for coordinate in (user_input.split(' ')) if coordinate != '']
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


def hard_level(move, valued_coordinates={}, depth=0):
    global table
    available_coordinates = [[i, j] for i in range(3) for j in range(3) if table[i][j] == '_']
    for selected_coordinates in available_coordinates:
        table[selected_coordinates[0]][selected_coordinates[1]] = move
        st1, st2 = status_printer(test=1)
        if st1 == 'finished':
            if st2 == move:
                score = -1 if depth % 2 else 1
                valued_coordinates[score] = selected_coordinates
                table[selected_coordinates[0]][selected_coordinates[1]] = '_'
                break
            elif st2 == 'D':
                score = 0
                valued_coordinates[score] = selected_coordinates
                table[selected_coordinates[0]][selected_coordinates[1]] = '_'
                continue
        else:
            move_result = hard_level('X' if move == 'O' else 'O', valued_coordinates={}, depth=depth + 1)
            valued_coordinates[move_result] = selected_coordinates
            table[selected_coordinates[0]][selected_coordinates[1]] = '_'  # ?
    if depth % 2:
        depth -= 1
        return min([key for key in valued_coordinates])
    else:
        depth -= 1
        return max([key for key in valued_coordinates])


def get_comp_input(move, level='easy'):
    global table
    available_coordinates = [[i, j] for i in range(3) for j in range(3) if table[i][j] == '_']
    if level == 'hard':
        print('Making move level "hard"')
        valued_coordinates = {}
        hard_level(move, valued_coordinates)
        selected_coordinates = valued_coordinates[1] if 1 in valued_coordinates else valued_coordinates[0]
        table[selected_coordinates[0]][selected_coordinates[1]] = move
        return
    if level == 'medium':
        print('Making move level "medium"')
        for selected_coordinates in available_coordinates:
            table[selected_coordinates[0]][selected_coordinates[1]] = move
            if status_printer(test=1)[0] == 'finished':
                return
            else:
                table[selected_coordinates[0]][selected_coordinates[1]] = '_'
        for selected_coordinates in available_coordinates:
            table[selected_coordinates[0]][selected_coordinates[1]] = 'X' if move == 'O' else 'O'
            if status_printer(test=1)[0] == 'finished':
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
    for item in inp:
        if item == '':
            inp.remove(item)
    if len(inp) == 1 and inp[0] == 'exit':
        quit()
    elif len(inp) == 3 and inp[0] == 'start' and all(item in ['user', 'easy', 'medium', 'hard'] for item in inp[1:3]):
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
    if status_printer()[0] == 'finished':
        break
    get_user_input('O') if players[1] == 'user' else get_comp_input('O', players[1])
    table_printer()
    if status_printer()[0] == 'finished':
        break