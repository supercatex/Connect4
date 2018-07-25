import numpy as np


class GameBoard:
    
    COLS = 7
    ROWS = 6
    CONNECT = 4
    
    
    def __init__(self):
        self.map = []
        for i in range(0, self.ROWS, 1):
            self.map.append([])
            for j in range(0, self.COLS, 1):
                self.map[i].append(0)
        
    
    def __str__(self):
        s = ''
        for i in range(self.ROWS - 1, -1, -1):
            for j in range(0, self.COLS, 1):
                if self.map[i][j] == 0:
                    s = s + '　'
                elif self.map[i][j] == 1:
                    s = s + '●'
                else:
                    s = s + '○'
            s = s + '\n'
        return s
    
    
    def getKey(self, player):
        s = '["'
        for i in range(self.ROWS - 1, -1, -1):
            for j in range(0, self.COLS, 1):
                if player == 1:
                    s = s + str(self.map[i][j])
                else:
                    if self.map[i][j] == 1:
                        s = s + '2'
                    elif self.map[i][j] == 2:
                        s = s + '1'
                    else:
                        s = s + '0'
        return s + '"]'
    
    
    def getState(self, step):
        temp = []
        for i in range(0, self.ROWS, 1):
            #temp.append([])
            for j in range(0, self.COLS, 1):
                if step % 2 == 0:
                    temp.append(self.map[i][j])
                else:
                    if self.map[i][j] == 1:
                        temp.append(2)
                    elif self.map[i][j] == 2:
                        temp.append(1)
                    else:
                        temp.append(0)
        return np.reshape(np.array(temp), [1, self.ROWS * self.COLS])
    
    
    def input_col(self, player):
        s = ''
        while s.isdigit() == False:
            s = input('Player %d input column from 1 to 7: ' % player)
        n = int(s) - 1
        if self.is_valid_col(n):
            return (self.move(n, player), n)
        else:
            print('this line is full.')
            return self.input_col(player)
        
    def is_valid_col(self, col):
        if col < 0 or col >= self.COLS: return False
        
        for i in range(0, self.ROWS, 1):
            if self.map[i][col] == 0:
                return True
        return False


    def move(self, col, step):
        for i in range(0, self.ROWS, 1):
            if self.map[i][col] == 0:
                self.map[i][col] = step % 2 + 1
                return self.is_connect4(i, col, step)
        return False
    
    
    def is_draw(self):
        for j in range(0, self.COLS, 1):
            if self.map[self.ROWS - 1][j] == 0:
                return False
        return True
    
    
    def is_connect4(self, row, col, step):
        player = step % 2 + 1
        
        n = 0
        for offset in range(-self.CONNECT, self.CONNECT + 1, 1):
            x = col + offset
            y = row 
            if x < 0 or x >= self.COLS: continue
            if self.map[y][x] == player:
                n = n + 1
                if n == self.CONNECT: return True
            else:
                n = 0
        
        n = 0
        for offset in range(-self.CONNECT, self.CONNECT + 1, 1):
            x = col
            y = row + offset 
            if y < 0 or y >= self.ROWS: continue
            if self.map[y][x] == player:
                n = n + 1
                if n == self.CONNECT: return True
            else:
                n = 0
        
        n = 0
        for offset in range(-self.CONNECT, self.CONNECT + 1, 1):
            x = col + offset
            y = row + offset
            if x < 0 or x >= self.COLS: continue
            if y < 0 or y >= self.ROWS: continue
            if self.map[y][x] == player:
                n = n + 1
                if n == self.CONNECT: return True
            else:
                n = 0
        
        n = 0
        for offset in range(-self.CONNECT, self.CONNECT + 1, 1):
            x = col - offset
            y = row + offset
            if x < 0 or x >= self.COLS: continue
            if y < 0 or y >= self.ROWS: continue
            if self.map[y][x] == player:
                n = n + 1
                if n == self.CONNECT: return True
            else:
                n = 0
                
        return False
