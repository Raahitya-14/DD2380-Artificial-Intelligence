
import random
import sys

from fishing_game_core.game_tree import Node
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR

class PlayerControllerHuman(PlayerController):
    def player_loop(self):
        """
        Function that generates the loop of the game. In each iteration
        the human plays through the keyboard and send
        this to the game through the sender. Then it receives an
        update of the game through receiver, with this it computes the
        next movement.
        :return:
        """

        while True:
            # send message to game that you are ready
            msg = self.receiver()
            if msg["game_over"]:
                return


class PlayerControllerMinimax(PlayerController):

    def __init__(self):
        super(PlayerControllerMinimax, self).__init__()

    def player_loop(self):
        """
        Main loop for the minimax next move search.
        :return:
        """

        # Generate first message (Do not remove this line!)
        first_msg = self.receiver()

        while True:
            msg = self.receiver()

            # Create the root node of the game tree
            node = Node(message=msg, player=0)

            # Possible next moves: "stay", "left", "right", "up", "down"
            best_move = self.search_best_next_move(initial_tree_node=node)

            # Execute next action
            self.sender({"action": best_move, "search_time": None})

    def alphabeta(self, node, depth, alpha, beta, player):
        bigint = 99999999
        children = node.compute_and_get_children()
        if  len(children) == 0 or depth == 0:
            v = self.utility(node.state, player)

        elif player == 0:
            v = -bigint
            for child in children:
                v = max(v, self.alphabeta(child, depth-1, alpha, beta, 1))
                alpha = max(alpha, v)
                if beta <= alpha:
                    break
        else:
            v = bigint
            for child in children:
                v = min(v, self.alphabeta(child, depth-1, alpha, beta, 0))
                beta = min(beta, v)
                if beta <= alpha:
                    break
        return v

    def utility(self, state, player):
        """
        Evaluate the utility of the given state for the specified player.
        :param state: Current game state
        :type state: game_tree.Node
        :param player: Current player (0 for green, 1 for red)
        :type player: int
        :return: Utility value for the state
        :rtype: float
        """
        #get dist to each fish from player
        #if closer to self heavy bias
        #score impacts bias
        playersPos = state.get_hook_positions()

        if player == 0:

            minDist = self.fish_distances(state, 0, playersPos)[0]
            self.eprint(minDist)
            return 10/(minDist+0.0001)

        else:
            minDist = self.fish_distances(state, 1, playersPos)[0]
            self.eprint(minDist)
            return 10/(minDist+0.0001)

    def fish_distances(self, state, player, pos):
        opp = 1
        if player == 1:
            opp = 0

        fishDist = []
        fishPositions = state.get_fish_positions()
        dist = abs(pos[player][1]-10)
        for number, fish in fishPositions.items():
            if fish[0] > pos[opp][0] and pos[opp][0] >= pos[player][0]:
                dist = 20-abs(pos[player][0]-fish[0]) + abs(fish[1]-pos[player][1])
            elif fish[0] < pos[opp][0] and pos[opp][0] < pos[player][0]:
                dist = 20-abs(pos[player][0]-fish[0]) + abs(fish[1]-pos[player][1])
            else:
                dist = abs(fish[0]-pos[player][0])+abs(fish[1]-pos[player][1])

            fishDist.append(dist)

        fishDist.sort()
        return fishDist

    def search_best_next_move(self, initial_tree_node):
        """
        Use minimax (and extensions) to find best possible next move for player 0 (green boat)
        :param initial_tree_node: Initial game tree node
        :type initial_tree_node: game_tree.Node
            (see the Node class in game_tree.py for more information!)
        :return: either "stay", "left", "right", "up" or "down"
        :rtype: str
        """

        # EDIT THIS METHOD TO RETURN BEST NEXT POSSIBLE MODE USING MINIMAX ###

        # NOTE: Don't forget to initialize the children of the current node
        #       with its compute_and_get_children() method!
        depth = 2
        alpha = -99999999
        beta = 99999999

        scoresOfMoves = []
        children = initial_tree_node.compute_and_get_children()
        for child in children:
            childScore = self.alphabeta(child, depth, alpha, beta, 0)
            scoresOfMoves.append(childScore)

        bestMove = children[scoresOfMoves.index(max(scoresOfMoves))].move
        return ACTION_TO_STR[bestMove]

    def eprint(*args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)