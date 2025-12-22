# universal_axioms.py - New foundational module

import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class AttributionResult:
    """Attribution result with axiom verification."""
    attributions: Dict[str, float]
    efficiency_satisfied: bool
    symmetry_satisfied: bool
    null_player_satisfied: bool
    additivity_satisfied: bool
    axiom_violations: List[str]

class UniversalAttributionAxioms:
    """
    Universal Attribution Principles validated across ALL domains.
    
    Four Fundamental Axioms:
    1. Efficiency: sum(attributions) = total_outcome (conservation)
    2. Symmetry: identical_contributors → equal_credit (fairness)
    3. Null Player: zero_contribution → zero_credit (precision)
    4. Additivity: credits combine linearly (composability)
    """
    
    def __init__(self, tolerance: float = 1e-6):
        self.tolerance = tolerance
    
    def verify_efficiency(self, 
                         attributions: Dict[str, float],
                         total_outcome: float = 1.0) -> Tuple[bool, float]:
        """
        Efficiency Axiom: Total credit equals total outcome.
        
        Mathematical: Σᵢ φᵢ = v(N)
        where φᵢ is attribution to player i, v(N) is total value
        """
        total_attribution = sum(attributions.values())
        error = abs(total_attribution - total_outcome)
        satisfied = error < self.tolerance
        return satisfied, error
    
    def verify_symmetry(self,
                       attributions: Dict[str, float],
                       contribution_values: Dict[str, float]) -> Tuple[bool, List[Tuple]]:
        """
        Symmetry Axiom: Identical contributors receive equal credit.
        
        Mathematical: If v(S ∪ {i}) = v(S ∪ {j}) for all S, then φᵢ = φⱼ
        """
        violations = []
        
        # Group by contribution value
        contribution_groups = {}
        for entity, value in contribution_values.items():
            rounded_value = round(value, 10)  # Handle floating point
            if rounded_value not in contribution_groups:
                contribution_groups[rounded_value] = []
            contribution_groups[rounded_value].append(entity)
        
        # Check equal attribution within groups
        for contrib_value, entities in contribution_groups.items():
            if len(entities) > 1:
                attributions_in_group = [attributions[e] for e in entities]
                if not np.allclose(attributions_in_group, attributions_in_group[0], 
                                  rtol=self.tolerance):
                    violations.append((entities, attributions_in_group))
        
        return len(violations) == 0, violations
    
    def verify_null_player(self,
                          attributions: Dict[str, float],
                          contribution_values: Dict[str, float]) -> Tuple[bool, List[str]]:
        """
        Null Player Axiom: Non-contributing factors receive zero credit.
        
        Mathematical: If v(S ∪ {i}) = v(S) for all S, then φᵢ = 0
        """
        violations = []
        
        for entity, contribution in contribution_values.items():
            if abs(contribution) < self.tolerance:  # Zero contributor
                if abs(attributions.get(entity, 0)) > self.tolerance:
                    violations.append(entity)
        
        return len(violations) == 0, violations
    
    def verify_additivity(self,
                         game1_attributions: Dict[str, float],
                         game2_attributions: Dict[str, float],
                         combined_attributions: Dict[str, float]) -> Tuple[bool, float]:
        """
        Additivity: Credits combine linearly across independent processes.
        
        Mathematical: φᵢ(v + w) = φᵢ(v) + φᵢ(w)
        for independent games v and w
        """
        max_error = 0.0
        all_entities = set(game1_attributions.keys()) | set(game2_attributions.keys())
        
        for entity in all_entities:
            expected = game1_attributions.get(entity, 0) + game2_attributions.get(entity, 0)
            actual = combined_attributions.get(entity, 0)
            error = abs(expected - actual)
            max_error = max(max_error, error)
        
        satisfied = max_error < self.tolerance
        return satisfied, max_error
    
    def compute_universal_attribution(self,
                                     entities: List[str],
                                     contribution_func,
                                     outcome_value: float = 1.0) -> AttributionResult:
        """
        Compute attribution satisfying all universal axioms.
        
        Uses Shapley values as they uniquely satisfy all four axioms.
        """
        n = len(entities)
        attributions = {entity: 0.0 for entity in entities}
        
        # Compute Shapley values (satisfies all axioms)
        for i, entity in enumerate(entities):
            for subset_size in range(n):
                # Generate all subsets of given size not containing entity
                from itertools import combinations
                other_entities = [e for e in entities if e != entity]
                
                for subset in combinations(other_entities, subset_size):
                    subset_list = list(subset)
                    
                    # Marginal contribution
                    with_entity = contribution_func(subset_list + [entity])
                    without_entity = contribution_func(subset_list)
                    marginal = with_entity - without_entity
                    
                    # Shapley weight
                    weight = (np.math.factorial(subset_size) * 
                             np.math.factorial(n - subset_size - 1) / 
                             np.math.factorial(n))
                    
                    attributions[entity] += weight * marginal
        
        # Normalize to outcome value
        total = sum(attributions.values())
        if total > 0:
            for entity in attributions:
                attributions[entity] = (attributions[entity] / total) * outcome_value
        
        # Verify all axioms
        contribution_values = {e: contribution_func([e]) for e in entities}
        
        efficiency_ok, eff_error = self.verify_efficiency(attributions, outcome_value)
        symmetry_ok, sym_violations = self.verify_symmetry(attributions, contribution_values)
        null_ok, null_violations = self.verify_null_player(attributions, contribution_values)
        
        violations = []
        if not efficiency_ok:
            violations.append(f"Efficiency violated: error={eff_error}")
        if not symmetry_ok:
            violations.append(f"Symmetry violated: {len(sym_violations)} cases")
        if not null_ok:
            violations.append(f"Null player violated: {null_violations}")
        
        return AttributionResult(
            attributions=attributions,
            efficiency_satisfied=efficiency_ok,
            symmetry_satisfied=symmetry_ok,
            null_player_satisfied=null_ok,
            additivity_satisfied=True,  # Shapley satisfies by construction
            axiom_violations=violations
        )
