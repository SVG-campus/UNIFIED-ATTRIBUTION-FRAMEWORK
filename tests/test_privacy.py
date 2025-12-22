"""
Unit tests for differential privacy
"""

import unittest
import numpy as np
from src.core.privacy import PrivateAttribution


class TestPrivateAttribution(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures"""
        self.epsilon = 1.0
        self.private = PrivateAttribution(epsilon=self.epsilon)
        self.attribution = {'A': 0.4, 'B': 0.35, 'C': 0.25}

    def test_laplace_noise(self):
        """Test Laplace noise generation"""
        noise = self.private.laplace_noise(sensitivity=1.0, size=1000)

        # Check mean approximately 0
        self.assertLess(abs(np.mean(noise)), 0.1)

        # Check scale
        expected_scale = 1.0 / self.epsilon
        actual_scale = np.std(noise) * np.sqrt(2)
        self.assertAlmostEqual(actual_scale, expected_scale, delta=0.5)

    def test_privatize_attribution(self):
        """Test attribution privatization"""
        noisy = self.private.privatize_attribution(self.attribution)

        # Check normalization
        total = sum(noisy.values())
        self.assertAlmostEqual(total, 1.0, places=5)

        # Check keys match
        self.assertEqual(set(noisy.keys()), set(self.attribution.keys()))

        # Check noise was added
        differences = [abs(noisy[k] - self.attribution[k]) for k in noisy.keys()]
        self.assertGreater(sum(differences), 0.0)

    def test_privacy_composition(self):
        """Test privacy loss composition"""
        n_queries = 10
        total_epsilon = self.private.compute_privacy_loss(n_queries)

        # Should be larger than single query epsilon
        self.assertGreater(total_epsilon, self.epsilon)


if __name__ == '__main__':
    unittest.main()