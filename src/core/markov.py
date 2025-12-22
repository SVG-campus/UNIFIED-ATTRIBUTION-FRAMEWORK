"""
Markov Chain Attribution using Removal Effects
"""

import numpy as np
from typing import List, Dict
from collections import defaultdict


class MarkovAttribution:
    """
    Compute attribution using Markov chain removal effects
    """

    def __init__(self, journeys: List[List[str]], conversions: List[int]):
        """
        Initialize Markov attribution

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
        """Extract unique channels from journeys"""
        channels = set()
        for journey in self.journeys:
            channels.update(journey)
        return sorted(list(channels))

    def build_transition_matrix(self, excluded_channel: str = None) -> Dict:
        """
        Build transition probability matrix

        Parameters:
        -----------
        excluded_channel : str
            Channel to exclude (for removal effect)

        Returns:
        --------
        transitions : Dict
            Transition probabilities
        """
        transitions = defaultdict(lambda: defaultdict(int))

        for journey, converted in zip(self.journeys, self.conversions):
            # Filter excluded channel
            if excluded_channel:
                journey = [ch for ch in journey if ch != excluded_channel]

            if not journey:
                continue

            # Count transitions
            for i in range(len(journey) - 1):
                from_state = journey[i]
                to_state = journey[i + 1]
                transitions[from_state][to_state] += 1

            # Add conversion transitions
            if converted:
                transitions[journey[-1]]['CONVERSION'] += 1
            else:
                transitions[journey[-1]]['NULL'] += 1

        # Normalize to probabilities
        transition_probs = {}
        for from_state, to_states in transitions.items():
            total = sum(to_states.values())
            if total > 0:
                transition_probs[from_state] = {
                    to_state: count / total
                    for to_state, count in to_states.items()
                }

        return transition_probs

    def compute_conversion_probability(self, transitions: Dict) -> float:
        """
        Compute overall conversion probability from transition matrix
        """
        # Simple approximation: average conversion rate from all states
        conversion_probs = []

        for from_state, to_states in transitions.items():
            if 'CONVERSION' in to_states:
                conversion_probs.append(to_states['CONVERSION'])

        return np.mean(conversion_probs) if conversion_probs else 0.0

    def compute_removal_effects(self) -> Dict[str, float]:
        """
        Compute removal effect for each channel

        Returns:
        --------
        attribution : Dict[str, float]
            Attribution weight for each channel
        """
        # Baseline conversion probability
        baseline_transitions = self.build_transition_matrix()
        baseline_prob = self.compute_conversion_probability(baseline_transitions)

        removal_effects = {}

        for channel in self.channels:
            # Compute conversion probability without this channel
            removed_transitions = self.build_transition_matrix(excluded_channel=channel)
            removed_prob = self.compute_conversion_probability(removed_transitions)

            # Removal effect = drop in conversion
            removal_effect = max(0, baseline_prob - removed_prob)
            removal_effects[channel] = removal_effect

        # Normalize to sum to 1
        total_effect = sum(removal_effects.values())
        if total_effect > 0:
            attribution = {
                ch: effect / total_effect
                for ch, effect in removal_effects.items()
            }
        else:
            # Equal attribution if no removal effects
            attribution = {ch: 1.0 / len(self.channels) for ch in self.channels}

        return attribution