import numpy as np
import random

# Regular Board Class to manage game
class Board:
    """
    Board class to represent a
    standard 2048 game board.
    """
    # User inputs for board size and difficulty
    def __init__(self, size=4, difficulty="normal"):
        self.board = self.make_board()
        self.score = 0
        self.size = size
        self.difficulty = difficulty

    def make_board(self):
        """
        Creates a starting board with correct size
        Adds a two to two random empty spaces.
        """
        board = np.zeros((4, 4), dtype=int)
        self.add_val(board, 2)
        self.add_val(board, 2)
        return board
    
    @staticmethod
    def add_val(arr, val):
        """
        Adds a new value to an empty space in the given array. 
        Value is either a 2 or a 4.
        """
        # Find indices of empty spaces
        zero_indices = np.argwhere(arr == 0)
        # Randomly choose index of an empty space
        random_index = np.random.choice(zero_indices.shape[0])

        # Split random index into row and column index
        row_index, col_index = zero_indices[random_index]

        # Set random empty space to given value
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
                # Same operation as above but in reverse direction
                arr[-len(non_zero_indices):] = arr[non_zero_indices]
                arr[:-len(non_zero_indices)] = 0
                
        else:
            arr[:] = 0         

    def combine(self, arr, to_front=None):
        """
        Combines adjacent values in the given 
        1-D array, with the direction depending 
        on the boolean to_front.
        """
        if to_front:
            for i in range(len(arr) - 1):
                if arr[i] == arr[i+1] and arr[i] != 0:
                    # Current value multiplied by two
                    arr[i] *= 2
                    # Adjacent, equal value to right removed
                    arr[i+1] = 0 
                    # Current, doubled value added to score
                    self.score += arr[i]

        else:
            for i in range(len(arr) - 1, 0, -1):
                if arr[i] == arr[i-1] and arr[i] != 0:
                    # Current value multiplied by two
                    arr[i] *= 2
                    # Adjacent, equal value to left removed
                    arr[i-1] = 0 
                    # Current, doubled value added to score
                    self.score += arr[i]

    def insta_win(self):
        """
        Instantly wins the game. 
        Helpful for testing win screen display.
        """
        self.board[0, 0] = 2048

    def insta_lose(self):
        """
        Instantly loses the game. 
        Helpful for testing lose screen display.
        """
        count = 1
        for i in range(self.size):
            for j in range(self.size):
                self.board[i, j] = count
                count += 1

    def reset_board(self):
        """
        Resets board to random starting board 
        with the same difficulty.
        """
        self.board = self.make_board()
        self.score = 0
    
    def move(self, direction):
        """
        Moves non-empty tiles around the board 
        up, down, left, or right, depending on 
        the user-input direction.
        """
        # Store state of board before move is executed
        prev_board = np.copy(self.board)
        for i in range(self.size):

            # Move left
            if direction == 'left':
                to_front = True
                self.shift_zeroes(self.board[i, :], to_front)
                self.combine(self.board[i, :], to_front)
                self.shift_zeroes(self.board[i, :], to_front)
            
            # Move right
            elif direction == 'right':
                to_front = False
                self.shift_zeroes(self.board[i, :], to_front)
                self.combine(self.board[i, :], to_front)
                self.shift_zeroes(self.board[i, :], to_front)
                
            # Move up
            elif direction == 'up':
                to_front = True
                self.shift_zeroes(self.board[:, i], to_front)
                self.combine(self.board[:, i], to_front)
                self.shift_zeroes(self.board[:, i], to_front)
                
            # Move down
            elif direction == 'down':
                to_front = False
                self.shift_zeroes(self.board[:, i], to_front)
                self.combine(self.board[:, i], to_front)
                self.shift_zeroes(self.board[:, i], to_front)
        
        # Check to see that the move changed the state of the board
        if not np.array_equal(prev_board, self.board):
            new_num = random.choice([2, 4])
            self.add_val(self.board, new_num)


    def has_won(self):
        """
        Checks if the player has won the game 
        by reaching 2048.
        """
        return np.any(self.board >= 2048)

    def has_lost(self):
        """
        Checks if the player has lost the game 
        by being unable to move and having no 
        2048 space present.
        """
        
        if np.all(self.board != 0):
            # Check if there are any equal, 
            # adjacent numbers in vertical direction
            for i in range(self.size):
                for j in range(self.size - 1):
                    if self.board[i, j] == self.board[i, j + 1]:
                        return False

            # Check if there are any equal, 
            # adjacent numbers in horizontal direction
            for j in range(self.size):
                for i in range(self.size - 1):
                    if self.board[i, j] == self.board[i + 1, j]:
                        return False

            return True

        return False

# Board class for an easier version of 2048
class BoardEasy(Board):

    def __init__(self, size=4, difficulty="easy"):
        super().__init__(size=size, difficulty=difficulty)

    def clear_board(self):
        max_value = np.max(self.board)
        self.board = np.zeros((self.size, self.size), dtype=int)
        self.board[0, 1] = max_value
        if max_value > 4:
            self.board[0, 2] = max_value / 2
            self.board[0, 3] = max_value / 4

# Board class for a harder version of 2048
class BoardHard(Board):

    def __init__(self, size=4, difficulty="hard"):
        super().__init__(size=size, difficulty=difficulty)

    
    def move(self, direction):
        """
        Moves non-empty tiles around the board 
        up, down, left, or right, depending on 
        the user-input direction. An extra 2 
        or 4 may appear after each move.
        """
        # Store state of board before move is executed
        prev_board = np.copy(self.board)
        for i in range(self.size):

            # Move left
            if direction == 'left':
                to_front = True
                self.shift_zeroes(self.board[i, :], to_front)
                self.combine(self.board[i, :], to_front)
                self.shift_zeroes(self.board[i, :], to_front)
            
            # Move right
            elif direction == 'right':
                to_front = False
                self.shift_zeroes(self.board[i, :], to_front)
                self.combine(self.board[i, :], to_front)
                self.shift_zeroes(self.board[i, :], to_front)
                
            # Move up
            elif direction == 'up':
                to_front = True
                self.shift_zeroes(self.board[:, i], to_front)
                self.combine(self.board[:, i], to_front)
                self.shift_zeroes(self.board[:, i], to_front)
                
            # Move down
            elif direction == 'down':
                to_front = False
                self.shift_zeroes(self.board[:, i], to_front)
                self.combine(self.board[:, i], to_front)
                self.shift_zeroes(self.board[:, i], to_front)
        
        # Check to see if the move modified the state of the board
        if not np.array_equal(prev_board, self.board):
            new_num = random.choice([2, 4])
            self.add_val(self.board, new_num)
            # 1/25 chance of two numbers appearing 
            # on the board instead of one
            if random.randint(0, 25) == 7:
                self.add_val(self.board, new_num)

        