# domain_applications.py - Apply universal attribution principles to major scientific problems
"""
Cross-domain attribution solver implementing Universal Attribution Axioms
for fundamental problems in physics, mathematics, economics, biology, and climate science.

This module provides a unified framework for computing fair attributions across
diverse domains using rigorous mathematical foundations.
"""

from typing import Callable, Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import numpy as np
from numpy.typing import NDArray


# Assuming UniversalAttributionAxioms is defined elsewhere
# from unified_attribution.core import UniversalAttributionAxioms


@dataclass
class AttributionResult:
    """
    Stores the result of an attribution computation.
    
    Attributes:
        attributions: Mapping from entity names to their attribution values
        total_contribution: Total value being attributed
        axioms_verified: Whether the result satisfies all axioms
        computation_time: Time taken to compute (optional)
        metadata: Additional domain-specific information
    """
    attributions: Dict[str, float]
    total_contribution: float
    axioms_verified: bool
    computation_time: Optional[float] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    def get_ranked_attributions(self, descending: bool = True) -> List[Tuple[str, float]]:
        """Return attributions sorted by value."""
        return sorted(
            self.attributions.items(),
            key=lambda x: x[1],
            reverse=descending
        )
    
    def get_relative_attributions(self) -> Dict[str, float]:
        """Return attributions as percentages of total."""
        if self.total_contribution == 0:
            return {k: 0.0 for k in self.attributions}
        return {
            k: (v / self.total_contribution) * 100
            for k, v in self.attributions.items()
        }


class DomainType(Enum):
    """Enumeration of supported scientific domains."""
    PHYSICS = "physics"
    MATHEMATICS = "mathematics"
    ECONOMICS = "economics"
    BIOLOGY = "biology"
    MEDICINE = "medicine"
    CLIMATE = "climate_science"


