import numpy as np
import random

class Board:

    SIZE = int(input("Choose Board Size: "))
    DIFFICULTY = input("Choose Difficulty(Easy/Normal/Hard):").lower()

    def __init__(self): 
        self.board = self.make_board()
        self.score = 0
        self.size = self.SIZE
        self.difficulty = self.DIFFICULTY

    def make_board(self):
        board = np.zeros((Board.SIZE, Board.SIZE), dtype=int)
        self.add_val(board, 2)
        self.add_val(board, 2)
        return board
    
    @staticmethod
    def add_val(arr, val):
        zero_indices = np.argwhere(arr == 0)
        random_index = np.random.choice(zero_indices.shape[0])

        row_index, col_index = zero_indices[random_index]

        arr[row_index, col_index] = val
    
    @staticmethod
    def shift_zeroes(arr, to_front):
        """
        Shifts all non-zero elements of a 1-D
        array to the front or the back of the
        array, depending on the boolean argument to_front.
        """
        # Creates list of the indices of non-zero values within
        # a single row/column
        non_zero_indices = np.nonzero(arr)[0]
        if len(non_zero_indices) > 0:
            if to_front:
                # The number of non-zero values in the list is taken and
                # used to slice the array up to this number. The indices
                # up to this number are then changed to the non-zero values,
                # retaining their order. 
                arr[:len(non_zero_indices)] = arr[non_zero_indices]
                arr[len(non_zero_indices):] = 0
            else:
                arr[-len(non_zero_indices):] = arr[non_zero_indices]
                arr[:-len(non_zero_indices)] = 0
                
        else:
            arr[:] = 0         

    def combine(self, arr, to_front=None):
        if to_front:
            for i in range(len(arr) - 1):
                if arr[i] == arr[i+1] and arr[i] != 0:
                    arr[i] *= 2
                    arr[i+1] = 0 
                    self.score += arr[i]

        else:
            for i in range(len(arr) - 1, 0, -1):
                if arr[i] == arr[i-1] and arr[i] != 0:
                    arr[i] *= 2
                    arr[i-1] = 0 
                    self.score += arr[i]

    def insta_win(self):
        self.board[0, 0] = 2048

    def insta_lose(self):
        count = 1
        for i in range(self.size):
            for j in range(self.size):
                self.board[i, j] = count
                count += 1

    def reset_board(self):
        self.board = self.make_board()
        self.score = 0
    
    def move(self, direction):
        
        prev_board = np.copy(self.board)
        for i in range(self.size):

            if direction == 'left':
                to_front = True
                self.shift_zeroes(self.board[i, :], to_front)
                self.combine(self.board[i, :], to_front)
                self.shift_zeroes(self.board[i, :], to_front)

            elif direction == 'right':
                to_front = False
                self.shift_zeroes(self.board[i, :], to_front)
                self.combine(self.board[i, :], to_front)
                self.shift_zeroes(self.board[i, :], to_front)
                
            elif direction == 'up':
                to_front = True
                self.shift_zeroes(self.board[:, i], to_front)
                self.combine(self.board[:, i], to_front)
                self.shift_zeroes(self.board[:, i], to_front)
                
            elif direction == 'down':
                to_front = False
                self.shift_zeroes(self.board[:, i - 1], to_front)
                self.combine(self.board[:, i - 1], to_front)
                self.shift_zeroes(self.board[:, i - 1], to_front)
        
        if not np.array_equal(prev_board, self.board):
            new_num = random.choice([2, 4])
            self.add_val(self.board, new_num)

    def has_won(self):
        return np.any(self.board >= 2048)

    def has_lost(self):
        if np.all(self.board != 0):
            for i in range(self.size):
                for j in range(self.size - 1):
                    if self.board[i, j] == self.board[i, j + 1]:
                        return False

            for j in range(self.size):
                for i in range(self.size - 1):
                    if self.board[i, j] == self.board[i + 1, j]:
                        return False

            return True

        return False


class BoardEasy(Board):

    def __init__(self):
        super().__init__()

    def clear_board(self):
        max_value = np.max(self.board)
        self.board = np.zeros((Board.SIZE, Board.SIZE), dtype=int)
        self.board[0, 0] = max_value

class BoardHard(Board):

    def __init__(self):
        super().__init__()

    def move(self, direction):
        
        prev_board = np.copy(self.board)
        for i in range(self.size):

            if direction == 'left':
                to_front = True
                self.shift_zeroes(self.board[i, :], to_front)
                self.combine(self.board[i, :], to_front)
                self.shift_zeroes(self.board[i, :], to_front)

            elif direction == 'right':
                to_front = False
                self.shift_zeroes(self.board[i, :], to_front)
                self.combine(self.board[i, :], to_front)
                self.shift_zeroes(self.board[i, :], to_front)
                
            elif direction == 'up':
                to_front = True
                self.shift_zeroes(self.board[:, i], to_front)
                self.combine(self.board[:, i], to_front)
                self.shift_zeroes(self.board[:, i], to_front)
                
            elif direction == 'down':
                to_front = False
                self.shift_zeroes(self.board[:, i - 1], to_front)
                self.combine(self.board[:, i - 1], to_front)
                self.shift_zeroes(self.board[:, i - 1], to_front)
        
        if not np.array_equal(prev_board, self.board):
            new_num = random.choice([2, 4])
            self.add_val(self.board, new_num)
            if random.randint(0, 25) == 0:
                self.add_val(self.board, new_num)
    