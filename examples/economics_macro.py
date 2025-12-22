#!/usr/bin/env python3
"""
Macroeconomic Attribution Analysis
GDP growth factor decomposition and market driver identification
"""

import numpy as np
import pandas as pd
from typing import Dict
from unified_attribution import UnifiedAttributionFramework

class EconomicsAttribution(UnifiedAttributionFramework):
    """Attribution for economic factors"""
    
    def analyze_gdp_growth(self, economic_data: pd.DataFrame) -> Dict:
        """
        Attribute GDP growth to economic factors
        
        Features:
        - Consumer spending
        - Investment
        - Government spending
        - Net exports
        - Interest rates
        - Inflation
        """
        features = economic_data[[
            'consumption', 'investment', 'govt_spending',
            'exports', 'imports', 'interest_rate', 'inflation'
        ]]
        
        target = economic_data['gdp_growth']
        
        return self.compute_all_attributions(
            features.values,
            target.values,
            feature_names=features.columns.tolist()
        )
    
    def simulate_economic_data(self, n_samples: int = 1000) -> pd.DataFrame:
        """Simulate economic data for demonstration"""
        np.random.seed(42)
        
        data = {
            'consumption': np.random.normal(1000, 100, n_samples),
            'investment': np.random.normal(300, 50, n_samples),
            'govt_spending': np.random.normal(400, 30, n_samples),
            'exports': np.random.normal(200, 40, n_samples),
            'imports': np.random.normal(180, 35, n_samples),
            'interest_rate': np.random.normal(0.05, 0.01, n_samples),
            'inflation': np.random.normal(0.02, 0.005, n_samples)
        }
        
        df = pd.DataFrame(data)
        
        # GDP growth = f(consumption, investment, govt, net exports)
        df['gdp_growth'] = (
            0.6 * df['consumption'] + 
            0.2 * df['investment'] + 
            0.15 * df['govt_spending'] + 
            0.05 * (df['exports'] - df['imports']) -
            10 * df['interest_rate'] +
            np.random.normal(0, 50, n_samples)
        )
        
        return df

if __name__ == "__main__":
    econ_attr = EconomicsAttribution()
    
    # Generate simulated data
    econ_data = econ_attr.simulate_economic_data()
    
    # Analyze GDP attribution
    results = econ_attr.analyze_gdp_growth(econ_data)
    
    print("="*70)
    print("MACROECONOMIC ATTRIBUTION: GDP GROWTH")
    print("="*70)
    print("\nFeature Contributions (Shapley Values):")
    for feat, value in results['shapley'].items():
        print(f"  {feat:<20}: {value:.6f}")
    print("\n" + "="*70)
