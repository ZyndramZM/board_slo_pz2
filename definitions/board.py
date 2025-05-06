"""
Moduł "board" zawiera definicje wszystkich elementów planszy:

* Pawn - pion
* Field - pole planszy
* Board - zbiór wszystkich pól planszy
"""
from argparse import ArgumentError
from enum import Enum
from typing import Optional, List


class Pawn:
    """
    Pawn - pion. Trzyma informacje o swoim kolorze i dopasowuje do tego swoje wyświetlanie.
    """

    class Color(Enum):
        """
        Enumerator definiujący możliwe kolory piona
        """
        WHITE = "X"
        BLACK = "O"

    def __init__(self, color: Color | str) -> None:
        """
        Tworzy nowego piona  wybranym kolorze

        :param color: Kolor piona
        :type color: Color | str
        """
        if isinstance(color, str):
            color = Pawn.Color(color)
        self.color = color

    def __str__(self):
        """
        :return: Wartość przypisana do koloru danego piona
        """
        return self.color.value


class Field:
    """
    Field - pole przechowuje informacje na temat swojej lokalizacji na planszy oraz ewentualnego
    piona, który może znajdować się na nim
    """

    class FieldAlreadyOccupied(Exception):
        pass

    class DoesNotExist(Exception):
        pass

    def __init__(self, x: int, y: int, pawn: Optional[Pawn] = None) -> None:
        """
        Tworzy nowe pole o współrzędnych x i y. Opcjonalnie może zawierać także piona na polu.

        :param x: Współrzędna x na planszy
        :type x: int
        :param y: Współrzędna y na planszy
        :type y: int
        :param pawn: Pion ustawiony na nowo-tworzonym polu
        :type pawn: Optional[Pawn]
        """
        self.x = x
        self.y = y
        self.pawn = pawn

    def clear_pawn(self) -> None:
        """
        Usuwa piona przypisanego do pola

        :return: None
        """
        self.pawn = None

    def add_pawn(self, pawn: Pawn) -> None:
        """
        Dodaje piona na pole, o ile nie ma na nim już innego piona. W przeciwnym wypadku rzuca błąd
        `FieldAlreadyOccupied`

        :param pawn: Pion do dodania.
        :type pawn: Pawn
        :return: None
        """
        if self.pawn is not None:
            raise self.FieldAlreadyOccupied(f'Na polu [{self.x}, {self.y} znajduje się już pion. '
                                            'Nie można dodać nowego piona do tego pola.')
        self.pawn = pawn

