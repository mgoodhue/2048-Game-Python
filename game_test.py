import gamelogic as gl
import unittest
import numpy as np

class TestBoard(unittest.TestCase):

    def assertArrayEqual(self, first, second, msg=None):
        """
        Compares numpy arrays to see if they are equal.
        """
        self.assertTrue(np.array_equal(first, second), msg=msg)

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
        gl.Board.shift_zeroes(arr1, True)
        self.assertArrayEqual(
            arr1,
            np.array([1, 2, 3, 2, 0, 0]),
            "Zeroes must be shifted to front")
        gl.Board.shift_zeroes(arr1, False)
        self.assertArrayEqual(
            arr1,
            np.array([0, 0, 1, 2, 3, 2]),
            "Zeroes must be shifted to end of array")
        
        empty = np.array([0, 0, 0])
        gl.Board.shift_zeroes(empty, True)
        self.assertArrayEqual(
            empty,
            np.array([0, 0, 0]),
            "Empty array shifted returns the same array")
        
        arr2 = np.array([1, 2, 0, 0])
        gl.Board.shift_zeroes(arr2, True)
        self.assertArrayEqual(
            arr2,
            np.array([1, 2, 0, 0]),
            "Given array is already shifted and should not change")

        print("Test shift_zeroes passed")

    def test_combine(self):
        self.score = 0
        arr1 = np.array([2, 2, 0, 2])
        gl.Board.combine(self, arr1, True)
        self.assertArrayEqual(
            arr1,
            np.array([4, 0, 0, 2]),
            "Adjacent elements should combine to the front.")
        
        arr2 = np.array([2, 2, 0, 2])
        gl.Board.combine(self, arr2, False)
        self.assertArrayEqual(
            arr2,
            np.array([0, 4, 0, 2]),
            "Adjacent elements should combine to the back.")
        
        arr3 = np.array([2, 0, 0, 2])
        gl.Board.combine(self, arr3, True)
        self.assertArrayEqual(
            arr3,
            np.array([2, 0, 0, 2]),
            "Elements must be adjacent to combine.")
        
        arr4 = np.array([0, 0, 0, 0])
        gl.Board.combine(self, arr4, True)
        self.assertArrayEqual(
            arr4,
            np.array([0, 0, 0, 0]),
            "Empty array does not change when combined.")
        
        print("Test combine passed")
        
    def test_insta_win(self):
        # Create a Board instance for testing
        board_instance = gl.Board()

        # Call the insta_win method
        board_instance.insta_win()

        # Check if only the top-left corner has the value 2048
        self.assertEqual(
            board_instance.board[0, 0], 
            2048, 
            "The value 2048 should be in the top-left corner of the board"
        )

        print("Test insta_win passed")

    def test_insta_lose(self):
        # Create a Board instance for testing
        board_instance = gl.Board()

        # Call the insta_lose method
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

        # Set the board to a known state
        initial_board = np.array([[2, 4, 0, 0],
                                  [0, 0, 8, 0],
                                  [0, 16, 0, 0],
                                  [32, 0, 0, 64]])

        # Set the score to a known value
        initial_score = 100

        # Assign known values to board and score
        board_instance.board = initial_board
        board_instance.score = initial_score

        # Call the reset_board method
        board_instance.reset_board()

        # Check if the board is reset to a new random board
        self.assertNotEqual(
            board_instance.board.tolist(),
            initial_board.tolist(),
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

        # Call the move method with the 'left' direction
        board_instance.move('left')

        print("Test move passed")



if __name__ == "__main__":
    unittest.main()