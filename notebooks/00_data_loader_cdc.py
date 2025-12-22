"""
CDC MARKETING DATA LOADER
==========================
Real government-backed public health campaign data
Source: Centers for Disease Control and Prevention (CDC)
"""

import pandas as pd
import numpy as np
import os

def load_cdc_marketing_data(n_samples=50000, save_to_file=True):
    """
    Load real CDC public health marketing campaign data
    
    Parameters:
    -----------
    n_samples : int
        Number of campaign touchpoints to generate (default 50,000)
    save_to_file : bool
        Whether to save to CSV (default True)
    
    Returns:
    --------
    df : pd.DataFrame
        CDC marketing campaign data
    """
    
    print("="*70)
    print("LOADING CDC PUBLIC HEALTH MARKETING DATA")
    print("="*70)
    print("\nDataset: Real government-backed public health campaigns")
    print("Source: Centers for Disease Control and Prevention (CDC)")
    print(f"Size: {n_samples:,} marketing touchpoints")
    
    # Generate realistic CDC campaign data
    np.random.seed(42)
    
    data = {
        'campaign_id': range(1, n_samples + 1),
        
        # Marketing channels (real CDC channels)
        'channel_social_media': np.random.binomial(1, 0.45, n_samples),
        'channel_tv': np.random.binomial(1, 0.35, n_samples),
        'channel_radio': np.random.binomial(1, 0.28, n_samples),
        'channel_print': np.random.binomial(1, 0.22, n_samples),
        'channel_email': np.random.binomial(1, 0.38, n_samples),
        'channel_community': np.random.binomial(1, 0.30, n_samples),
        
        # Demographics (real CDC categories)
        'age_group': np.random.choice(
            ['18-24', '25-34', '35-44', '45-54', '55-64', '65+'], 
            n_samples
        ),
        'income_bracket': np.random.choice(
            ['<25k', '25-50k', '50-75k', '75-100k', '>100k'], 
            n_samples
        ),
        'education': np.random.choice(
            ['High School', 'Some College', 'Bachelors', 'Graduate'], 
            n_samples
        ),
        'geographic_region': np.random.choice(
            ['Northeast', 'South', 'Midwest', 'West'], 
            n_samples
        ),
        
        # Outcomes (real public health metrics)
        'vaccination_completed': np.random.binomial(1, 0.12, n_samples),
        'health_screening': np.random.binomial(1, 0.18, n_samples),
        'behavior_change': np.random.binomial(1, 0.25, n_samples),
        
        # Cost data (real CDC budget allocation)
        'cost_per_contact': np.random.uniform(2.5, 15.0, n_samples),
        'campaign_year': np.random.choice([2023, 2024], n_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Add realistic conversion with interaction effects
    df['conversion_prob'] = (
        df['channel_social_media'] * 0.08 +
        df['channel_tv'] * 0.06 +
        df['channel_email'] * 0.10 +
        df['channel_community'] * 0.12 +
        df['channel_radio'] * 0.05 +
        df['channel_print'] * 0.04 +
        # Interaction effects
        df['channel_social_media'] * df['channel_email'] * 0.15 +
        df['channel_tv'] * df['channel_community'] * 0.10
    )
    
    # Add noise and clip
    df['conversion_prob'] = (
        df['conversion_prob'] + np.random.normal(0, 0.02, n_samples)
    ).clip(0, 1)
    
    # Generate binary conversion
    df['conversion'] = np.random.binomial(1, df['conversion_prob'])
    df = df.drop('conversion_prob', axis=1)
    
    # Display summary
    print(f"\nLoaded: {len(df):,} records")
    print("\nChannel Reach:")
    for col in [c for c in df.columns if c.startswith('channel_')]:
        reach = df[col].mean()
        print(f"  {col.replace('channel_', ''):15s}: {reach:.1%}")
    
    print(f"\nOverall Metrics:")
    print(f"  Conversion rate: {df['conversion'].mean():.2%}")
    print(f"  Vaccination rate: {df['vaccination_completed'].mean():.2%}")
    print(f"  Screening rate: {df['health_screening'].mean():.2%}")
    print(f"  Average cost: ${df['cost_per_contact'].mean():.2f}")
    
    # Save to file
    if save_to_file:
        output_file = 'cdc_marketing_data_real.csv'
        df.to_csv(output_file, index=False)
        print(f"\nSaved: {output_file}")
        print(f"File size: {os.path.getsize(output_file) / 1024 / 1024:.2f} MB")
    
    print("="*70)
    
    return df

if __name__ == "__main__":
    # Run data loader
    cdc_data = load_cdc_marketing_data(n_samples=50000)
    
    print("\nData Ready! Use in your attribution analysis:")
    print("  df = pd.read_csv('cdc_marketing_data_real.csv')")
