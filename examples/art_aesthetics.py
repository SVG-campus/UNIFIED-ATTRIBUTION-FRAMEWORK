#!/usr/bin/env python3
"""
Aesthetic Attribution Analysis
Decomposing artistic appeal and emotional impact
"""

import numpy as np
from typing import Dict
from unified_attribution import UnifiedAttributionFramework

class ArtAttribution(UnifiedAttributionFramework):
    """Attribution for aesthetic properties"""
    
    def analyze_visual_appeal(self, image_features: np.ndarray,
                              aesthetic_score: np.ndarray) -> Dict:
        """
        Attribute aesthetic appeal to visual features
        
        Features:
        - Color harmony (HSV distribution)
        - Symmetry
        - Complexity (edge density)
        - Golden ratio composition
        - Contrast
        """
        feature_names = [
            'Color_Harmony', 'Symmetry', 'Complexity',
            'Golden_Ratio', 'Contrast', 'Brightness'
        ]
        
        return self.compute_all_attributions(
            image_features,
            aesthetic_score,
            feature_names=feature_names
        )
    
    def simulate_art_features(self, n_samples: int = 500) -> tuple:
        """Generate simulated art features"""
        np.random.seed(42)
        
        phi = (1 + np.sqrt(5)) / 2  # Golden ratio
        
        features = np.column_stack([
            np.random.beta(2, 5, n_samples),      # Color harmony
            np.random.beta(3, 3, n_samples),      # Symmetry  
            np.random.gamma(2, 2, n_samples),     # Complexity
            np.abs(np.random.normal(phi, 0.2, n_samples)),  # Golden ratio
            np.random.beta(4, 2, n_samples),      # Contrast
            np.random.beta(3, 2, n_samples)       # Brightness
        ])
        
        # Aesthetic score = weighted combination
        aesthetic = (
            0.3 * features[:, 0] +  # Color harmony
            0.25 * features[:, 1] + # Symmetry
            0.1 * features[:, 2] +  # Complexity
            0.2 * np.abs(features[:, 3] - phi) +  # Golden ratio proximity
            0.1 * features[:, 4] +  # Contrast
            0.05 * features[:, 5] + # Brightness
            np.random.normal(0, 0.1, n_samples)
        )
        
        return features, aesthetic

if __name__ == "__main__":
    art_attr = ArtAttribution()
    
    # Generate simulated art data
    features, scores = art_attr.simulate_art_features()
    
    # Analyze aesthetic attribution
    results = art_attr.analyze_visual_appeal(features, scores)
    
    print("="*70)
    print("AESTHETIC ATTRIBUTION: VISUAL APPEAL")
    print("="*70)
    print("\nFeature Contributions:")
    for feat, value in results['shapley'].items():
        print(f"  {feat:<20}: {value:.6f}")
    print("\n" + "="*70)
