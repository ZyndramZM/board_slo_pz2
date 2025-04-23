import pytest

from definitions.board import Pawn


class TestPawn:

    # Creating a Pawn with both WHITE and BLACK colors should set the color property and string representation correctly
    def test_pawn_with_both_colors(self):
        # Arrange
        white_color = Pawn.Color.WHITE
        black_color = Pawn.Color.BLACK

        # Act
        white_pawn = Pawn(white_color)
        black_pawn = Pawn(black_color)

        # Assert
        assert white_pawn.color == Pawn.Color.WHITE
        assert str(white_pawn) == "X"
        assert black_pawn.color == Pawn.Color.BLACK
        assert str(black_pawn) == "O"

    # Attempting to create a Pawn with an invalid color value
    def test_pawn_with_invalid_color(self):
        # Arrange
        invalid_color = "INVALID"

        # Act & Assert
        with pytest.raises(ValueError):
            pawn = Pawn(invalid_color)

    # Checking behavior when comparing two Pawns of the same color
    def test_compare_pawns_of_same_color(self):
        # Arrange
        pawn1 = Pawn(Pawn.Color.WHITE)
        pawn2 = Pawn(Pawn.Color.WHITE)

        # Act & Assert
        assert pawn1.color == pawn2.color
        assert pawn1 is not pawn2


    # Checking behavior when comparing two Pawns of different colors
    def test_compare_pawns_of_different_colors(self):
        # Arrange
        pawn1 = Pawn(Pawn.Color.WHITE)
        pawn2 = Pawn(Pawn.Color.BLACK)

        # Act & Assert
        assert pawn1.color != pawn2.color
        assert pawn1 is not pawn2

