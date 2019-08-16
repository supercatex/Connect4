import numpy as np


class GameBoard:

    _COLS = 7
    _ROWS = 6
    _WIN = 4
    _PIECES = [" ", "O", "X"]

    def __init__(self):
        self.board = np.zeros((GameBoard._ROWS, GameBoard._COLS), np.uint8)
        self.steps = []

    def printout(self):
        temp = self.board.astype(np.str)
        temp = np.where(temp == "0", " ", temp)
        temp = np.where(temp == "1", "O", temp)
        temp = np.where(temp == "2", "X", temp)

        print("  _______________")
        i = 0
        for row in temp:
            print(i, end=" ")
            i += 1
            for col in row:
                print("|%s" % col, end="")
            print("|")
        print("  ===============")
        print("   0 1 2 3 4 5 6 ")

        print("Step:", len(self.steps))
        if len(self.steps) > 0:
            print("Last move:", self.steps[-1])

    def move(self, col):
        if col < 0 or col >= GameBoard._COLS:
            return False

        rows = np.argwhere(self.board[:, col] == 0)
        if len(rows) == 0:
            return False

        row = np.argmax(rows)

        coin = len(self.steps) % 2 + 1
        self.board[row, col] = coin
        self.steps.append(col)
        return True

    def valid_move(self):
        rows = np.argwhere(self.board == 0)
        return np.unique(rows[:, 1])

    def check_four(self):
        for k in range(2):
            player = k + 1
            for i in range(GameBoard._ROWS):
                count = 0
                for j in range(GameBoard._COLS):
                    if self.board[i, j] == player:
                        count += 1
                    else:
                        if count >= GameBoard._WIN:
                            print(GameBoard._PIECES[player], i, j - count, count, "--")
                        count = 0
                if count >= GameBoard._WIN:
                    print(GameBoard._PIECES[player], i, GameBoard._COLS - count, count, "--")

        for k in range(2):
            player = k + 1
            for j in range(GameBoard._COLS):
                count = 0
                for i in range(GameBoard._ROWS):
                    if self.board[i, j] == player:
                        count += 1
                    else:
                        if count >= GameBoard._WIN:
                            print(GameBoard._PIECES[player], i - count, j, count, "|")
                        count = 0
                if count >= GameBoard._WIN:
                    print(GameBoard._PIECES[player], GameBoard._ROWS - count, j, count, "|")

        for k in range(2):
            player = k + 1
            for i in range(GameBoard._WIN - 1, GameBoard._ROWS):
                count = 0
                for j in range(0, i + 1):
                    if self.board[i - j, j] == player:
                        count += 1
                    else:
                        if count >= GameBoard._WIN:
                            print(GameBoard._PIECES[player], i - j + count, j - count, count, "/")
                        count = 0
                if count >= GameBoard._WIN:
                    print(GameBoard._PIECES[player], count - 1, i + 1 - count, count, "/")



if __name__ == "__main__":
    game = GameBoard()
    game.printout()

    for i in range(42):
        choice = game.valid_move()
        if len(choice) > 0:
            game.move(np.random.choice(choice))
        game.printout()

    print(game.check_four())