class CrossDomainAttributionSolver:
    """
    Apply Universal Attribution Principles to fundamental problems
    across physics, mathematics, economics, biology, and medicine.
    
    This solver implements domain-specific contribution functions while
    maintaining universal axiom compliance across all domains.
    
    Attributes:
        axioms: The universal attribution axiom verifier
        epsilon: Numerical tolerance for floating-point comparisons
        verbose: Whether to output detailed computation logs
    """
    
    def __init__(
        self,
        axiom_verifier: Any,  # UniversalAttributionAxioms
        epsilon: float = 1e-10,
        verbose: bool = False
    ):
        """
        Initialize the cross-domain attribution solver.
        
        Args:
            axiom_verifier: Instance implementing universal attribution axioms
            epsilon: Numerical tolerance for comparisons
            verbose: Enable detailed logging
        """
        self.axioms = axiom_verifier
        self.epsilon = epsilon
        self.verbose = verbose
        self._computation_cache: Dict[str, AttributionResult] = {}
    
    def _validate_inputs(
        self,
        entities: List[str],
        contributions: Dict[str, float]
    ) -> None:
        """
        Validate input data for consistency.
        
        Args:
            entities: List of entity identifiers
            contributions: Mapping of entities to their contribution values
            
        Raises:
            ValueError: If inputs are invalid or inconsistent
        """
        if not entities:
            raise ValueError("Entity list cannot be empty")
        
        if not contributions:
            raise ValueError("Contributions dictionary cannot be empty")
        
        # Check all entities have contributions
        missing = set(entities) - set(contributions.keys())
        if missing:
            raise ValueError(f"Missing contributions for entities: {missing}")
        
        # Check for negative contributions where inappropriate
        negative = {k: v for k, v in contributions.items() if v < 0}
        if negative:
            raise ValueError(f"Negative contributions found: {negative}")
    
    def solve_quantum_measurement(
        self,
        basis_states: List[str],
        measurement_outcomes: Dict[str, float],
        normalize: bool = True
    ) -> AttributionResult:
        """
        Quantum Measurement Problem: Attribute observational collapse to basis states.
        
        Applies Born rule interpretation to compute how each basis state
        contributes to wavefunction collapse during measurement.
        
        Domain: Quantum Physics
        Problem: Which basis element contributes most to wavefunction reduction?
        
        Args:
            basis_states: List of quantum basis state labels (e.g., ['|0⟩', '|1⟩'])
            measurement_outcomes: Probability amplitudes for each state
            normalize: Whether to normalize probabilities to sum to 1
            
        Returns:
            AttributionResult with quantum state attributions
            
        Example:
            >>> solver.solve_quantum_measurement(
            ...     basis_states=['|0⟩', '|1⟩'],
            ...     measurement_outcomes={'|0⟩': 0.6, '|1⟩': 0.8}
            ... )
        """
        self._validate_inputs(basis_states, measurement_outcomes)
        
        # Normalize amplitudes if requested
        if normalize:
            total_amplitude = np.sqrt(sum(v**2 for v in measurement_outcomes.values()))
            measurement_outcomes = {
                k: v / total_amplitude
                for k, v in measurement_outcomes.items()
            }
        
        def contribution_func(states_subset: List[str]) -> float:
            """Quantum contribution: Born rule (probability amplitude squared)."""
            if not states_subset:
                return 0.0
            return sum(measurement_outcomes[s]**2 for s in states_subset)
        
        result = self.axioms.compute_universal_attribution(
            entities=basis_states,
            contribution_func=contribution_func,
            outcome_value=1.0
        )
        
        result.metadata.update({
            'domain': DomainType.PHYSICS.value,
            'problem_type': 'quantum_measurement',
            'normalized': normalize,
            'decoherence_basis': basis_states
        })
        
        return result
    
    def solve_dark_energy_attribution(
        self,
        factors: List[str],
        acceleration_contributions: Dict[str, float],
        include_interactions: bool = True,
        interaction_strength: float = 0.1
    ) -> AttributionResult:
        """
        Dark Energy Problem: Decompose cosmological acceleration.
        
        Attributes the observed acceleration of universal expansion to
        various theoretical factors including vacuum energy, modified gravity,
        and quintessence fields.
        
        Domain: Cosmological Physics
        Factors: vacuum energy, modified gravity, quintessence, etc.
        
        Args:
            factors: List of cosmological factor names
            acceleration_contributions: Base contribution of each factor to expansion
            include_interactions: Whether to model synergistic effects
            interaction_strength: Scaling factor for interaction terms (0-1)
            
        Returns:
            AttributionResult decomposing dark energy contributions
        """
        self._validate_inputs(factors, acceleration_contributions)
        
        if not 0 <= interaction_strength <= 1:
            raise ValueError("interaction_strength must be in [0, 1]")
        
        def contribution_func(factors_subset: List[str]) -> float:
            """Cosmological contribution with optional interaction terms."""
            if not factors_subset:
                return 0.0
            
            # Linear combination of base contributions
            base_contrib = sum(acceleration_contributions[f] for f in factors_subset)
            
            # Model synergistic interactions between factors
            if include_interactions and len(factors_subset) > 1:
                # Geometric mean captures multiplicative synergy
                amplitudes = [acceleration_contributions[f] for f in factors_subset]
                interaction = np.prod(amplitudes) ** (1.0 / len(factors_subset))
                return base_contrib + interaction_strength * interaction
            
            return base_contrib
        
        total_value = sum(acceleration_contributions.values())
        result = self.axioms.compute_universal_attribution(
            entities=factors,
            contribution_func=contribution_func,
            outcome_value=total_value
        )
        
        result.metadata.update({
            'domain': DomainType.PHYSICS.value,
            'problem_type': 'dark_energy_decomposition',
            'interactions_modeled': include_interactions,
            'hubble_constant_units': 'km/s/Mpc'
        })
        
        return result
    
    def solve_p_vs_np_complexity(
        self,
        algorithm_components: List[str],
        runtime_contributions: Dict[str, float],
        use_log_scale: bool = True
    ) -> AttributionResult:
        """
        P vs NP: Attribute computational complexity to algorithm components.
        
        Decomposes algorithm runtime to identify which operations contribute
        exponential versus polynomial growth, relevant to the P vs NP question.
        
        Domain: Computational Complexity Theory
        Goal: Identify bottleneck operations in algorithm runtime
        
        Args:
            algorithm_components: Names of algorithm steps/operations
            runtime_contributions: Base runtime factor for each component
            use_log_scale: Whether to work in log-space (recommended for large values)
            
        Returns:
            AttributionResult showing complexity decomposition
        """
        self._validate_inputs(algorithm_components, runtime_contributions)
        
        def contribution_func(components_subset: List[str]) -> float:
            """Complexity grows multiplicatively; use log-space for stability."""
            if not components_subset:
                return 0.0
            
            if use_log_scale:
                # Work in log-space to handle exponential growth
                log_complexity = sum(
                    np.log(max(runtime_contributions[comp], self.epsilon))
                    for comp in components_subset
                )
                return log_complexity
            else:
                # Direct multiplicative complexity
                complexity = np.prod([runtime_contributions[comp] for comp in components_subset])
                return complexity
        
        # Total outcome in log-space if using logarithms
        if use_log_scale:
            outcome = sum(
                np.log(max(runtime_contributions[c], self.epsilon))
                for c in algorithm_components
            )
        else:
            outcome = np.prod([runtime_contributions[c] for c in algorithm_components])
        
        result = self.axioms.compute_universal_attribution(
            entities=algorithm_components,
            contribution_func=contribution_func,
            outcome_value=outcome
        )
        
        result.metadata.update({
            'domain': DomainType.MATHEMATICS.value,
            'problem_type': 'computational_complexity',
            'log_scale': use_log_scale,
            'complexity_class': 'unknown'  # Would be determined by analysis
        })
        
        return result
    
    def solve_cancer_treatment_synergy(
        self,
        drug_combinations: List[str],
        tumor_suppression: Dict[str, float],
        synergy_model: str = 'exponential',
        synergy_base: float = 1.2
    ) -> AttributionResult:
        """
        Cancer Treatment: Attribute tumor suppression to drug combinations.
        
        Discovers optimal multi-drug protocols by computing synergistic
        Shapley values that account for drug-drug interactions.
        
        Domain: Oncology/Pharmacology
        Goal: Optimize multi-drug cancer treatment protocols
        
        Args:
            drug_combinations: Names of therapeutic drugs
            tumor_suppression: Individual suppression efficacy (0-1 scale)
            synergy_model: Type of synergy ('exponential', 'linear', 'bliss')
            synergy_base: Base factor for exponential synergy (>1 for positive)
            
        Returns:
            AttributionResult showing drug attribution and synergy effects
        """
        self._validate_inputs(drug_combinations, tumor_suppression)
        
        # Validate suppression values are in [0, 1]
        invalid = {k: v for k, v in tumor_suppression.items() if not 0 <= v <= 1}
        if invalid:
            raise ValueError(f"Tumor suppression must be in [0, 1]: {invalid}")
        
        def contribution_func(drugs_subset: List[str]) -> float:
            """Model drug efficacy with synergistic interactions."""
            if not drugs_subset:
                return 0.0
            
            # Sum individual drug effects
            individual_effect = sum(tumor_suppression[d] for d in drugs_subset)
            
            # Apply synergy model for multi-drug combinations
            if len(drugs_subset) > 1:
                if synergy_model == 'exponential':
                    # Exponential synergy: effect amplifies with more drugs
                    synergy_factor = synergy_base ** (len(drugs_subset) - 1)
                    return individual_effect * synergy_factor
                    
                elif synergy_model == 'bliss':
                    # Bliss independence model from pharmacology
                    # P(A or B) = P(A) + P(B) - P(A)*P(B)
                    combined = 1.0
                    for drug in drugs_subset:
                        combined *= (1 - tumor_suppression[drug])
                    return 1.0 - combined
                    
                elif synergy_model == 'linear':
                    # Simple additive effect
                    return individual_effect
                    
                else:
                    raise ValueError(f"Unknown synergy model: {synergy_model}")
            
            return individual_effect
        
        result = self.axioms.compute_universal_attribution(
            entities=drug_combinations,
            contribution_func=contribution_func,
            outcome_value=1.0  # Normalized to 100% suppression target
        )
        
        result.metadata.update({
            'domain': DomainType.MEDICINE.value,
            'problem_type': 'cancer_drug_synergy',
            'synergy_model': synergy_model,
            'synergy_base': synergy_base,
            'therapeutic_index': 'not_computed'
        })
        
        return result
    
    def solve_economic_inequality(
        self,
        factors: List[str],
        output_contributions: Dict[str, float],
        current_distribution: Dict[str, float],
        redistribution_policy: str = 'proportional'
    ) -> Dict[str, Any]:
        """
        Economic Inequality: Fair attribution and optimal redistribution.
        
        Computes fair economic attributions based on factor contributions
        and calculates redistribution needed to achieve equity.
        
        Domain: Economics
        Factors: labor, capital, technology, policy, natural resources
        
        Args:
            factors: Economic production factors
            output_contributions: Measured contribution to total output
            current_distribution: Current distribution of wealth/income
            redistribution_policy: Method for computing fair shares
            
        Returns:
            Dictionary containing fair attributions, redistribution plan, and metrics
        """
        self._validate_inputs(factors, output_contributions)
        self._validate_inputs(factors, current_distribution)
        
        def contribution_func(factors_subset: List[str]) -> float:
            """Economic production function (currently linear)."""
            if not factors_subset:
                return 0.0
            return sum(output_contributions[f] for f in factors_subset)
        
        # Compute fair attribution via Shapley values
        fair_attribution = self.axioms.compute_universal_attribution(
            entities=factors,
            contribution_func=contribution_func,
            outcome_value=sum(output_contributions.values())
        )
        
        # Calculate redistribution needed
        redistribution = {}
        for factor in factors:
            fair_share = fair_attribution.attributions[factor]
            current_share = current_distribution[factor]
            redistribution[factor] = fair_share - current_share
        
        # Compute inequality metrics
        total_redistribution = sum(abs(v) for v in redistribution.values()) / 2
        
        # Gini coefficient before and after
        gini_before = self._compute_gini_coefficient(list(current_distribution.values()))
        gini_after = self._compute_gini_coefficient(
            list(fair_attribution.attributions.values())
        )
        
        return {
            'fair_attribution': fair_attribution,
            'redistribution_needed': redistribution,
            'total_redistribution_volume': total_redistribution,
            'inequality_reduction': gini_before - gini_after,
            'gini_before': gini_before,
            'gini_after': gini_after,
            'redistribution_policy': redistribution_policy,
            'metadata': {
                'domain': DomainType.ECONOMICS.value,
                'problem_type': 'inequality_analysis'
            }
        }
    
    def solve_climate_warming_attribution(
        self,
        sources: List[str],
        temperature_contributions: Dict[str, float],
        include_feedback: bool = True,
        feedback_strength: float = 1.15
    ) -> AttributionResult:
        """
        Climate Science: Attribute temperature rise to emission sources.
        
        Decomposes observed global warming into contributions from various
        greenhouse gases and other climate forcings, including feedback effects.
        
        Domain: Climate Science
        Sources: CO₂, methane, N₂O, aerosols, solar cycles, albedo changes
        
        Args:
            sources: Names of climate forcing sources
            temperature_contributions: Direct temperature effect (°C) of each source
            include_feedback: Whether to model climate feedback amplification
            feedback_strength: Amplification factor for feedback loops (>1)
            
        Returns:
            AttributionResult decomposing warming attribution
        """
        self._validate_inputs(sources, temperature_contributions)
        
        if feedback_strength < 1.0:
            raise ValueError("feedback_strength must be >= 1.0 for positive feedback")
        
        def contribution_func(sources_subset: List[str]) -> float:
            """Temperature contribution with climate feedback loops."""
            if not sources_subset:
                return 0.0
            
            # Direct radiative forcing effects
            direct_warming = sum(temperature_contributions[s] for s in sources_subset)
            
            # Model positive feedback amplification
            # More sources active = stronger feedback (water vapor, ice-albedo)
            if include_feedback and len(sources_subset) > 1:
                feedback_amplification = feedback_strength ** (len(sources_subset) - 1)
                return direct_warming * feedback_amplification
            
            return direct_warming
        
        total_warming = sum(temperature_contributions.values())
        result = self.axioms.compute_universal_attribution(
            entities=sources,
            contribution_func=contribution_func,
            outcome_value=total_warming
        )
        
        # Compute equilibrium climate sensitivity estimate
        co2_attribution = result.attributions.get('CO₂', 0.0)
        ecs_estimate = co2_attribution * 3.0  # Rough ECS scaling
        
        result.metadata.update({
            'domain': DomainType.CLIMATE.value,
            'problem_type': 'warming_attribution',
            'includes_feedback': include_feedback,
            'feedback_strength': feedback_strength,
            'equilibrium_climate_sensitivity_estimate': ecs_estimate,
            'temperature_units': 'celsius',
            'baseline_period': '1850-1900'
        })
        
        return result
    
    @staticmethod
    def _compute_gini_coefficient(values: List[float]) -> float:
        """
        Compute Gini coefficient as a measure of inequality.
        
        Args:
            values: Distribution of wealth/income
            
        Returns:
            Gini coefficient (0 = perfect equality, 1 = perfect inequality)
        """
        if not values or all(v == 0 for v in values):
            return 0.0
        
        sorted_values = np.sort(values)
        n = len(values)
        index = np.arange(1, n + 1)
        
        return (2 * np.sum(index * sorted_values)) / (n * np.sum(sorted_values)) - (n + 1) / n
    
    def clear_cache(self) -> None:
        """Clear the computation cache."""
        self._computation_cache.clear()
    
    def get_supported_domains(self) -> List[str]:
        """Return list of supported scientific domains."""
        return [domain.value for domain in DomainType]


