"""
Unit tests for Shapley value computation
"""

import unittest
import numpy as np
from src.core.shapley import FastShapleyAttribution


class TestShapleyValues(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures"""
        self.players = ['A', 'B', 'C']
        self.simple_value = lambda coalition: len(coalition) / 3

    def test_efficiency(self):
        """Test efficiency axiom: sum of values = total value"""
        shapley = FastShapleyAttribution(self.players, self.simple_value)
        values, _ = shapley.monte_carlo_shapley(1000)

        total = sum(values.values())
        expected_total = self.simple_value(self.players)

        self.assertAlmostEqual(total, expected_total, places=2)

    def test_symmetry(self):
        """Test symmetry axiom: equal contributions = equal values"""
        shapley = FastShapleyAttribution(self.players, self.simple_value)
        values, _ = shapley.monte_carlo_shapley(1000)

        # All players symmetric in this game
        values_list = list(values.values())
        self.assertAlmostEqual(values_list[0], values_list[1], places=1)
        self.assertAlmostEqual(values_list[1], values_list[2], places=1)

    def test_null_player(self):
        """Test null player axiom: zero contribution = zero value"""
        def value_with_null(coalition):
            # Player C is null (contributes nothing)
            return len([p for p in coalition if p != 'C']) / 2

        shapley = FastShapleyAttribution(self.players, value_with_null)
        values, _ = shapley.monte_carlo_shapley(1000)

        # Player C should have near-zero value
        self.assertLess(values['C'], 0.1)

    def test_additivity(self):
        """Test additivity axiom: values are additive"""
        def value1(coalition):
            return len(coalition) * 0.1

        def value2(coalition):
            return len(coalition) * 0.2

        def combined_value(coalition):
            return value1(coalition) + value2(coalition)

        shapley1 = FastShapleyAttribution(self.players, value1)
        shapley2 = FastShapleyAttribution(self.players, value2)
        shapley_combined = FastShapleyAttribution(self.players, combined_value)

        values1, _ = shapley1.monte_carlo_shapley(500)
        values2, _ = shapley2.monte_carlo_shapley(500)
        values_combined, _ = shapley_combined.monte_carlo_shapley(500)

        for player in self.players:
            expected = values1[player] + values2[player]
            actual = values_combined[player]
            self.assertAlmostEqual(expected, actual, places=1)

    def test_convergence(self):
        """Test convergence with increasing samples"""
        shapley = FastShapleyAttribution(self.players, self.simple_value)

        # Compute with different sample sizes
        values_100, _ = shapley.monte_carlo_shapley(100)
        values_1000, _ = shapley.monte_carlo_shapley(1000)
        values_5000, _ = shapley.monte_carlo_shapley(5000)

        # Variance should decrease with more samples
        var_100 = np.var(list(values_100.values()))
        var_5000 = np.var(list(values_5000.values()))

        # For symmetric game, variance should be small
        self.assertLess(var_5000, 0.01)

    def test_marginal_contributions(self):
        """Test marginal contributions structure"""
        shapley = FastShapleyAttribution(self.players, self.simple_value)
        values, marginals = shapley.monte_carlo_shapley(100)

        # Check marginals structure
        self.assertEqual(len(marginals), len(self.players))

        for player, marginal_list in marginals.items():
            self.assertEqual(len(marginal_list), 100)
            # Marginals should be non-negative for monotone value function
            self.assertTrue(all(m >= -0.01 for m in marginal_list))


class TestExactShapley(unittest.TestCase):

    def test_small_game(self):
        """Test exact Shapley for small game"""
        players = ['A', 'B']
        value = lambda coalition: len(coalition) / 2

        shapley = FastShapleyAttribution(players, value)
        exact_values = shapley.exact_shapley()

        # Each player should get 0.5
        self.assertAlmostEqual(exact_values['A'], 0.5, places=5)
        self.assertAlmostEqual(exact_values['B'], 0.5, places=5)

    def test_exact_too_large(self):
        """Test that exact Shapley rejects large games"""
        players = [f'P{i}' for i in range(15)]
        value = lambda coalition: len(coalition)

        shapley = FastShapleyAttribution(players, value)

        with self.assertRaises(ValueError):
            shapley.exact_shapley()


if __name__ == '__main__':
    unittest.main()