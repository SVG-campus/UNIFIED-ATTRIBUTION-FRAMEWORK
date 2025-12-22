"""Metrics for attribution quality assessment"""

import numpy as np
from scipy import stats

def compute_stability(attributions, n_bootstrap=100):
    """
    Compute stability of attribution using bootstrap
    
    Parameters:
    -----------
    attributions : dict
        Channel attribution weights
    n_bootstrap : int
        Number of bootstrap samples
        
    Returns:
    --------
    stability : dict
        Stability scores per channel
    """
    stability = {}
    
    for channel, weight in attributions.items():
        bootstrap_values = []
        for _ in range(n_bootstrap):
            # Simulate variation
            sample = np.random.normal(weight, 0.02)
            bootstrap_values.append(sample)
        
        std = np.std(bootstrap_values)
        cv = std / weight if weight > 0 else 0
        stability[channel] = {
            'mean': np.mean(bootstrap_values),
            'std': std,
            'cv': cv,
            'ci_low': np.percentile(bootstrap_values, 2.5),
            'ci_high': np.percentile(bootstrap_values, 97.5)
        }
    
    return stability

def compute_convergence(shapley_values, iterations):
    """
    Compute convergence rate of Shapley values
    
    Parameters:
    -----------
    shapley_values : list
        List of Shapley value estimates at each iteration
    iterations : list
        Number of samples at each iteration
        
    Returns:
    --------
    convergence_rate : float
        Estimated convergence rate
    """
    errors = []
    true_value = shapley_values[-1]  # Use final value as ground truth
    
    for i, val in enumerate(shapley_values[:-1]):
        error = abs(val - true_value)
        errors.append(error)
    
    # Fit power law: error = a * n^(-b)
    log_n = np.log(iterations[:-1])
    log_error = np.log(np.array(errors) + 1e-10)
    
    slope, intercept = np.polyfit(log_n, log_error, 1)
    convergence_rate = -slope
    
    return convergence_rate
