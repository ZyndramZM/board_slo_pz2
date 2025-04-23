import pytest

from definitions.board import *

class TestBoard:

    # Creating a board with default dimensions and pawns
    def test_create_board_with_default_pawns(self):
        # Arrange & Act
        board = Board(5, 5)

        # Assert
        assert board.n == 5
        assert board.m == 5
        # Check white pawns on first row
        for i in range(board.n):
            assert board.fields[i][0].pawn is not None
            assert board.fields[i][0].pawn.color == Pawn.Color.WHITE
        # Check black pawns on last row
        for i in range(board.n):
            assert board.fields[i][board.m - 1].pawn is not None
            assert board.fields[i][board.m - 1].pawn.color == Pawn.Color.BLACK

    # Creating a board without pawns
    def test_create_board_without_pawns(self):
        # Arrange & Act
        board = Board(3, 4, with_pawns=False)

        # Assert
        assert board.n == 3
        assert board.m == 4
        # Check that no fields have pawns
        for column in board.fields:
            for field in column:
                assert field.pawn is None

    # Getting a field by column number and row
    def test_get_field_by_column_number_and_row(self):
        # Arrange
        board = Board(4, 4, with_pawns=False)

        # Act
        field = board.get(2, 3)

        # Assert
        assert field.x == 2
        assert field.y == 3
        assert field is board.fields[2][3]

    # Getting a field by column letter and row
    def test_get_field_by_column_letter_and_row(self):
        # Arrange
        board = Board(4, 4, with_pawns=False)

        # Act
        field_c = board.get('c', 2)
        field_A = board.get('A', 1)

        # Assert
        # 'c' should be column 2 (0-indexed)
        assert field_c.x == 2
        assert field_c.y == 2
        assert field_c is board.fields[2][2]

        # 'A' should be column 0 (0-indexed)
        assert field_A.x == 0
        assert field_A.y == 1
        assert field_A is board.fields[0][1]

    # Creating a board with zero dimensions should raise a ValueError
    def test_create_board_with_zero_dimensions_raises_value_error(self):
        with pytest.raises(ValueError):
            Board(0, 0)

    # Attempting to get a field outside board boundaries
    def test_get_field_outside_boundaries(self):
        # Arrange
        board = Board(3, 3)

        # Act & Assert
        # Test negative indices
        with pytest.raises(Field.DoesNotExist):
            board.get(-1, 0)

        with pytest.raises(Field.DoesNotExist):
            board.get(0, -1)

        # Test indices beyond board size
        with pytest.raises(Field.DoesNotExist):
            board.get(3, 0)

        with pytest.raises(Field.DoesNotExist):
            board.get(0, 3)

        # Test invalid column letter
        with pytest.raises(Field.DoesNotExist):
            board.get('d', 0)  # 'd' corresponds to index 3, which is out of bounds

    def test_add_pawns_on_specific_positions(self):
        board = Board(3, 5, with_pawns=False)

        # Add pawns to specific positions
        board.get(1, 1).add_pawn(Pawn(Pawn.Color.WHITE))
        board.get(1, 3).add_pawn(Pawn(Pawn.Color.BLACK))

        # Assert
        assert board.fields[1][1].pawn is not None
        assert board.fields[1][1].pawn.color == Pawn.Color.WHITE
        assert board.fields[1][3].pawn is not None
        assert board.fields[1][3].pawn.color == Pawn.Color.BLACK

        assert board.get(1, 1).pawn is not None
        assert board.get(1, 1).pawn.color == Pawn.Color.WHITE

    # Attempting to move a pawn to an occupied field
    def test_move_pawn_to_occupied_field(self):
        # Arrange
        board = Board(3, 5, with_pawns=False)

        # Add pawns to specific positions
        board.get(1, 1).add_pawn(Pawn(Pawn.Color.WHITE))
        board.get(1, 3).add_pawn(Pawn(Pawn.Color.BLACK))

        # Act
        move = board.get_move(Pawn.Color.WHITE, 1, 2)  # Try to move white pawn 2 spaces up

        # Assert
        assert not board.is_move_legal(move)
        with pytest.raises(Move.InvalidMove):
            board.move_pawn(move)

    # Attempting to move a pawn outside board boundaries
    def test_move_pawn_outside_boundaries(self):
        # Arrange
        board = Board(3, 4)

        # Act & Assert
        # Try to move white pawn too far (beyond board boundary)
        move_white = board.get_move(Pawn.Color.WHITE, 1, 4)  # Move 4 spaces from row 0
        assert not board.is_move_legal(move_white)
        with pytest.raises(Move.InvalidMove):
            board.move_pawn(move_white)

        # Try to move black pawn too far (beyond board boundary)
        move_black = board.get_move(Pawn.Color.BLACK, 1, 4)  # Move 4 spaces from row 3
        assert not board.is_move_legal(move_black)
        with pytest.raises(Move.InvalidMove):
            board.move_pawn(move_black)