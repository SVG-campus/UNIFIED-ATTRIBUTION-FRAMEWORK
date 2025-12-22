"""
Enhanced Test Runner with Cross-Domain Analysis (FIXED)
Runs all tests and performs relationship discovery
"""

import sys
import time
import json
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import numpy as np

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from relationship_finder import RelationshipFinder, DomainPattern

# Import all test cases
from tests.test_mathematics import run_test as test_mathematics
from tests.test_marketing import run_test as test_marketing
from tests.test_physics_quantum import run_test as test_physics_quantum
from tests.test_physics_classical import run_test as test_physics_classical
from tests.test_economics import run_test as test_economics
from tests.test_art import run_test as test_art
from tests.test_psychology import run_test as test_psychology
from tests.test_biology import run_test as test_biology
from tests.test_chemistry import run_test as test_chemistry
from tests.test_medicine import run_test as test_medicine
from tests.test_linguistics import run_test as test_linguistics

def extract_attribution_vectors(results: Any) -> List[float]:
    """Extract numerical attribution vector from results"""
    vectors = []

    try:
        # Handle different result types
        if isinstance(results, dict):
            # Try to extract from nested structure
            for key, value in results.items():
                if isinstance(value, (int, float)) and not np.isnan(value) and np.isfinite(value):
                    vectors.append(float(value))
                elif isinstance(value, dict):
                    # Recurse into nested dicts
                    nested = extract_attribution_vectors(value)
                    vectors.extend(nested)
                elif isinstance(value, (list, tuple)):
                    for item in value:
                        if isinstance(item, (int, float)) and not np.isnan(item) and np.isfinite(item):
                            vectors.append(float(item))
        elif isinstance(results, (list, tuple)):
            for item in results:
                if isinstance(item, (int, float)) and not np.isnan(item) and np.isfinite(item):
                    vectors.append(float(item))
        elif isinstance(results, (int, float)) and not np.isnan(results) and np.isfinite(results):
            vectors.append(float(results))
    except Exception as e:
        print(f"  Warning: Could not extract vectors: {e}")

    # Return at least a zero vector if nothing found
    return vectors if vectors else [0.0]

