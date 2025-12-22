"""
Unified Attribution Framework
==============================
Core attribution methods combining game theory, causality, and privacy
"""

__version__ = "1.0.0"
__author__ = "Your Name"

# Only import if modules exist
try:
    from .core.shapley import FastShapleyAttribution
    from .core.markov import MarkovAttribution
    from .core.hybrid import HybridAttribution
    from .core.privacy import PrivateAttribution

    __all__ = [
        'FastShapleyAttribution',
        'MarkovAttribution', 
        'HybridAttribution',
        'PrivateAttribution'
    ]
except ImportError as e:
    # Modules not yet added - this is OK during development
    __all__ = []
    pass