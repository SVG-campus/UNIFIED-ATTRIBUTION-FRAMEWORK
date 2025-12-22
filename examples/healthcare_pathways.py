"""
Healthcare Pathways Attribution
================================
Analyze treatment pathway effectiveness
"""

import numpy as np
import pandas as pd
from collections import Counter


def generate_healthcare_data(n_patients=500):
    """Generate synthetic healthcare pathway data"""

    np.random.seed(42)

    # Treatment types
    treatments = [
        'Primary_Care',
        'Emergency_Room',
        'Specialist_Consultation',
        'Diagnostic_Testing',
        'Physical_Therapy',
        'Medication',
        'Surgery',
        'Follow_Up'
    ]

    # Generate patient pathways
    pathways = []
    outcomes = []

    for _ in range(n_patients):
        # Random pathway length
        pathway_length = np.random.randint(2, 6)

        # Generate pathway
        pathway = []

        # Most start with Primary Care or Emergency
        if np.random.random() < 0.7:
            pathway.append('Primary_Care')
        else:
            pathway.append('Emergency_Room')

        # Add subsequent treatments
        available = [t for t in treatments if t not in pathway]
        for _ in range(pathway_length - 1):
            if available:
                next_treatment = np.random.choice(available)
                pathway.append(next_treatment)
                available.remove(next_treatment)

        pathways.append(pathway)

        # Outcome based on pathway
        # More treatments generally better outcomes
        outcome_prob = 0.5 + (len(pathway) * 0.08)

        # Boost for specific treatments
        if 'Specialist_Consultation' in pathway:
            outcome_prob += 0.15
        if 'Follow_Up' in pathway:
            outcome_prob += 0.10

        outcome = 1 if np.random.random() < np.clip(outcome_prob, 0, 1) else 0
        outcomes.append(outcome)

    # Create dataframe
    data = pd.DataFrame(0, index=range(n_patients), columns=treatments)
    for i, pathway in enumerate(pathways):
        for treatment in pathway:
            data.loc[i, treatment] = 1

    data['Positive_Outcome'] = outcomes

    return data, pathways, outcomes


def analyze_healthcare_pathways():
    """Analyze healthcare treatment pathways"""

    print("="*70)
    print("HEALTHCARE PATHWAY ATTRIBUTION")
    print("="*70)

    # Generate data
    print("\nGenerating patient pathway data...")
    data, pathways, outcomes = generate_healthcare_data(n_patients=1000)

    print(f"Patients: {len(data):,}")
    print(f"Positive outcome rate: {np.mean(outcomes):.2%}")

    # Treatment statistics
    print("\nTreatment Frequency:")
    treatments = [c for c in data.columns if c != 'Positive_Outcome']
    for treatment in treatments:
        count = data[treatment].sum()
        rate = data[treatment].mean()
        print(f"  {treatment:25s}: {count:4d} ({rate:.1%})")

    # Pathway analysis
    print("\n" + "="*70)
    print("PATHWAY PATTERNS")
    print("="*70)

    pathway_strings = [' -> '.join(p) for p in pathways]
    pathway_counter = Counter(pathway_strings)

    print("\nMost Common Pathways:")
    for pathway, count in pathway_counter.most_common(5):
        print(f"  {count:3d}x: {pathway}")

    # Treatment attribution (simplified)
    print("\n" + "="*70)
    print("TREATMENT ATTRIBUTION")
    print("="*70)

    # Calculate impact of each treatment
    attribution = {}
    for treatment in treatments:
        # Patients with this treatment
        with_treatment = data[data[treatment] == 1]['Positive_Outcome']
        without_treatment = data[data[treatment] == 0]['Positive_Outcome']

        if len(with_treatment) > 0 and len(without_treatment) > 0:
            impact = with_treatment.mean() - without_treatment.mean()
            attribution[treatment] = max(0, impact)
        else:
            attribution[treatment] = 0.0

    # Normalize
    total = sum(attribution.values())
    if total > 0:
        attribution = {t: v/total for t, v in attribution.items()}

    print("\nTreatment Impact (Normalized):")
    print("-"*70)
    for treatment, impact in sorted(attribution.items(), 
                                    key=lambda x: x[1], reverse=True):
        print(f"  {treatment:25s}: {impact:.4f} ({impact*100:.2f}%)")

    # Outcome by pathway length
    print("\n" + "="*70)
    print("OUTCOME BY PATHWAY COMPLEXITY")
    print("="*70)

    pathway_lengths = [len(p) for p in pathways]
    outcome_by_length = {}

    for length in range(2, 7):
        indices = [i for i, l in enumerate(pathway_lengths) if l == length]
        if indices:
            outcome_rate = np.mean([outcomes[i] for i in indices])
            outcome_by_length[length] = outcome_rate

    print("\nOutcome Rate by # of Treatments:")
    for length, rate in sorted(outcome_by_length.items()):
        print(f"  {length} treatments: {rate:.1%}")

    # Key findings
    print("\n" + "="*70)
    print("KEY FINDINGS")
    print("="*70)

    top_treatment = max(attribution.items(), key=lambda x: x[1])[0]
    avg_pathway_length = np.mean(pathway_lengths)

    print(f"\n1. Most impactful treatment: {top_treatment}")
    print(f"2. Average pathway length: {avg_pathway_length:.1f} treatments")
    print(f"3. Overall success rate: {np.mean(outcomes):.1%}")
    print(f"4. Patients with Follow-Up: "
          f"{data['Follow_Up'].mean():.1%} (recommend increasing)")

    return attribution, data, pathways


if __name__ == "__main__":
    attribution, data, pathways = analyze_healthcare_pathways()

    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)