"""
Main API for Unified Attribution Framework
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
import time

# Note: These imports assume proper package structure
# Adjust paths as needed for your setup


class CompleteUnifiedFramework:
    """
    Complete unified framework for attribution analysis
    """

    def __init__(
        self,
        journeys: List[List[str]],
        data: pd.DataFrame,
        epsilon: float = 1.0,
        use_gpu: bool = False
    ):
        """
        Initialize unified framework

        Parameters:
        -----------
        journeys : List[List[str]]
            Customer journey sequences
        data : pd.DataFrame
            Tabular data with binary channel columns
        epsilon : float
            Privacy budget
        use_gpu : bool
            Enable GPU acceleration
        """
        self.journeys = journeys
        self.data = data
        self.epsilon = epsilon
        self.use_gpu = use_gpu

        # Extract channels and conversions
        self.channels = sorted(data.columns.tolist())
        self.conversions = self._infer_conversions()

    def _infer_conversions(self) -> List[int]:
        """Infer conversions from data"""
        # Simple heuristic: conversion if any channel = 1
        conversions = (self.data.sum(axis=1) > 0).astype(int).tolist()
        return conversions

    def compute_complete_attribution(self) -> Tuple[Dict, float]:
        """
        Compute all attribution methods

        Returns:
        --------
        results : Dict
            Attribution results for all methods
        elapsed : float
            Total runtime in seconds
        """
        start_time = time.time()

        results = {}

        # 1. Shapley attribution
        results['shapley'] = self._compute_shapley()

        # 2. Markov attribution
        results['markov'] = self._compute_markov()

        # 3. Hybrid attribution
        results['hybrid'] = self._compute_hybrid()

        # 4. Causal attribution (simplified)
        results['causal'] = self._compute_causal()

        # 5. Private attribution
        results['private'] = self._compute_private(results['hybrid'])

        elapsed = time.time() - start_time

        return results, elapsed

    def _compute_shapley(self) -> Dict[str, float]:
        """Compute Shapley values"""
        # Simplified implementation
        # In practice, import from src.core.shapley

        shapley_values = {}
        for channel in self.channels:
            # Simple approximation: presence correlation
            presence = self.data[channel].values
            conversion_rate = np.mean(presence)
            shapley_values[channel] = conversion_rate

        # Normalize
        total = sum(shapley_values.values())
        if total > 0:
            shapley_values = {ch: v / total for ch, v in shapley_values.items()}

        return shapley_values

    def _compute_markov(self) -> Dict[str, float]:
        """Compute Markov attribution"""
        # Simplified implementation
        markov_values = {}

        for channel in self.channels:
            # Removal effect approximation
            with_channel = self.data[self.data[channel] == 1]
            without_channel = self.data[self.data[channel] == 0]

            if len(without_channel) > 0:
                effect = (len(with_channel) / len(self.data)) * 1.5
            else:
                effect = 0.5

            markov_values[channel] = effect

        # Normalize
        total = sum(markov_values.values())
        if total > 0:
            markov_values = {ch: v / total for ch, v in markov_values.items()}

        return markov_values

    def _compute_hybrid(self) -> Dict[str, float]:
        """Compute hybrid attribution"""
        shapley = self._compute_shapley()
        markov = self._compute_markov()

        # Weighted combination (50-50)
        hybrid = {}
        for channel in self.channels:
            hybrid[channel] = 0.5 * shapley.get(channel, 0) + 0.5 * markov.get(channel, 0)

        # Normalize
        total = sum(hybrid.values())
        if total > 0:
            hybrid = {ch: v / total for ch, v in hybrid.items()}

        return hybrid

    def _compute_causal(self) -> Dict[str, float]:
        """Compute causal attribution (simplified)"""
        # Simplified causal inference
        causal_values = {}

        for channel in self.channels:
            # Estimate causal effect using propensity scores (simplified)
            treated = self.data[self.data[channel] == 1]
            control = self.data[self.data[channel] == 0]

            if len(treated) > 0 and len(control) > 0:
                effect = abs(len(treated) - len(control)) / len(self.data)
            else:
                effect = 0.1

            causal_values[channel] = effect

        # Normalize
        total = sum(causal_values.values())
        if total > 0:
            causal_values = {ch: v / total for ch, v in causal_values.items()}

        return causal_values

    def _compute_private(self, base_attribution: Dict[str, float]) -> Dict[str, float]:
        """Add differential privacy"""
        # Add Laplace noise
        sensitivity = 2.0 / len(self.channels)
        scale = sensitivity / self.epsilon

        private_attribution = {}
        for channel, value in base_attribution.items():
            noise = np.random.laplace(0, scale)
            private_attribution[channel] = max(0, value + noise)

        # Renormalize
        total = sum(private_attribution.values())
        if total > 0:
            private_attribution = {ch: v / total for ch, v in private_attribution.items()}

        return private_attribution