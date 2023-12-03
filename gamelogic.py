import numpy as np

class Board:
    SIZE = 4

    def __init__(self):
        self.board = np.zeros((4, 4))

    def has_won(self):
        """
        Returns true if a 2048 value is present.
        Returns false otherwise.
        """
        return np.all(self.board == 2048)
    
    def has_lost(self):
        """
        Returns true if the board is full of values
        that are not equal to 0 or 2048 and the player
        has lost. 
        Returns false otherwise.
        """
        return np.all((self.board != 0) and (self.board != 2048))
    
    @staticmethod
    def shift_zeroes(arr, to_front=True):
        """
        Shifts all non-zero elements of a 1-D
        array to the front or the back of the
        array, depending on the boolean input to_front.
        """
        non_zero_indices = np.nonzero(arr)
        if to_front:
            arr[:len(non_zero_indices)] = arr[non_zero_indices]
            arr[len(non_zero_indices):] = 0
        else:
            arr[len(non_zero_indices):] = arr[non_zero_indices]
            arr[:len(non_zero_indices)] = 0
    
    def move(self, direction):
        for i in range(Board.SIZE):
            if direction == 'up':
                self.shift_zeroes(self.board[i, :], to_front=True)
            elif direction == 'down':
                self.shift_zeroes(self.board[i, :], to_front=False)
            elif direction == 'left':
                self.shift_zeroes(self.board[:, i], to_front=True)
            elif direction == 'right':
                self.shift_zeroes(self.board[:, i], to_front=False)

class Game:
    
    def __init__(self):
        self.board = Board()
        self.score = 0

    
        


