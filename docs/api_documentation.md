Unified Attribution Framework - API Documentation

Version: 1.0.0 | Last Updated: December 2025

============================================================================
TABLE OF CONTENTS
============================================================================

1. Installation
2. Core Classes
3. Attribution Methods
4. Visualization Tools
5. Metrics and Evaluation
6. Advanced Usage
7. Examples
8. Troubleshooting

============================================================================
1. INSTALLATION
============================================================================

Quick Install:
    pip install unified-attribution-framework

From Source:
    git clone https://github.com/username/unified-attribution-framework.git
    cd unified-attribution-framework
    pip install -e .

With GPU Support:
    pip install unified-attribution-framework[gpu]

============================================================================
2. CORE CLASSES
============================================================================

CompleteUnifiedFramework
------------------------
Main class for computing unified attribution across all methods.

Constructor:
    from unified_attribution import CompleteUnifiedFramework

    framework = CompleteUnifiedFramework(
        journeys: List[List[str]],
        data: pd.DataFrame,
        epsilon: float = 1.0,
        use_gpu: bool = False
    )

Parameters:
    - journeys: List of customer journeys (channel sequences)
    - data: Tabular data with binary channel columns
    - epsilon: Privacy budget (default 1.0)
    - use_gpu: Enable GPU acceleration (default False)

Methods:
    compute_complete_attribution()
        Compute all attribution methods
        Returns: (results dict, elapsed float)

Example:
    results, elapsed = framework.compute_complete_attribution()
    print(results['hybrid'])

============================================================================
3. ATTRIBUTION METHODS
============================================================================

FastShapleyAttribution
----------------------
Compute Shapley values using Monte Carlo sampling.

Usage:
    from src.core.shapley import FastShapleyAttribution

    shapley = FastShapleyAttribution(players, value_function)
    values, marginals = shapley.monte_carlo_shapley(n_samples=1000)

MarkovAttribution
-----------------
Compute attribution using Markov chain removal effects.

Usage:
    from src.core.markov import MarkovAttribution

    markov = MarkovAttribution(journeys, conversions)
    attribution = markov.compute_removal_effects()

HybridShapleyMarkov
-------------------
Novel hybrid method combining Shapley and Markov.

Usage:
    from src.core.hybrid import HybridShapleyMarkov

    hybrid = HybridShapleyMarkov(journeys, conversions)
    attribution = hybrid.compute_hybrid_attribution()

============================================================================
4. VISUALIZATION TOOLS
============================================================================

plot_attribution()
------------------
Plot single method attribution results.

    from src.utils.visualization import plot_attribution

    fig, ax = plot_attribution(results, method='hybrid')
    plt.show()

plot_comparison()
-----------------
Compare multiple attribution methods.

    from src.utils.visualization import plot_comparison

    fig, ax = plot_comparison(results, methods=['shapley', 'markov'])
    plt.show()

============================================================================
5. METRICS AND EVALUATION
============================================================================

compute_stability()
-------------------
Bootstrap stability analysis for attribution.

    from src.utils.metrics import compute_stability

    stability = compute_stability(attributions, n_bootstrap=100)

compute_convergence()
---------------------
Analyze convergence rate of algorithms.

    from src.utils.metrics import compute_convergence

    rate = compute_convergence(shapley_values, iterations)

============================================================================
6. ADVANCED USAGE
============================================================================

Custom Value Functions
----------------------
Define custom coalition value functions:

    def custom_value(coalition):
        base_value = len(coalition) * 0.1
        if 'Email' in coalition and 'Social' in coalition:
            base_value += 0.15
        return min(base_value, 1.0)

    shapley = FastShapleyAttribution(players, custom_value)
    values, _ = shapley.monte_carlo_shapley(n_samples=5000)

Privacy-Utility Tradeoff
------------------------
Adjust epsilon to balance privacy and utility:

    # High privacy (more noise)
    framework = CompleteUnifiedFramework(journeys, data, epsilon=0.1)

    # Moderate privacy
    framework = CompleteUnifiedFramework(journeys, data, epsilon=1.0)

    # Low privacy (less noise)
    framework = CompleteUnifiedFramework(journeys, data, epsilon=5.0)

GPU Acceleration
----------------
Enable GPU for large-scale computations:

    import torch
    print(f"GPU Available: {torch.cuda.is_available()}")

    framework = CompleteUnifiedFramework(
        journeys, data, epsilon=1.0, use_gpu=True
    )

============================================================================
7. EXAMPLES
============================================================================

Example 1: Basic Marketing Attribution
---------------------------------------
    import pandas as pd
    from unified_attribution import CompleteUnifiedFramework

    journeys = [
        ['Display', 'Search', 'Direct'],
        ['Social', 'Email', 'Direct'],
        ['Email', 'Direct']
    ]

    data = pd.DataFrame({
        'Display': [1, 0, 0],
        'Search': [1, 0, 0],
        'Social': [0, 1, 0],
        'Email': [0, 1, 1],
        'Direct': [1, 1, 1]
    })

    framework = CompleteUnifiedFramework(journeys, data)
    results, elapsed = framework.compute_complete_attribution()

    for channel, weight in results['hybrid'].items():
        print(f"{channel}: {weight:.4f}")

Example 2: Healthcare Pathways
-------------------------------
    treatments = [
        ['Primary_Care', 'Specialist', 'Treatment'],
        ['Emergency', 'Treatment'],
    ]

    framework = CompleteUnifiedFramework(treatments, data)
    results, _ = framework.compute_complete_attribution()

============================================================================
8. TROUBLESHOOTING
============================================================================

Issue: ImportError
Solution:
    pip install -e .
    export PYTHONPATH="${PYTHONPATH}:/path/to/src"

Issue: GPU Not Detected
Solution:
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
    python -c "import torch; print(torch.cuda.is_available())"

Issue: Memory Error
Solution:
    # Process in smaller batches
    batch_size = 5000
    results = batch_attribution(journeys, data, batch_size)

Issue: Slow Performance
Solutions:
    1. Enable GPU: use_gpu=True
    2. Reduce samples: n_samples=500
    3. Use parallel processing

Performance Benchmarks
----------------------
Dataset Size | CPU Time | GPU Time | Memory
1K samples   | 0.05s    | 0.02s    | 50MB
10K samples  | 0.3s     | 0.06s    | 200MB
100K samples | 2.5s     | 0.5s     | 2GB
1M samples   | 25s      | 2.5s     | 8GB

============================================================================
GETTING HELP
============================================================================

Documentation: https://github.com/username/unified-attribution-framework
Issues: https://github.com/username/unified-attribution-framework/issues
Email: your.email@example.com

============================================================================
CITATION
============================================================================

@article{unified_attribution_2025,
  title={Unified Attribution Framework: Combining Game Theory, 
         Causality, and Differential Privacy},
  author={Your Name},
  year={2025},
  url={https://github.com/username/unified-attribution-framework}
}

============================================================================
END OF DOCUMENTATION
============================================================================

For more examples, see notebooks/ directory.