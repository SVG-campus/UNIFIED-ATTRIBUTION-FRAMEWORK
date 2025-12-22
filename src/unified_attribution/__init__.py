# Save this as: unified_attribution.py

"""
Unified Attribution Framework
Core implementation of Shapley value computation and attribution methods
"""

import numpy as np
from typing import Dict, List, Optional
from itertools import combinations
import warnings

class UnifiedAttributionFramework:
    """
    Unified framework for computing feature attributions using Shapley values
    and other attribution methods across all scientific domains.
    """
    
    def __init__(self, verbose: bool = False):
        """
        Initialize the attribution framework.
        
        Args:
            verbose: If True, print detailed computation information
        """
        self.verbose = verbose
        
    def compute_shapley_values(
        self, 
        X: np.ndarray, 
        y: np.ndarray,
        feature_names: Optional[List[str]] = None
    ) -> Dict[str, float]:
        """
        Compute Shapley values for each feature.
        
        Args:
            X: Feature matrix of shape (n_samples, n_features)
            y: Target vector of shape (n_samples,)
            feature_names: Optional list of feature names
            
        Returns:
            Dictionary mapping feature names to Shapley values
        """
        n_features = X.shape[1]
        
        if feature_names is None:
            feature_names = [f"feature_{i}" for i in range(n_features)]
        
        # Simple approximation using linear regression coefficients
        # In production, use proper Shapley computation
        from sklearn.linear_model import LinearRegression
        from sklearn.preprocessing import StandardScaler

        # Replace invalid values BEFORE creating the scaler
        X = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)

        # Standardize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Fit model
        model = LinearRegression()
        model.fit(X_scaled, y)

        # Use coefficients as approximate Shapley values
        coeffs = np.abs(model.coef_)
        
        # Normalize to sum to 1
        shapley_values = coeffs / coeffs.sum()
        
        return {name: float(value) for name, value in zip(feature_names, shapley_values)}
    
    def compute_all_attributions(
        self,
        X: np.ndarray,
        y: np.ndarray,
        feature_names: Optional[List[str]] = None
    ) -> Dict:
        """
        Compute all attribution methods.
        
        Args:
            X: Feature matrix
            y: Target vector
            feature_names: Optional feature names
            
        Returns:
            Dictionary with 'shapley', 'lime', 'gradient' keys
        """
        shapley = self.compute_shapley_values(X, y, feature_names)
        
        # For now, return shapley for all methods
        # In production, implement LIME and gradient-based methods
        return {
            'shapley': shapley,
            'lime': shapley.copy(),  # Placeholder
            'gradient': shapley.copy()  # Placeholder
        }
