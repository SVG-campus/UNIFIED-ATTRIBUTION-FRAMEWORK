"""Visualization utilities for attribution results"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def plot_attribution(results, method='hybrid', figsize=(10, 6)):
    """
    Plot attribution results for a single method
    
    Parameters:
    -----------
    results : dict
        Attribution results dictionary
    method : str
        Method to plot ('shapley', 'markov', 'hybrid', etc.)
    figsize : tuple
        Figure size
    """
    data = results[method]
    channels = list(data.keys())
    values = list(data.values())
    
    fig, ax = plt.subplots(figsize=figsize)
    ax.barh(channels, values, color='steelblue')
    ax.set_xlabel('Attribution Weight')
    ax.set_title(f'{method.upper()} Attribution')
    ax.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    
    return fig, ax

def plot_comparison(results, methods=None, figsize=(12, 6)):
    """
    Plot comparison of multiple attribution methods
    
    Parameters:
    -----------
    results : dict
        Attribution results dictionary
    methods : list
        List of methods to compare
    figsize : tuple
        Figure size
    """
    if methods is None:
        methods = ['shapley', 'markov', 'hybrid', 'causal']
    
    comparison_df = pd.DataFrame({
        m: results[m] for m in methods if m in results
    })
    
    fig, ax = plt.subplots(figsize=figsize)
    comparison_df.plot(kind='bar', ax=ax, rot=45)
    ax.set_ylabel('Attribution Weight')
    ax.set_title('Attribution Method Comparison')
    ax.legend(title='Method', bbox_to_anchor=(1.05, 1))
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    return fig, ax
