"""
Hybrid Shapley-Markov Attribution
Novel combination of game theory and Markov chains
"""

import numpy as np
from typing import List, Dict
from .shapley import FastShapleyAttribution
from .markov import MarkovAttribution


class HybridShapleyMarkov:
    """
    Hybrid method combining Shapley values and Markov chains
    """

    def __init__(self, journeys: List[List[str]], conversions: List[int]):
        """
        Initialize hybrid attribution

        Parameters:
        -----------
        journeys : List[List[str]]
            Customer journey sequences
        conversions : List[int]
            Binary conversion outcomes
        """
        self.journeys = journeys
        self.conversions = conversions
        self.channels = self._extract_channels()

    def _extract_channels(self) -> List[str]:
        """Extract unique channels"""
        channels = set()
        for journey in self.journeys:
            channels.update(journey)
        return sorted(list(channels))

    def _create_value_function(self) -> callable:
        """
        Create value function for Shapley based on journey data
        """
        def value_function(coalition: List[str]) -> float:
            """Value = conversion rate for journeys using only coalition channels"""
            if not coalition:
                return 0.0

            relevant_journeys = []
            relevant_conversions = []

            for journey, converted in zip(self.journeys, self.conversions):
                # Check if journey uses only coalition channels
                if all(ch in coalition for ch in journey):
                    relevant_journeys.append(journey)
                    relevant_conversions.append(converted)

            if not relevant_conversions:
                return 0.0

            return np.mean(relevant_conversions)

        return value_function

    def compute_shapley_component(self) -> Dict[str, float]:
        """Compute Shapley component"""
        value_func = self._create_value_function()
        shapley = FastShapleyAttribution(self.channels, value_func)
        shapley_values, _ = shapley.monte_carlo_shapley(n_samples=1000)

        # Normalize
        total = sum(shapley_values.values())
        if total > 0:
            shapley_values = {ch: v / total for ch, v in shapley_values.items()}

        return shapley_values

    def compute_markov_component(self) -> Dict[str, float]:
        """Compute Markov component"""
        markov = MarkovAttribution(self.journeys, self.conversions)
        markov_values = markov.compute_removal_effects()
        return markov_values

    def compute_hybrid_attribution(self, alpha: float = 0.5) -> Dict[str, float]:
        """
        Compute hybrid attribution

        Parameters:
        -----------
        alpha : float
            Weighting parameter (0 = pure Markov, 1 = pure Shapley)

        Returns:
        --------
        attribution : Dict[str, float]
            Hybrid attribution weights
        """
        shapley_attr = self.compute_shapley_component()
        markov_attr = self.compute_markov_component()

        # Weighted combination
        hybrid_attr = {}
        for channel in self.channels:
            shapley_val = shapley_attr.get(channel, 0.0)
            markov_val = markov_attr.get(channel, 0.0)

            hybrid_attr[channel] = alpha * shapley_val + (1 - alpha) * markov_val

        # Normalize
        total = sum(hybrid_attr.values())
        if total > 0:
            hybrid_attr = {ch: v / total for ch, v in hybrid_attr.items()}

        return hybrid_attr