"""
Medicine Domain - REAL DATA from NIH RePORTER
Uses actual medical research funding data from National Institutes of Health
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from real_data_adapters import NIHReporterAdapter
from unified_attribution import UnifiedAttributionFramework
import numpy as np

def run_test():
    """Run medicine attribution with REAL NIH research data"""
    print("\n" + "="*70)
    print("🏥 MEDICINE - REAL DATA FROM NIH RePORTER")
    print("="*70)

    # Initialize adapter
    adapter = NIHReporterAdapter()

    # Get REAL medical research funding data
    real_data = adapter.search_projects("cancer", limit=15)

    if 'error' in real_data:
        print(f"Error fetching data: {real_data['error']}")
        return {'error': real_data['error']}

    projects = real_data['projects']

    if len(projects) < 3:
        print("Insufficient data retrieved")
        return {'error': 'Insufficient data'}

    # Create feature matrix from REAL research data
    X = np.array([
        [
            p['award_amount'] / 1000000,  # Millions
            p['fiscal_year'],
            len(p['title'])  # Title length as complexity proxy
        ]
        for p in projects
    ])

    # Outcome: normalized award amount
    y = np.array([p['award_amount'] for p in projects])
    y = (y - y.min()) / (y.max() - y.min() + 1e-6)

    # Run attribution
    framework = UnifiedAttributionFramework()
    attributions = framework.compute_shapley_values(
        X, y,
        feature_names=['award_millions', 'fiscal_year', 'project_complexity']
    )

    print("\n📊 Attribution Results (REAL NIH DATA):")
    print("-" * 70)
    for feature, value in attributions.items():
        print(f"  {feature:25s} → {value:.4f}")

    print("\n📋 Sample Research Projects Analyzed:")
    for p in projects[:5]:
        print(f"  • ${p['award_amount']:,.0f} | FY{p['fiscal_year']}")
        print(f"    {p['title'][:70]}...")
        print(f"    PI: {p['pi_name']} at {p['organization'][:40]}")

    print("\n✓ Data Source: NIH RePORTER - National Institutes of Health")
    print("="*70 + "\n")

    return attributions

if __name__ == "__main__":
    run_test()