# Utility functions for common operations
def compare_attributions(
    result1: AttributionResult,
    result2: AttributionResult,
    tolerance: float = 1e-6
) -> Dict[str, Any]:
    """
    Compare two attribution results for similarity.
    
    Args:
        result1: First attribution result
        result2: Second attribution result
        tolerance: Numerical tolerance for floating-point comparison
        
    Returns:
        Dictionary with comparison metrics
    """
    common_entities = set(result1.attributions.keys()) & set(result2.attributions.keys())
    
    if not common_entities:
        return {'similar': False, 'reason': 'No common entities'}
    
    differences = {
        entity: abs(result1.attributions[entity] - result2.attributions[entity])
        for entity in common_entities
    }
    
    max_diff = max(differences.values())
    mean_diff = np.mean(list(differences.values()))
    
    return {
        'similar': max_diff < tolerance,
        'max_difference': max_diff,
        'mean_difference': mean_diff,
        'differences': differences,
        'common_entities': list(common_entities)
    }


def visualize_attribution_result(
    result: AttributionResult,
    top_n: Optional[int] = None
) -> str:
    """
    Create a simple text visualization of attribution results.
    
    Args:
        result: Attribution result to visualize
        top_n: Show only top N entities (None = show all)
        
    Returns:
        Formatted string representation
    """
    ranked = result.get_ranked_attributions()
    
    if top_n:
        ranked = ranked[:top_n]
    
    relative = result.get_relative_attributions()
    
    lines = ["Attribution Results", "=" * 50]
    
    for entity, value in ranked:
        pct = relative[entity]
        bar_length = int(pct / 2)  # Scale to 50 chars max
        bar = "█" * bar_length
        lines.append(f"{entity:20s} {value:10.4f} ({pct:5.1f}%) {bar}")
    
    lines.append("=" * 50)
    lines.append(f"Total: {result.total_contribution:.4f}")
    
    return "\n".join(lines)


if __name__ == "__main__":
    # Example usage and testing
    print("Cross-Domain Attribution Solver")
    print("Supports domains:", [d.value for d in DomainType])
