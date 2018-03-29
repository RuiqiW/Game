"""
A module for strategies.

NOTE: Make sure this file adheres to python-ta.
Adjust the type annotations as needed, and implement both a recursive
and an iterative version of minimax.
"""
from typing import Any
from state_tree import StateTree

# TODO: Adjust the type annotation as needed.


def interactive_strategy(game: Any) -> Any:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)


def rough_outcome_strategy(game: Any) -> Any:
    """
    Return a move for game by picking a move which results in a state with
    the lowest rough_outcome() for the opponent.

    NOTE: game.rough_outcome() should do the following:
        - For a state that's over, it returns the score for the current
          player of that state.
        - For a state that's not over:
            - If there is a move that results in the current player winning,
              return 1.
            - If all moves result in states where the other player can
              immediately win, return -1.
            - Otherwise; return a number between -1 and 1 corresponding to how
              'likely' the current player will win from the current state.

        In essence: rough_outcome() will only look 1 or 2 states ahead to
        'guess' the outcome of the game, but no further. It's better than
        random, but worse than minimax.
    """
    current_state = game.current_state
    best_move = None
    best_outcome = -2  # Temporarily -- just so we can replace this easily later

    # Get the move that results in the lowest rough_outcome for the opponent
    for move in current_state.get_possible_moves():
        new_state = current_state.make_move(move)

        # We multiply the below by -1 since a state that's bad for the opponent
        # is good for us.
        guessed_score = new_state.rough_outcome() * -1
        if guessed_score > best_outcome:
            best_outcome = guessed_score
            best_move = move

    # Return the move that resulted in the best rough_outcome
    return best_move

# TODO: Implement a recursive version of the minimax strategy.


def minimax_recursive_strategy(game: Any) -> Any:
    """
    Obtain a move using recursion
    """
    current_state = game.current_state
    possible_moves = current_state.get_possible_moves()
    tie_move = []
    for move in possible_moves:
        new_state = current_state.make_move(move)
        score = recursive_score(game, new_state)
        if score == 1:
            return move
        elif score == 0:
            tie_move.append(move)
    if tie_move != []:
        return tie_move[0]
    return possible_moves[0]


def recursive_score(game: Any, state: Any) -> int:
    """
    Get the final score for a move.
    """
    if game.is_over(state):
        return score_state_over(game, state)
    new_states = []
    for move in state.get_possible_moves():
        new_states.append(state.make_move(move))
    return (-1) * max([recursive_score(game, new_state)
                       for new_state in new_states])

# TODO: Implement an iterative version of the minimax strategy.


def minimax_iterative_strategy(game: Any) -> Any:
    """
    Obtain a move using iteration
    """
    current_state = game.current_state
    possible_moves = current_state.get_possible_moves()
    tie_move = []
    for move in possible_moves:
        new_state = current_state.make_move(move)
        score = iterative_score(game, new_state)
        if score == 1:
            return move
        elif score == 0:
            tie_move.append(move)
    if tie_move != []:
        return tie_move[0]
    return possible_moves[0]


def iterative_score(game: Any, state: Any) -> int:
    """
    Get the final score for a move.
    """
    new_states = []
    root = StateTree(state)
    new_states.append(root)
    while new_states != []:
        mother = new_states.pop()
        # state is over
        if game.is_over(mother.state):
            mother.score = score_state_over(game, mother.state)
        # state is not over but have children already
        elif mother.children is not None:
            mother.score = (-1) * max([child.score
                                       for child in mother.children])
        # don't have children
        else:
            mother.children = []
            for move in mother.state.get_possible_moves():
                mother.children.append(StateTree(mother.state.make_move(move)))
            new_states.append(mother)
            for child in mother.children:
                new_states.append(child)
    return root.score


def score_state_over(game: Any, state: Any) -> int:
    """
    Get the score of a state.
    Precondition: game.is_over(state)
    """
    current_state = game.current_state
    game.current_state = state
    if state.get_current_player_name() == 'p1':
        cur, other = 'p1', 'p2'
    else:
        cur, other = 'p2', 'p1'
    if game.is_winner(cur):
        game.current_state = current_state
        return -1
    elif game.is_winner(other):
        game.current_state = current_state
        return 1
    game.current_state = current_state
    return 0


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
