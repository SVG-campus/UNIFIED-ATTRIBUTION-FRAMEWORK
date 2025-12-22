"""
Unit tests for Markov attribution
"""

import unittest
import numpy as np
from src.core.markov import MarkovAttribution


class TestMarkovAttribution(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures"""
        self.journeys = [
            ['A', 'B', 'C'],
            ['A', 'C'],
            ['B', 'C'],
            ['A', 'B']
        ]
        self.conversions = [1, 1, 0, 1]

    def test_transition_matrix(self):
        """Test transition matrix construction"""
        markov = MarkovAttribution(self.journeys, self.conversions)
        transitions = markov.build_transition_matrix()

        # Check that probabilities sum to 1
        for from_state, to_states in transitions.items():
            total = sum(to_states.values())
            self.assertAlmostEqual(total, 1.0, places=5)

    def test_removal_effects(self):
        """Test removal effect computation"""
        markov = MarkovAttribution(self.journeys, self.conversions)
        attribution = markov.compute_removal_effects()

        # Check normalization
        total = sum(attribution.values())
        self.assertAlmostEqual(total, 1.0, places=5)

        # All values non-negative
        for value in attribution.values():
            self.assertGreaterEqual(value, 0.0)


if __name__ == '__main__':
    unittest.main()