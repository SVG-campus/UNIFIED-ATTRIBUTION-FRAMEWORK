"""
Differential Privacy for Attribution
Laplace mechanism and privacy composition
"""

import numpy as np
from typing import Dict


class PrivateAttribution:
    """
    Differential privacy-preserving attribution
    """

    def __init__(self, epsilon: float = 1.0, delta: float = 1e-5):
        """
        Initialize private attribution

        Parameters:
        -----------
        epsilon : float
            Privacy budget (lower = more privacy)
        delta : float
            Privacy parameter for advanced composition
        """
        self.epsilon = epsilon
        self.delta = delta
        self.privacy_spent = 0.0

    def laplace_noise(self, sensitivity: float, size: int = 1) -> np.ndarray:
        """
        Generate Laplace noise calibrated to epsilon

        Parameters:
        -----------
        sensitivity : float
            Global sensitivity of the function
        size : int
            Number of noise samples

        Returns:
        --------
        noise : np.ndarray
            Laplace noise samples
        """
        scale = sensitivity / self.epsilon
        noise = np.random.laplace(0, scale, size)
        return noise

    def privatize_attribution(self, attribution: Dict[str, float]) -> Dict[str, float]:
        """
        Add differential privacy noise to attribution weights

        Parameters:
        -----------
        attribution : Dict[str, float]
            True attribution weights

        Returns:
        --------
        noisy_attribution : Dict[str, float]
            Privatized attribution weights
        """
        # Global sensitivity = max change in any attribution weight
        # when one data point changes
        n_channels = len(attribution)
        sensitivity = 2.0 / n_channels  # Conservative estimate

        noisy_attribution = {}
        for channel, weight in attribution.items():
            noise = self.laplace_noise(sensitivity, size=1)[0]
            noisy_weight = max(0, weight + noise)  # Clip to non-negative
            noisy_attribution[channel] = noisy_weight

        # Renormalize to sum to 1
        total = sum(noisy_attribution.values())
        if total > 0:
            noisy_attribution = {
                ch: w / total for ch, w in noisy_attribution.items()
            }

        # Track privacy spent
        self.privacy_spent += self.epsilon

        return noisy_attribution

    def compute_privacy_loss(self, n_queries: int) -> float:
        """
        Compute total privacy loss under composition

        Parameters:
        -----------
        n_queries : int
            Number of queries made

        Returns:
        --------
        total_epsilon : float
            Total privacy budget spent
        """
        # Advanced composition theorem
        total_epsilon = np.sqrt(2 * n_queries * np.log(1 / self.delta)) * self.epsilon
        return total_epsilon

    def privacy_budget_remaining(self) -> float:
        """Get remaining privacy budget"""
        return max(0, self.epsilon - self.privacy_spent)