import pytest
from definitions.board import Pawn, Field

class TestField:

    # Creating a Field with valid x, y coordinates and no pawn
    def test_create_field_with_valid_coordinates_no_pawn(self):
        field = Field(3, 4)
        assert field.x == 3
        assert field.y == 4
        assert field.pawn is None

    # Creating a Field with valid x, y coordinates and a pawn
    def test_create_field_with_valid_coordinates_and_pawn(self):
        pawn = Pawn(Pawn.Color.WHITE)
        field = Field(1, 2, pawn)
        assert field.x == 1
        assert field.y == 2
        assert field.pawn == pawn
        assert str(field.pawn) == "X"

    # Adding a pawn to an empty field
    def test_add_pawn_to_empty_field(self):
        field = Field(5, 5)
        pawn = Pawn(Pawn.Color.BLACK)
        field.add_pawn(pawn)
        assert field.pawn == pawn
        assert str(field.pawn) == "O"

    # Clearing a pawn from a field that has a pawn
    def test_clear_pawn_from_field(self):
        pawn = Pawn(Pawn.Color.WHITE)
        field = Field(0, 0, pawn)
        assert field.pawn is not None
        field.clear_pawn()
        assert field.pawn is None

    # Attempting to add a pawn to a field that already has a pawn
    def test_add_pawn_to_occupied_field(self):
        field = Field(3, 3, Pawn(Pawn.Color.WHITE))
        new_pawn = Pawn(Pawn.Color.BLACK)
        with pytest.raises(Field.FieldAlreadyOccupied):
            field.add_pawn(new_pawn)
        assert str(field.pawn) == "X"  # Original pawn should remain

    # Creating a Field with negative coordinates
    def test_create_field_with_negative_coordinates(self):
        field = Field(-1, -5)
        assert field.x == -1
        assert field.y == -5
        assert field.pawn is None

    # Creating a Field with very large coordinate values
    def test_create_field_with_large_coordinates(self):
        large_x = 10**6
        large_y = 10**6
        field = Field(large_x, large_y)
        assert field.x == large_x
        assert field.y == large_y

    # Adding a pawn with an invalid color
    def test_add_pawn_with_invalid_color(self):
        field = Field(7, 7)
        with pytest.raises(ValueError):
            invalid_pawn = Pawn("INVALID_COLOR")
            field.add_pawn(invalid_pawn)