"""
An implementation of a state for Stonehenge.

"""
from typing import List, Dict, Tuple
from game_state import GameState
from draw import draw_hexagon


class StonehengeState(GameState):
    """
    The state of a game at a certain point in time.
    """
    CELL = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self, is_p1_turn: bool, side_length: int) -> None:
        """
        Initialize this game state and set the current player based on
        is_p1_turn.
        >>> stone = StonehengeState(True, 3)
        >>> stone.side_length
        3
        >>> stone.ley_lines
        ['@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@']
        >>> stone.cells
        ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
        >>> stone = StonehengeState(True, 1)
        >>> stone.claims
        {0: [2, 0, 0], 2: [2, 0, 0], 4: [2, 0, 0], 1: [1, 0, 0], 3: [1, 0, 0], 5: [1, 0, 0]}
        """
        super().__init__(is_p1_turn)
        self.side_length = side_length
        self.ley_lines = ['@'] * (self.side_length + 1) * 3
        self.cells = []
        self.claims = self._claim_ley_line()
        total_cell = self.side_length * (self.side_length + 5) // 2
        for i in range(total_cell):
            self.cells.append(self.CELL[i])

    def _claim_ley_line(self) -> Dict:
        """
        Initialize a dictionary recording the number of '1' and '2'
        in each ley line. Doctest is in init method.
        """
        claims = {}
        for i in range(self.side_length):
            claims[i] = [i + 2, 0, 0]
            claims[i + self.side_length + 1] = [i + 2, 0, 0]
            claims[i + (self.side_length + 1) * 2] = [i + 2, 0, 0]
        claims[self.side_length] = [self.side_length, 0, 0]
        claims[self.side_length * 2 + 1] = [self.side_length, 0, 0]
        claims[self.side_length * 3 + 2] = [self.side_length, 0, 0]
        return claims

    def __str__(self) -> str:
        """
        Return a string representation of the current state of the game.
        """
        return draw_hexagon(self.side_length, self.cells, self.ley_lines)

    def get_possible_moves(self) -> list:
        """
        Return all possible moves that can be applied to this state.

        >>> stone = StonehengeState(True, 1)
        >>> stone.get_possible_moves()
        ['A', 'B', 'C']
        >>> new_state = stone.make_move('A')
        >>> new_state.get_possible_moves()
        []
        """
        moves = []
        if not self.state_over():
            for i in self.cells:
                if i.isalpha():
                    moves.append(i)
        return moves

    def make_move(self, move: str) -> "StonehengeState":
        """
        Return the GameState that results from applying move to this GameState.
        >>> stone = StonehengeState(True, 2)
        >>> state = stone.make_move('A')
        >>> state.cells
        ['1', 'B', 'C', 'D', 'E', 'F', 'G']
        >>> state.ley_lines
        ['1', '@', '@', '@', '@', '@', '@', '@', '1']
        """
        new_state = StonehengeState(not self.p1_turn, self.side_length)
        new_state.cells = self.change_cell(move)
        new_state.claims, new_state.ley_lines = self.change_claims(move)
        return new_state

    def __repr__(self) -> str:
        """
        Return a representation of this state (which can be used for
        equality testing).
        >>> stone = StonehengeState(True, 1)
        >>> info = "P1's Turn: True, Side Length: 1 \\n"
        >>> repr(stone) ==  info + str(stone)
        True
        """
        return "P1's Turn: {}, Side Length: {} \n".format(self.p1_turn,
                                                          self.side_length) \
               + self.__str__()

    def change_cell(self, move: str) -> List[str]:
        """
        Change the cell according to move.
        >>> stone = StonehengeState(True, 2)
        >>> stone.change_cell('A')
        ['1', 'B', 'C', 'D', 'E', 'F', 'G']
        >>> stone.change_cell('B')
        ['A', '1', 'C', 'D', 'E', 'F', 'G']
        """
        cells = self.cells[:]
        for i in range(len(cells)):
            if cells[i] == move:
                cells[i] = '1' if self.get_current_player_name() == 'p1' \
                    else '2'
        return cells

    def get_position(self, move: str) -> Tuple:
        """
        Find the position of a move
        >>> stone = StonehengeState(True, 2)
        >>> stone.get_position('F')
        (2, 7, 3)
        >>> stone = StonehengeState(True, 3)
        >>> stone.get_position('K')
        (3, 9, 5)
        """
        index = self.cells.index(move)
        row = 0
        i = 2
        while index - i >= 0 and i <= self.side_length + 1:
            index = index - i
            i += 1
            row += 1
        if row == self.side_length:
            index += 1
        down_left = (self.side_length + 1) * 3 - index - 1
        down_right = (self.side_length + 1) * 2 - 1 - (row + 1 - index)
        return (row, down_left, down_right)

    def change_claims(self, move: str) -> (Dict, List):
        """
        Change claims according to move.
        >>> stone = StonehengeState(True, 2)
        >>> stone.change_claims('A')
        ({0: [2, 1, 0], 3: [2, 0, 0], 6: [2, 0, 0], 1: [3, 0, 0], 4: [3, 1, 0], 7: [3, 0, 0], 2: [2, 0, 0], 5: [2, 0, 0], 8: [2, 1, 0]}, ['1', '@', '@', '@', '@', '@', '@', '@', '1'])
        >>> stone.change_claims('B')
        ({0: [2, 1, 0], 3: [2, 0, 0], 6: [2, 0, 0], 1: [3, 0, 0], 4: [3, 0, 0], 7: [3, 1, 0], 2: [2, 0, 0], 5: [2, 1, 0], 8: [2, 0, 0]}, ['1', '@', '@', '@', '@', '1', '@', '@', '@'])
        """
        claim = {}
        for c in self.claims:
            claim[c] = self.claims[c][:]
        ley_line = self.ley_lines[:]
        for pos in self.get_position(move):
            self.change_claim(pos, claim, ley_line)
        return claim, ley_line

    def change_claim(self, position: int, claims: Dict, ley_lines: List) \
            -> None:
        """
        Change claim according to the No. of ley line
        """
        if self.get_current_player_name() == 'p1':
            claims[position][1] += 1
            if ley_lines[position] == '@' and \
                    2 * claims[position][1] >= claims[position][0]:
                ley_lines[position] = '1'
        elif self.get_current_player_name() == 'p2':
            claims[position][2] += 1
            if ley_lines[position] == '@' and \
                    2 * claims[position][2] >= claims[position][0]:
                ley_lines[position] = '2'

    def count(self, player: str) -> int:
        """
        Count the number of ley lines claimed by player.
        >>> stone = StonehengeState(True, 2)
        >>> stone1 = stone.make_move('A')
        >>> stone = stone1.make_move('B')
        >>> stone1 = stone.make_move('G')
        >>> stone1.count('p1')
        5
        >>> stone1.count('p2')
        1
        """
        if player == 'p1':
            return sum([1 if ley == '1' else 0 for ley in self.ley_lines])
        return sum([1 if ley == '2' else 0 for ley in self.ley_lines])

    def state_over(self)-> bool:
        """
        Return whether or not this game is over.
        >>> stone = StonehengeState(True, 1)
        >>> new_state = stone.make_move('A')
        >>> new_state.state_over()
        True
        """
        total = (self.side_length + 1) * 3
        return 2 * self.count('p1') >= total or 2 * self.count('p2') >= total

    def rough_outcome(self) -> float:
        """
        Return an estimate in interval [LOSE, WIN] of best outcome the current
        player can guarantee from state self.

        >>> stone = StonehengeState(True, 1)
        >>> stone.rough_outcome()
        1
        >>> stone1 = StonehengeState(True, 2)
        >>> stone2 = stone1.make_move('A')
        >>> stone2.rough_outcome()
        0
        >>> stone1 = stone2.make_move('E')
        >>> stone1.rough_outcome()
        0
        >>> stone2 = stone1.make_move('F')
        >>> stone2.rough_outcome()
        -1
        """
        total = (self.side_length + 1) * 3
        # state is over, get current score of current player
        if self.state_over():
            if self.get_current_player_name() == 'p1':
                cur, other = 'p1', 'p2'
            else:
                cur, other = 'p2', 'p1'
            if 2 * self.count(cur) >= total:
                if 2 * self.count(other) < total:
                    return self.WIN
            else:
                return self.LOSE
        # state not over
        else:
            if self.win_in_one() == 1:
                return self.WIN
            else:
                new_states = []
                for move in self.get_possible_moves():
                    new_states.append(self.make_move(move))
                if all([new_state.win_in_one() == 1
                        for new_state in new_states]):
                    return self.LOSE
        return self.DRAW

    def win_in_one(self) -> int:
        """
        Return whether the current player of a state that is not over
        can win immediately.
        >>> stone = StonehengeState(True, 1)
        >>> stone.win_in_one()
        1
        >>> new_stone = stone.make_move('A')
        >>> new_stone.win_in_one()
        0
        >>> stone = StonehengeState(True, 2)
        >>> stone.win_in_one()
        0
        """
        if not self.state_over():
            for move in self.get_possible_moves():
                new_state = self.make_move(move)
                if new_state.state_over():
                    return 1
        return 0


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
