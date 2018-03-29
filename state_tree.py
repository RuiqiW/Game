"""
StateTree Class
"""
from typing import Any, Union, List
from game_state import GameState
from stonehenge_state import StonehengeState


class StateTree:
    """
    A Tree ADT to keep track of game states.

    state: current state of a game
    score: highest garanteed score of a state
    children: a list of StateTree with states after possible moves
    """
    state: GameState
    score: Union[int, None]
    children: Union[None, List["StateTree"]]

    def __init__(self, state: GameState, score: Union[int, None] = None,
                 children: Union[None, List["StateTree"]] = None) -> None:
        """
        Initialize a StateTree

        >>> root = StateTree(StonehengeState(True, 1))
        >>> root.score

        >>> root.children

        >>> repr(root.state) == repr(StonehengeState(True, 1))
        True
        """
        self.state = state
        self.score = score
        self.children = children

    def __eq__(self, other: Any) -> bool:
        """
        Check whether two StateTrees are equal

        >>> root1 = StateTree(StonehengeState(True, 1))
        >>> root2 = StateTree(StonehengeState(True, 1))
        >>> root1 == root2
        True
        >>> root2.score = 1
        >>> root1 == root2
        False
        """
        return (type(self) == type(other)
                and repr(self.state) == repr(other.state)
                and self.score == other.score
                and self.children == other.children)

    def __str__(self) -> str:
        """
        String representation of a StateTree
        """
        return str(self.state)


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
