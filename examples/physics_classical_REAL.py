"""
Physics Domain - REAL DATA from USGS Earthquakes
Uses actual seismic data from US Geological Survey
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from real_data_adapters import USGSEarthquakeAdapter
from unified_attribution import UnifiedAttributionFramework
import numpy as np

def run_test():
    """Run physics attribution with REAL USGS earthquake data"""
    print("\n" + "="*70)
    print("🌍 PHYSICS - REAL DATA FROM USGS")
    print("="*70)

    # Initialize adapter
    adapter = USGSEarthquakeAdapter()

    # Get REAL earthquake data
    real_data = adapter.get_recent_earthquakes(min_magnitude=4.5)

    if 'error' in real_data:
        print(f"Error fetching data: {real_data['error']}")
        return {'error': real_data['error']}

    earthquakes = real_data['earthquakes']

    if len(earthquakes) < 3:
        print("Insufficient data retrieved")
        return {'error': 'Insufficient data'}

    # Create feature matrix from REAL earthquake data
    X = np.array([
        [eq['magnitude'], eq['depth_km'], abs(eq['latitude'])]
        for eq in earthquakes
    ])

    # Outcome: energy release (exponential in magnitude)
    y = np.array([10 ** (1.5 * eq['magnitude']) for eq in earthquakes])

    # Run attribution
    framework = UnifiedAttributionFramework()
    attributions = framework.compute_shapley_values(
        X, y,
        feature_names=['magnitude', 'depth_km', 'latitude']
    )

    print("\n📊 Attribution Results (REAL USGS DATA):")
    print("-" * 70)
    for feature, value in attributions.items():
        print(f"  {feature:25s} → {value:.4f}")

    print("\n📋 Sample Earthquakes Analyzed:")
    for eq in earthquakes[:5]:
        print(f"  • M{eq['magnitude']:.1f} at {eq['depth_km']:.1f}km | {eq['place'][:50]}")

    print("\n✓ Data Source: United States Geological Survey")
    print("="*70 + "\n")

    return attributions

if __name__ == "__main__":
    run_test()