class Move:
    """
    Klasa opisująca pojedynczy ruch. Zawiera informacje skąd dokąd rusza się dany pion oraz
    jaki ma kolor.
    """

    class InvalidMove(Exception):
        """
        Wyjątek rzucany, gdy zostanie wykryty nieprawidłowy ruch.
        """
        pass

    def __init__(self,
                 board: 'Board',
                 color: Pawn.Color,
                 column: int,
                 amount: int,
                 auto_validate: bool = False) -> None:
        """
        Tworzy instancję klasy `Move` - opis pojedynczego ruchu piona na planszy.

        :param board: Plansza, na której toczy się rozgrywka
        :type board: Board:
        :param color: Kolor piona
        :type color: Pawn.Color
        :param column: Kolumna, na której znajduje się ruszany pion
        :type column: int
        :param amount: Liczba pól, o którą przesuwa się piona
        :type amount: int
        :param auto_validate: Opcja, która sprawia, że ruch jest walidowany bezpośrednio po utworzeniu
        :type auto_validate: bool

        :raise AttributeError: Błąd rzucany, gdy podano nieprawidłowy kolor piona
        :raise InvalidMove: Błąd rzucany, gdy walidacja ruch zakończy się porażką
        """
        if color not in Pawn.Color:
            raise AttributeError(f"Atrybut `color` nie może mieć wartości {color}. "
                                 "Jedyne możliwe wartości tego atrybutu to BLACK i WHITE")
        if not (0 <= column < board.n):
            raise self.InvalidMove(f"Podana kolumna: {column} nie istnieje. "
                                   f"Kolumna musi być w przedziale od 0 do {board.n-1}")

        self.board = board
        self.color = color
        self.column = column
        self.from_field = self._find_from_field()
        self.to_field = self._calculate_to_field(amount)

        if auto_validate:
            self.validate()

    def __str__(self) -> str:
        return (f'Ruch {self.color.name}: kolumna [{self.column}] '
                f'pola [{self.from_field} -> {self.to_field}]')

    def _find_from_field(self) -> int:
        """
        Szuka miejsca w danej kolumnie, na której znajduje się pion danego koloru.

        :return: Indeks pola, na którym znajduje się pion koloru `self.color` w kolumnie
            `self.column`
        :type: int

        :raise AttributeError: Błąd jest rzucany, gdy podany zostanie nieprawidłowy kolor lub gdy
            plansza nie jest poprawnie zainicjalizowana
        """
        move_column = self.board.fields[self.column]
        if self.color == Pawn.Color.WHITE:
            for i in range(self.board.m):
                pawn = move_column[i].pawn
                if pawn is not None and pawn.color == Pawn.Color.WHITE:
                    return i
        elif self.color == Pawn.Color.BLACK:
            for i in range(self.board.m-1, 0, -1):
                pawn = move_column[i].pawn
                if pawn is not None and pawn.color == Pawn.Color.BLACK:
                    return i

        raise AttributeError('Plansza nie została poprawnie zainicjalizowana. Nie znaleziono piona'
                             f'w kolorze {self.color.name} na kolumnie {self.column}')

    def _calculate_to_field(self, amount: int) -> int:
        """
        Oblicza pole, na które ruszy się pion, podróżując o wartość `amount`

        :param amount: Liczba pól, o które ma się ruszyć pion
        :type amount: int
        :return: Pole docelowe ruchu
        """
        if self.color == Pawn.Color.WHITE:
            return self.from_field + amount
        if self.color == Pawn.Color.BLACK:
            return self.from_field - amount
        raise ValueError("Błędnie zdefiniowany kolor piona.")



    def validate(self) -> None:
        """
        Sprawdza, czy ten ruch jest poprawny. Jeśli ruch nie jest poprawny rzuca wyjątek.

        :return: None

        :raise InvalidMove: Błąd rzucany, gdy ruch nie jest poprawny
        """
        shift = 1 if self.color == Pawn.Color.WHITE else -1
        try:
            self.board.get(self.column, self.from_field)
            self.board.get(self.column, self.to_field)
        except Field.DoesNotExist as e:
            raise self.InvalidMove(f"'{self}' wychodzi poza granice planszy.") from e

        if self.board.get(self.column, self.from_field).pawn.color != self.color:
            raise self.InvalidMove(f"'{self}' nie jest możliwy. Na polu początkowym "
                                   f"{self.from_field} nie ma piona w kolorze {self.color}")

        for i in range(min(self.from_field + shift, self.to_field),
                       max(self.from_field + shift, self.to_field) + shift,
                       shift):
            if self.board.get(self.column, i).pawn is not None:
                raise self.InvalidMove(f"'{self}' nie jest możliwy. Na trasie ruchu znajduje się inny pion.")


