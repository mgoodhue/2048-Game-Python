import gamelogic as gl
import unittest
import numpy as np

class TestBoard(unittest.TestCase):

    def test_normal_board_init(self):
        # Create a normal board
        board = gl.Board()
        self.assertEqual(board.size, 4, "Board size should be 4")
        self.assertEqual(board.difficulty, "normal", "Difficulty should be 'normal'")
        self.assertEqual(board.score, 0, "Initial score should be 0")

        print("Test normal_board_init passed")

    def test_hard_board_init(self):
        # Create a hard board
        board = gl.BoardHard()
        self.assertEqual(board.size, 4, "Board size should be 4")
        self.assertEqual(board.difficulty, "normal", "Difficulty should be 'normal'")
        self.assertEqual(board.score, 0, "Initial score should be 0")

        print("Test normal_board_init passed")

    def test_make_board(self):
        # Create a Board instance for testing
        board_instance = gl.Board()

        # Call the make_board method
        board = board_instance.make_board()

        # Check if the board is created correctly
        self.assertIsInstance(
            board, 
            np.ndarray, 
            "The board should be a NumPy array")
        
        # Check if the board has the correct size
        self.assertEqual(
            board.shape, 
            (board_instance.size, board_instance.size), 
            "The board should have the correct size")

        # Check if there are two 2s in the board
        num_twos = np.sum(board == 2)
        self.assertEqual(
            num_twos, 
            2, 
            "The starting board should contain two 2s")
        
        print("Test make_board passed")

    def test_add_val_two(self):
        # Create a Board instance for testing
        board_instance = gl.Board()

        # Test the add_val method with mocked randomness (returning 2)
        board = np.zeros((board_instance.size, board_instance.size), dtype=int)
        board_instance.add_val(board, 2)

        # Assertions to check if the value 2 is correctly added
        self.assertIn(2, board, "The value 2 should be in the board")

        print("Test add_val (2) passed")

    def test_add_val_four(self):
        # Create a Board instance for testing
        board_instance = gl.Board()

        # Test the add_val method with mocked randomness (returning 4)
        board = np.zeros((board_instance.size, board_instance.size), dtype=int)
        board_instance.add_val(board, 4)

        # Assertions to check if the value 4 is correctly added
        self.assertIn(4, board, "The value 4 should be in the board")

        print("Test add_val (4) passed")

    def test_shift_zeroes(self):
        # Create a Board instance for testing
        arr1 = np.array([1, 2, 0, 3, 0, 2])

        # Check if zeroes are shifted to the back
        gl.Board.shift_zeroes(arr1, True)
        self.assertTrue(
            np.array_equal(arr1, np.array([1, 2, 3, 2, 0, 0])),
            "Zeroes should be shifted to back")
        
        # Check if zeroes are shifted to the front
        gl.Board.shift_zeroes(arr1, False)
        self.assertTrue(
            np.array_equal(arr1, np.array([0, 0, 1, 2, 3, 2])),
            "Zeroes should be shifted to front")
        
        # Check if empty array is unchanged by shifting
        empty = np.array([0, 0, 0])
        gl.Board.shift_zeroes(empty, True)
        self.assertTrue(
            np.array_equal(empty, np.array([0, 0, 0])),
            "Empty array shifted returns the same array")
        
        # Check if already-shifted array is unchanged by shifting
        arr2 = np.array([1, 2, 0, 0])
        gl.Board.shift_zeroes(arr2, True)
        self.assertTrue(
            np.array_equal(arr2, np.array([1, 2, 0, 0])),
            "Given array is already shifted and should not change")

        print("Test shift_zeroes passed")

    def test_combine(self):
        self.score = 0

        # Check combining to the front
        arr1 = np.array([2, 2, 0, 2])
        gl.Board.combine(self, arr1, True)
        self.assertTrue(
            np.array_equal(arr1, np.array([4, 0, 0, 2])),
            "Adjacent elements should combine to the front.")
        
        # Check combining to the back
        arr2 = np.array([2, 2, 0, 2])
        gl.Board.combine(self, arr2, False)
        self.assertTrue(
            np.array_equal(arr2, np.array([0, 4, 0, 2])),
            "Adjacent elements should combine to the back.")
        
        # Check combining non-adjacent elements
        arr3 = np.array([2, 0, 0, 2])
        gl.Board.combine(self, arr3, True)
        self.assertTrue(
            np.array_equal(arr3, np.array([2, 0, 0, 2])),
            "Elements must be adjacent to combine.")
        
        # Check combining on empty array
        arr4 = np.array([0, 0, 0, 0])
        gl.Board.combine(self, arr4, True)
        self.assertTrue(
            np.array_equal(arr4, np.array([0, 0, 0, 0])),
            "Empty array does not change when combined.")
        
        print("Test combine passed")
        
    def test_insta_win(self):
        # Create a Board instance for testing
        board_instance = gl.Board()

        # Call the insta_win method
        board_instance.insta_win()

        # Check if the top-left corner has the value 2048
        self.assertEqual(
            board_instance.board[0, 0], 
            2048, 
            "The value 2048 should appear in the top-left corner of the board"
        )

        print("Test insta_win passed")

    def test_insta_lose(self):
        # Create a Board instance for testing
        board_instance = gl.Board()

        # Call insta_lose
        board_instance.insta_lose()

        # Check if each cell in the board has a unique value starting from 1
        count = 1
        for i in range(board_instance.size):
            for j in range(board_instance.size):
                self.assertEqual(
                    board_instance.board[i, j],
                    count,
                    f"The cell at ({i}, {j}) should have the value {count}"
                )
                count += 1

        print("Test insta_lose passed")

    def test_reset_board(self):
        # Create a Board instance for testing
        board_instance = gl.Board()

        # Create initial board
        initial_board = np.array([[2, 4, 0, 0],
                                  [0, 0, 8, 0],
                                  [0, 16, 0, 0],
                                  [32, 0, 0, 64]])

        # Set initial score
        initial_score = 100

        # Assign values to Board instance
        board_instance.board = initial_board
        board_instance.score = initial_score

        # Call the reset_board method
        board_instance.reset_board()

        # Check if the board is reset to a new random board
        self.assertFalse(
            np.array_equal(board_instance.board, initial_board),
            "The board should not be the same after resetting"
        )

        # Check if the score is reset to 0
        self.assertEqual(
            board_instance.score,
            0,
            "The score should be reset to 0"
        )

        print("Test reset_board passed")

    def test_move(self):
        # Create a Board instance for testing
        board_instance = gl.Board()

        # Set the board to a known state
        initial_board = np.array([[2, 4, 0, 2],
                                  [0, 0, 8, 0],
                                  [0, 16, 0, 0],
                                  [32, 0, 0, 64]])

        # Assign the known board to the instance
        board_instance.board = initial_board

        # Capture the sum of the board before calling move
        sum_before_move = np.sum(board_instance.board)
        non_zeroes_before_move = np.count_nonzero(board_instance.board)

        # Call the move method with the 'left' direction
        board_instance.move('left')

        # Check if the sum of the board increased after moving
        sum_after_move = np.sum(board_instance.board)
        non_zeroes_after_move = np.count_nonzero(board_instance.board)

        # Check if sum of all elements on board increases after move
        self.assertTrue(
            sum_after_move > sum_before_move,
            "After moving, the sum of the board should increase by 2 or 4"
        )

        # Check if there is one less empty space after a move with no combinations
        self.assertEqual(
            non_zeroes_after_move,
            non_zeroes_before_move + 1,
            "After moving, an empty space should be filled with a 2 or a 4"
        )

        # Set up a board with combinable values
        combinable_board = np.array([[2, 4, 0, 2],
                                     [0, 4, 8, 0],
                                     [0, 16, 0, 0],
                                     [32, 0, 0, 64]])
        
        # Assign above board to Board instance
        board_instance.board = combinable_board

        # Check number of filled spaces before combining
        non_zeroes_before_combine = np.count_nonzero(board_instance.board)

        # Move up on the board
        board_instance.move('up')

        # Count the number of filled spaces after moving (Shifting and combining)
        non_zeroes_after_combine = np.count_nonzero(board_instance.board)

        # Check if number of filled spaces is the 
        # same (One combination, one new number added)
        self.assertEqual(
            non_zeroes_before_combine,
            non_zeroes_after_combine,
            "One combination should reduce nonzeroes by 1, " 
            + "and a new nonzero should be added," 
            + "keeping the number of nonzeroes constant."
        )

        print("Test move passed")

    def test_has_won(self):
        # Create a Board instance for testing
        board_instance = gl.Board()

        # Set the board to a known state
        initial_board = np.array([[2, 4, 0, 2],
                                  [0, 0, 8, 0],
                                  [0, 16, 0, 0],
                                  [32, 0, 0, 64]])

        # Assign the known board to the instance
        board_instance.board = initial_board
        self.assertFalse(board_instance.has_won(), "Player should not have won")

        # Create a winning board example
        winning_board = np.array([[2, 4, 0, 2],
                                  [0, 0, 8, 0],
                                  [0, 16, 2048, 0],
                                  [32, 0, 0, 64]])
        
        # Set the board instance to the winning board
        board_instance.board = winning_board
        # Check if the board counts as winning
        self.assertTrue(board_instance.has_won(), "Player should have won")

        print("Test has_won passed")

    def test_has_lost(self):
        # Create a Board instance for testing
        board_instance = gl.Board()

        # Create an in-process board state(Hasn't won or lost)
        not_lost_board = np.array([[2, 4, 0, 2],
                                   [0, 0, 8, 0],
                                   [0, 16, 0, 0],
                                   [32, 0, 0, 64]])
        
        # Create an in-process board that has no empty spaces
        not_lost_full_board = np.array([[2, 4, 8, 16],
                                        [16, 8, 4, 2],
                                        [2, 4, 8, 16],
                                        [16, 16, 4, 2]])
        
        # Create a board that has been lost
        lost_board = np.array([[2, 4, 8, 16],
                               [16, 8, 4, 2],
                               [2, 4, 8, 16],
                               [16, 8, 4, 2]])
        
        # Set the Board instance to the losing board
        board_instance.board = lost_board

        # Check if having this board counts as a loss
        self.assertTrue(
            board_instance.has_lost(),
            "The game should be lost only with no" 
            + "matching adjacent elements and no space left"
        )

        # Set the Board instance to the non-losing board
        board_instance.board = not_lost_board

        # Check that the non-losing board 
        # does not count as a loss
        self.assertFalse(
            board_instance.has_lost(),
            "The game should be lost only" 
            + "with no matching adjacent elements and no space left"
        )

        # Set the Board instance to the non-losing but full board
        board_instance.board = not_lost_full_board

        # Check that the full, non-losing board 
        # does not count as a loss
        self.assertFalse(
            board_instance.has_lost(),
            "The game should be lost only" 
            + "with no matching adjacent elements and no space left"
        )

        # Create an empty board 
        empty_board = np.zeros((4, 4), dtype=int)

        # Set the Board instance to the empty board
        board_instance.board = empty_board

        # Check that the empty board
        # does not count as a loss
        self.assertFalse(
            board_instance.has_lost(),
            "The game should not be lost with an empty board"
        )

        print("Test has_lost passed")

    def test_clear_board(self):
         # Create a BoardEasy instance for testing
        board_instance = gl.BoardEasy()

        # Set up an in-process board state
        initial_board = np.array([[2, 4, 0, 2],
                                  [0, 0, 8, 0],
                                  [0, 16, 0, 0],
                                  [32, 0, 0, 64]])

        # Assign the Board instance to the in-process board state
        board_instance.board = initial_board

        # Clear the board 
        board_instance.clear_board()

        # Example of correctly cleared version of initial board
        cleared_board = np.array([[0, 64, 32, 16],
                                  [0, 0, 0, 0],
                                  [0, 0, 0, 0],
                                  [0, 0, 0, 0]])
        
        # Check if the board has been correctly cleared
        self.assertTrue(
            np.array_equal(cleared_board, board_instance.board),
            "Board should have 3 descending values in the top left."
        )

        print("Test clear_board passed")


if __name__ == "__main__":
    unittest.main()