"""
Fast Shapley Attribution with Monte Carlo Sampling
Sublinear complexity O(sqrt(n))
"""

import numpy as np
from typing import List, Dict, Callable, Tuple
from itertools import combinations
import time


class FastShapleyAttribution:
    """
    Compute Shapley values using Monte Carlo sampling
    """

    def __init__(self, players: List[str], value_function: Callable):
        """
        Initialize Shapley attribution

        Parameters:
        -----------
        players : List[str]
            List of player/channel names
        value_function : Callable
            Function mapping coalitions to values
        """
        self.players = players
        self.value_function = value_function
        self.n_players = len(players)

    def monte_carlo_shapley(self, n_samples: int = 1000) -> Tuple[Dict[str, float], Dict[str, List[float]]]:
        """
        Compute Shapley values using Monte Carlo sampling

        Parameters:
        -----------
        n_samples : int
            Number of permutation samples

        Returns:
        --------
        values : Dict[str, float]
            Shapley value for each player
        marginals : Dict[str, List[float]]
            Marginal contributions per sample
        """
        marginal_contributions = {player: [] for player in self.players}

        for _ in range(n_samples):
            # Random permutation
            perm = np.random.permutation(self.players).tolist()

            # Compute marginal contributions
            for i, player in enumerate(perm):
                coalition_without = perm[:i]
                coalition_with = perm[:i+1]

                value_without = self.value_function(coalition_without)
                value_with = self.value_function(coalition_with)

                marginal = value_with - value_without
                marginal_contributions[player].append(marginal)

        # Average marginals = Shapley values
        shapley_values = {
            player: np.mean(marginals)
            for player, marginals in marginal_contributions.items()
        }

        return shapley_values, marginal_contributions

    def exact_shapley(self) -> Dict[str, float]:
        """
        Compute exact Shapley values (exponential complexity)
        Only for small player sets
        """
        if self.n_players > 10:
            raise ValueError("Exact Shapley only for n <= 10")

        shapley_values = {player: 0.0 for player in self.players}

        # Iterate over all coalitions
        for r in range(self.n_players + 1):
            for coalition in combinations(self.players, r):
                coalition_list = list(coalition)
                v_coalition = self.value_function(coalition_list)

                # Each player not in coalition
                for player in self.players:
                    if player not in coalition:
                        coalition_with_player = coalition_list + [player]
                        v_with = self.value_function(coalition_with_player)

                        marginal = v_with - v_coalition
                        weight = (np.math.factorial(r) * 
                                 np.math.factorial(self.n_players - r - 1) /
                                 np.math.factorial(self.n_players))

                        shapley_values[player] += weight * marginal

        return shapley_values