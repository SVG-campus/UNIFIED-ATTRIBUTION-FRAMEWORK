"""
Chemistry Domain - REAL DATA from PubChem (NIH)
Uses actual chemical compound data from US National Institutes of Health
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from real_data_adapters import PubChemAdapter
from unified_attribution import UnifiedAttributionFramework
import numpy as np

def run_test():
    """Run chemistry attribution with REAL PubChem data"""
    print("\n" + "="*70)
    print("🧪 CHEMISTRY - REAL DATA FROM PUBCHEM (NIH)")
    print("="*70)

    # Initialize adapter
    adapter = PubChemAdapter()

    # Get REAL chemical data
    compounds_to_analyze = [
        'aspirin', 'ibuprofen', 'acetaminophen',  # Pain relievers
        'caffeine', 'nicotine', 'morphine',        # Alkaloids
        'glucose', 'fructose', 'sucrose',          # Sugars
        'ethanol', 'methanol', 'propanol'          # Alcohols
    ]

    real_data = adapter.get_compound_properties(compounds_to_analyze)

    if 'error' in real_data:
        print(f"Error fetching data: {real_data['error']}")
        return {'error': real_data['error']}

    # Extract features from REAL data
    compounds = real_data['compounds']

    if len(compounds) < 3:
        print("Insufficient data retrieved")
        return {'error': 'Insufficient data'}

    # Create feature matrix from REAL molecular weights
    X = np.array([[c['molecular_weight'], len(c['formula'])] for c in compounds])

    # Create outcome: classify by molecular weight ranges
    y = np.array([1 if c['molecular_weight'] > 150 else 0 for c in compounds])

    # Run attribution
    framework = UnifiedAttributionFramework()
    attributions = framework.compute_shapley_values(
        X, y,
        feature_names=['molecular_weight', 'formula_length']
    )

    print("\n📊 Attribution Results (REAL NIH DATA):")
    print("-" * 70)
    for feature, value in attributions.items():
        print(f"  {feature:25s} → {value:.4f}")

    print("\n📋 Sample Compounds Analyzed:")
    for c in compounds[:5]:
        print(f"  • {c['compound']:15s} | MW: {c['molecular_weight']:7.2f} | {c['formula']}")

    print("\n✓ Data Source: PubChem / National Institutes of Health")
    print("="*70 + "\n")

    return attributions

if __name__ == "__main__":
    run_test()
