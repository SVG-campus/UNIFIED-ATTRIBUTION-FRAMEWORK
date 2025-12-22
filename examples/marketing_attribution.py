"""
Marketing Attribution Example
==============================
Multi-touch attribution across digital channels
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Import framework (adjust path as needed)
# from unified_attribution import CompleteUnifiedFramework


def generate_marketing_data(n_customers=1000):
    """Generate synthetic marketing data"""

    np.random.seed(42)

    # Channels
    channels = ['Display', 'Search', 'Social', 'Email', 'Video', 'Affiliate']

    # Generate customer interactions
    data = pd.DataFrame({
        'Display': np.random.binomial(1, 0.25, n_customers),
        'Search': np.random.binomial(1, 0.40, n_customers),
        'Social': np.random.binomial(1, 0.30, n_customers),
        'Email': np.random.binomial(1, 0.35, n_customers),
        'Video': np.random.binomial(1, 0.15, n_customers),
        'Affiliate': np.random.binomial(1, 0.20, n_customers),
    })

    # Generate conversions with interaction effects
    conversion_prob = (
        data['Display'] * 0.05 +
        data['Search'] * 0.15 +
        data['Social'] * 0.08 +
        data['Email'] * 0.12 +
        data['Video'] * 0.06 +
        data['Affiliate'] * 0.10 +
        # Interaction effects
        data['Search'] * data['Email'] * 0.10 +
        data['Social'] * data['Video'] * 0.08
    )

    data['Conversion'] = np.random.binomial(
        1, np.clip(conversion_prob, 0, 1)
    )

    # Create customer journeys
    journeys = []
    for idx, row in data[channels].iterrows():
        journey = [ch for ch in channels if row[ch] == 1]
        journeys.append(journey if journey else ['Direct'])

    return data, journeys


def run_marketing_attribution():
    """Run complete marketing attribution analysis"""

    print("="*70)
    print("MARKETING ATTRIBUTION ANALYSIS")
    print("="*70)

    # Generate data
    print("\nGenerating marketing data...")
    data, journeys = generate_marketing_data(n_customers=5000)

    print(f"Customers: {len(data):,}")
    print(f"Conversion rate: {data['Conversion'].mean():.2%}")

    # Channel statistics
    print("\nChannel Touchpoints:")
    channels = [c for c in data.columns if c != 'Conversion']
    for channel in channels:
        touchpoints = data[channel].sum()
        rate = data[channel].mean()
        print(f"  {channel:12s}: {touchpoints:4d} ({rate:.1%})")

    # Simulate attribution (replace with actual framework call)
    print("\n" + "="*70)
    print("COMPUTING ATTRIBUTION")
    print("="*70)

    # Mock results - replace with actual computation
    attribution = {
        'Search': 0.285,
        'Email': 0.225,
        'Social': 0.180,
        'Display': 0.120,
        'Affiliate': 0.110,
        'Video': 0.080
    }

    print("\nAttribution Results (Hybrid Shapley-Markov):")
    print("-"*70)
    for channel, weight in sorted(attribution.items(), 
                                  key=lambda x: x[1], reverse=True):
        print(f"  {channel:12s}: {weight:.4f} ({weight*100:.2f}%)")

    # ROI Analysis
    print("\n" + "="*70)
    print("ROI ANALYSIS")
    print("="*70)

    # Mock cost data
    costs = {
        'Display': 15000,
        'Search': 25000,
        'Social': 12000,
        'Email': 8000,
        'Video': 20000,
        'Affiliate': 10000
    }

    total_conversions = data['Conversion'].sum()
    total_cost = sum(costs.values())

    print(f"\nTotal Conversions: {total_conversions:,}")
    print(f"Total Marketing Spend: ${total_cost:,}")
    print(f"Overall CPA: ${total_cost/total_conversions:.2f}")

    print("\nChannel ROI:")
    print("-"*70)
    for channel in attribution.keys():
        attributed_conv = attribution[channel] * total_conversions
        channel_cost = costs[channel]
        roi = (attributed_conv / channel_cost) * 1000  # per $1000
        cpa = channel_cost / attributed_conv if attributed_conv > 0 else 0

        print(f"  {channel:12s}: ${channel_cost:6,} -> "
              f"{attributed_conv:5.0f} conv | "
              f"CPA: ${cpa:6.2f} | ROI: {roi:.2f}/k")

    # Budget recommendations
    print("\n" + "="*70)
    print("BUDGET RECOMMENDATIONS")
    print("="*70)

    print("\nRecommended Reallocation:")
    print("-"*70)
    optimal_budget = {ch: attr * total_cost for ch, attr in attribution.items()}

    for channel in attribution.keys():
        current = costs[channel]
        optimal = optimal_budget[channel]
        change = optimal - current
        change_pct = (change / current) * 100

        if abs(change_pct) > 10:
            action = "INCREASE" if change > 0 else "DECREASE"
            print(f"  {channel:12s}: {action:8s} by ${abs(change):6,.0f} "
                  f"({change_pct:+.1f}%)")

    return attribution, data


if __name__ == "__main__":
    attribution, data = run_marketing_attribution()

    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)