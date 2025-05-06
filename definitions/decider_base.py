from definitions.board import Board, Pawn
from abc import ABC, abstractmethod

class DeciderBase(ABC):
    """
    Klasa bazowa dla programów decyzyjnych. Nie zawiera implementacji poszczególnych metod,
    a jedynie definiuje jakie działania powinna umieć wykonywać klasa z algorytmem decyzyjnym.
    """
    def __init__(self, board: Board, color: Pawn.Color) -> None:
        self.board = board
        self.color = color

    @abstractmethod
    def move(self) -> None:
        """
        Wykonuje ruch na aktualnym stanie `move_pawn` na `self.board`. Metoda powinna samodzielnie
        zdecydować jaki ruch należy wykonać. Może przy tym korzystać ze wszystkich danych board, ale
        nie może wprowadzać żadnych zmian. Metoda nie zwraca wyniku.

        :return: None
        """
        raise NotImplemented("Wykonano metodę abstrakcyjną.")