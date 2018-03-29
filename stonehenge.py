"""
An implementation of Stonehenge.
"""

from game import Game
from stonehenge_state import StonehengeState


class StonehengeGame(Game):
    """
    Abstract class for a game to be played with two players.
    """

    def __init__(self, p1_starts: bool) -> None:
        """
        Initialize this Game, using p1_starts to find who the first player is.
        Precondition: side length <= 5

        """
        side_length = int(input("Enter the side length of the board: "))
        self.current_state = StonehengeState(p1_starts, side_length)

    def get_instructions(self) -> str:
        """
        Return the instructions for this Game.
        """
        instructions = """Players take turns claiming cells. 
        When a player captures at least half of the cells in a ley-line,
        then the player captures that ley-line. The 1st player 
        to capture at least half of the ley-lines is the winner.
        """
        return instructions

    def is_over(self, state: StonehengeState)-> bool:
        """
        Return whether or not this game is over.
        """
        return state.state_over()

    def is_winner(self, player: str)-> bool:
        """
        Return whether player has won the game.
        Precondition: player is 'p1' or 'p2'.
        """
        count1 = 0
        count2 = 0
        total = 0
        for ley in self.current_state.ley_lines:
            if ley == '1':
                count1 += 1
            elif ley == '2':
                count2 += 1
            total += 1
        if player == 'p1':
            return self.is_over(self.current_state) and 2 * count1 >= total
        elif player == 'p2':
            return self.is_over(self.current_state) and 2 * count2 >= total
        return False

    def str_to_move(self, string: str)-> str:
        """
        Return the move that string represents. If string is not a move,
        return an invalid move.
        """
        if not string.strip().isalpha():
            return 'a'
        return string.strip()


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