class Board:
    """
    Board - plansza; przechowuje informacje na temat planszy: wszystkich pól oraz pionów oraz ich
    lokalizacji

    Na planszy obowiązuje układ współrzędnych (x, y), gdzie:

    * `x` - oznacza kolumnę
    * `y` - oznacza wiersz

    obie wartości zaczynają się od 0 i kończą odpowiednio na n-1 i m-1.
    """

    def __init__(self,
                 n: int,
                 m: int,
                 with_pawns: bool = True) -> None:
        """
        Tworzy nową planszę o wymiarach n x m. Argument `with_pawns` pozwala na automatyczne
        wypełnienie planszy pionami na początkowym i końcowym wierszu.

        :param n: Liczba kolumn
        :type n: int
        :param m: Liczba wierszy
        :type m: int
        :param with_pawns: Automatyczne wypełnianie planszy pionami
        :type with_pawns: bool
        """
        if n <= 0 or m <= 0:
            raise ValueError(f"Nie można utworzyć planszy o wymiarach {n} x {m}. Liczby kolumn i wierszy muszą być dodatnie.")
        self.n = n
        self.m = m
        self.fields = []
        self.moves = []

        for i in range(self.n):
            column = [Field(i, j) for j in range(self.m)]
            self.fields.append(column)

        if with_pawns:
            self.place_default_pawns()

    @staticmethod
    def column_number(column: str | int) -> int:
        """
        Zwraca numer kolumny niezależnie, zamieniając literę na liczbę, jeśli jest to potrzebne

        :param column: Litera lub liczba oznaczająca kolumnę
        :type column: str | int

        :return: Numer kolumny
        :type: int

        :raise Field.DoesNotExist: Gdy litera kolumny ie jest poprawna
        """
        if isinstance(column, str):
            if len(column) != 1 and not column.isalpha():
                raise Field.DoesNotExist(f"Kolumna '{column}' nie jest poprawną nazwą kolumny.")
            column = ord(column.lower()) - ord('a')
        return column

    def print(self) -> None:
        """
        Wypisuje uproszczony wygląd planszy
        """
        print("   " + "".join([chr(i+ord('A')) for i in range(self.n)]))
        for j in range(self.m):
            row = str(j)
            if j < 10:
                row += " "
            row += " "
            for i in range(self.n):
                field = self.fields[i][j]
                if field.pawn is None:
                    row += '.'
                elif field.pawn.color == Pawn.Color.BLACK:
                    row += 'B'
                else:
                    row += 'W'
            print(row)

    def get(self, column: str | int, row: int) -> Field:
        """
        Zwraca pole planszy zadane przez numer / literę kolumny i numer wiersza

        :param column: Numer lub litera wiersza
        :type column: str | int
        :param row: Numer wiersza
        :type row: int

        :return: Pole planszy o współrzędnych zadanych argumentami
        :type: Field
        """
        column = self.column_number(column)

        if any((
            column < 0,
            column >= self.n,
            row < 0,
            row >= self.m,
        )):
            raise Field.DoesNotExist(f'Pole [{column}, {row}] nie istnieje.')

        return self.fields[column][row]

    def place_default_pawns(self, clear_board: bool = True) -> None:
        """
        Ustawia piony na domyślnych pozycjach. Odpowiednio:

        * piony białe umieszcza na indeksie 0
        * piony czarne umieszcza na indeksie `self.m - 1`

        :param clear_board: jeśli True, zanim ustawi piony na pozycjach startowych, funkcja najpierw
            usunie wszystkie piony znajdujące się na planszy
        :return: None
        """
        if clear_board:
            self.clear_all_pawns()

        for i in range(self.n):
            self.fields[i][0].add_pawn(Pawn(Pawn.Color.WHITE))

        for i in range(self.n):
            self.fields[i][self.m - 1].add_pawn(Pawn(Pawn.Color.BLACK))

    def clear_all_pawns(self) -> None:
        """
        Usuwa wszystkie piony z planszy

        :return: None
        """
        for column in self.fields:
            for field in column:
                field.clear_pawn()

    def get_move(self, color: Pawn.Color, column: int | str, amount: int) -> Move:
        """
        Zwraca obiekt obrazujący ruch piona na podstawie koloru, kolumny i liczby pól

        :param color: Kolor piona, który ma być ruszony
        :type color: Pawn.Color
        :param column: Kolumna, na której ma być wykonany ruch
        :type column: int | str
        :param amount: Liczba pól, o ktorą ma być wykonany ruch
        :type amount: int

        :return: Obiekt ruchu
        :type: Move
        """
        return Move(self, color, column, amount)

    @staticmethod
    def is_move_legal(move: Move) -> bool:
        """
        Sprawdza, czy ruch jest legalny.

        :return: `True` jeśli ruch jest dozwolony, `False` w przeciwnym przypadku
        :type: bool
        """
        try:
            move.validate()
            return True
        except Move.InvalidMove:
            return False

    def move_pawn(self, move: Move) -> None:
        """
        Wykonuje ruch, jeśli jest on dozwolony

        :param move: Ruch do wykonania
        :type move: Move

        :return: None

        :raise Move.InvalidMove: if validation fails
        """
        move.validate()

        pawn = self.get(move.column, move.from_field).pawn
        if pawn is None:
            raise Move.InvalidMove(f'Na polu [{move.column}, {move.from_field}] nie ma piona.')
        self.get(move.column, move.from_field).clear_pawn()
        self.get(move.column, move.to_field).add_pawn(pawn)
        self.moves.append(move)

