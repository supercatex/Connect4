
_rows = 6
_cols = 7
_board = []
for i in range(_rows):
    _row_list = []
    for j in range(_cols):
        _row_list.append(0)
    _board.append(_row_list)


def print_board(board):
    for row in board:
        print(row)


def find_empty_row(board, column):
    if column < 0 or column >= len(board[0]):
        return None
    i = 0
    while board[i][column] != 0:
        i = i + 1
        if i >= len(board):
            return None
    return i


def check_win(board):
    for p in range(1, 3, 1):
        for row in board:
            c = 0
            for i in range(len(row)):
                if p == row[i]:
                    c += 1
                else:
                    c = 0
                if c >= 4:
                    return True
    return False


print_board(_board)

i = 0
while i < _rows * _cols:
    _player = i % 2 + 1
    _user_input = input("P%d:" % (_player))
    _user_input_index = int(_user_input)
    _return = find_empty_row(_board, _user_input_index)
    if _return is None:
        print("No empty space!")
        continue
    _board[_return][_user_input_index] = _player
    print_board(_board)

    if check_win(_board):
        print("P%d WIN!!!" % (_player))
        break

    i = i + 1
