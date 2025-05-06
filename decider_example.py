"""
Przykładowy program decyzyjny. Stworzenie podobnego programu jest jednym z celi PZ2.
"""
from random import choice
from typing import List

from definitions.board import Move
from definitions.decider_base import DeciderBase

class DeciderExample(DeciderBase):
    def list_possible_moves(self) -> List[Move]:
        """
        :return: Lista wszystkich dozwolonych ruchów
        :type: List[Move]
        """
        possible_moves = []
        for i, col in enumerate(self.board.fields):
            my_pawn = None
            enemy_pawn = None
            for j, field in enumerate(col):
                if field.pawn is None:
                    continue
                if field.pawn.color == self.color:
                    my_pawn = j
                else:
                    enemy_pawn = j
            if my_pawn is None or enemy_pawn is None:
                raise AttributeError("Plansza wygląda na błędnie zdefiniowaną - nie umiem znaleźć "
                                     "piona mojego lub przeciwnika.")
            distance = abs(my_pawn - enemy_pawn)
            for step in range(1, distance):
                new_move = Move(self.board, self.color, i, step)
                try:
                    new_move.validate()
                    possible_moves.append(new_move)
                except Move.InvalidMove:
                    pass
        return possible_moves

    def move(self) -> None:
        """
        Tworzy listę możliwych ruchów, a następnie wybiera i wykonuje losowy z nich.
        """
        possible_moves = self.list_possible_moves()
        move = choice(possible_moves)
        self.board.move_pawn(move)