def run_enhanced_tests():
    """Run all tests with enhanced relationship discovery"""

    print("=" * 70)
    print("UNIFIED ATTRIBUTION FRAMEWORK - ENHANCED TEST SUITE")
    print("=" * 70)
    print(f"Started: {datetime.now().isoformat()}")
    print()

    # Define test suite
    test_suite = [
        ("mathematics", test_mathematics),
        ("marketing_attribution", test_marketing),
        ("physics_quantum", test_physics_quantum),
        ("physics_classical", test_physics_classical),
        ("economics_macro", test_economics),
        ("art_aesthetics", test_art),
        ("psychology_cognition", test_psychology),
        ("biology_genetics", test_biology),
        ("chemistry_reactions", test_chemistry),
        ("medicine_clinical", test_medicine),
        ("linguistics_meaning", test_linguistics),
    ]

    results_log = []
    relationship_finder = RelationshipFinder()

    total_start = time.time()
    successes = 0
    failures = 0

    # Run each test
    for test_name, test_func in test_suite:
        print(f"Running: {test_name}...", end=" ", flush=True)
        test_start = time.time()

        try:
            test_result = test_func()
            test_duration = time.time() - test_start

            # Extract attribution patterns
            attribution_vector = extract_attribution_vectors(test_result)

            # Create domain pattern
            pattern = DomainPattern(
                domain=test_name,
                pattern_type="attribution_analysis",
                features={"test_duration": test_duration},
                attribution_vector=attribution_vector,
                metadata={
                    "timestamp": datetime.now().isoformat(),
                    "test_success": True
                }
            )
            relationship_finder.add_domain_pattern(pattern)

            results_log.append({
                "name": test_name,
                "success": True,
                "duration": round(test_duration, 4),
                "timestamp": datetime.now().isoformat(),
                "attribution_vector_length": len(attribution_vector),
                "sample_attributions": attribution_vector[:5] if len(attribution_vector) > 0 else [],
                "error": None
            })

            successes += 1
            print(f"✓ ({test_duration:.2f}s, {len(attribution_vector)} features)")

        except Exception as e:
            test_duration = time.time() - test_start
            error_msg = f"{type(e).__name__}: {str(e)}"

            results_log.append({
                "name": test_name,
                "success": False,
                "duration": round(test_duration, 4),
                "timestamp": datetime.now().isoformat(),
                "attribution_vector_length": 0,
                "sample_attributions": [],
                "error": error_msg
            })

            failures += 1
            print(f"✗ ({test_duration:.2f}s)")
            print(f"  Error: {error_msg}")

    total_duration = time.time() - total_start

    # Discover relationships
    print()
    print("=" * 70)
    print("DISCOVERING CROSS-DOMAIN RELATIONSHIPS...")
    print("=" * 70)

    relationship_start = time.time()
    relationships = relationship_finder.find_domain_similarities(threshold=0.3)
    relationship_report = relationship_finder.generate_report()
    relationship_duration = time.time() - relationship_start

    print(f"Found {len(relationships)} cross-domain relationships in {relationship_duration:.2f}s")
    print()

    # Display top relationships
    if relationship_report['strongest_relationships']:
        print("Top 5 Strongest Domain Relationships:")
        for i, rel in enumerate(relationship_report['strongest_relationships'][:5], 1):
            print(f"{i}. {rel['domain_a']} ↔ {rel['domain_b']}")
            print(f"   Similarity: {rel['similarity_score']:.3f}")
            print(f"   Shared patterns: {len(rel['shared_patterns'])}")
            print()
    else:
        print("Note: Limited relationships found. This may improve with more diverse attribution data.")
        print()

    # Create comprehensive report
    final_report = {
        "timestamp": datetime.now().isoformat(),
        "test_summary": {
            "total_tests": len(test_suite),
            "successes": successes,
            "failures": failures,
            "total_duration": round(total_duration, 4),
            "avg_duration": round(total_duration / len(test_suite), 4)
        },
        "test_results": results_log,
        "relationship_analysis": relationship_report,
        "performance_metrics": {
            "fastest_test": min(results_log, key=lambda x: x['duration'])['name'],
            "slowest_test": max(results_log, key=lambda x: x['duration'])['name'],
            "relationship_discovery_time": round(relationship_duration, 4)
        }
    }

    # Save reports
    output_dir = Path(__file__).parent
    enhanced_report_path = output_dir / "enhanced_test_report.json"
    relationship_report_path = output_dir / "relationship_report.json"

    with open(enhanced_report_path, "w") as f:
        json.dump(final_report, f, indent=2)

    with open(relationship_report_path, "w") as f:
        json.dump(relationship_report, f, indent=2)

    # Print summary
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Total Tests: {len(test_suite)}")
    print(f"Successes: {successes}")
    print(f"Failures: {failures}")
    print(f"Total Duration: {total_duration:.2f}s")
    print(f"Relationships Found: {len(relationships)}")
    print()
    print("✓ Reports saved to:")
    print(f"  → {enhanced_report_path.absolute()}")
    print(f"  → {relationship_report_path.absolute()}")
    print()
    print("=" * 70)
    print("HOW TO DOWNLOAD THESE FILES:")
    print("=" * 70)
    print("1. In VS Code (Codespaces), right-click on the file in Explorer")
    print("2. Select 'Download...'")
    print()
    print("OR use terminal:")
    print("  cat enhanced_test_report.json")
    print("  cat relationship_report.json")
    print()

    return final_report

if __name__ == "__main__":
    try:
        report = run_enhanced_tests()
        sys.exit(0 if report['test_summary']['failures'] == 0 else 1)
    except Exception as e:
        print(f"\nFatal error: {e}")
        traceback.print_exc()
        sys.exit(1)
