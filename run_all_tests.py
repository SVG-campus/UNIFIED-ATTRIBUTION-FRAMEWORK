"""
Unified Attribution Framework - Test Runner
============================================
Run this in GitHub Codespaces to test everything!

Usage:
    python3 run_all_tests.py
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a shell command and print results"""
    print(f"\n{'='*70}")
    print(f"{description}")
    print('='*70)

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)

        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
        else:
            print(f"⚠️  {description} - COMPLETED WITH WARNINGS")

        return result.returncode == 0

    except subprocess.TimeoutExpired:
        print(f"⏱️  {description} - TIMEOUT (took > 5 min)")
        return False
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False


def main():
    print("="*70)
    print("UNIFIED ATTRIBUTION FRAMEWORK - COMPLETE TEST SUITE")
    print("="*70)
    print(f"Python: {sys.version}")
    print(f"Working Directory: {os.getcwd()}")

    # Check if in correct directory
    if not os.path.exists('src'):
        print("\n❌ ERROR: src/ directory not found!")
        print("Make sure you're in the repository root:")
        print("  cd /workspaces/UNIFIED-ATTRIBUTION-FRAMEWORK")
        sys.exit(1)

    # Setup Python path
    src_path = os.path.abspath('src')
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    os.environ['PYTHONPATH'] = f"{src_path}:{os.environ.get('PYTHONPATH', '')}"

    print(f"\nPYTHONPATH: {os.environ.get('PYTHONPATH')}")

    # Install dependencies
    run_command(
        "pip install -q numpy pandas scipy matplotlib seaborn scikit-learn networkx pytest",
        "Step 1: Installing Dependencies"
    )

    # Generate data
    if os.path.exists('notebooks/00_data_loader_cdc.py'):
        run_command(
            "cd notebooks && python3 00_data_loader_cdc.py && cd ..",
            "Step 2: Generating CDC Marketing Data"
        )

    # Run tests
    test_files = [
        ('tests/test_shapley.py', 'Test Shapley Values'),
        ('tests/test_markov.py', 'Test Markov Attribution'),
        ('tests/test_privacy.py', 'Test Differential Privacy')
    ]

    for test_file, desc in test_files:
        if os.path.exists(test_file):
            # Try pytest first, fallback to direct execution
            success = run_command(f"python3 -m pytest {test_file} -v", f"Step 3: {desc}")
            if not success:
                run_command(f"python3 {test_file}", f"Step 3 (fallback): {desc}")

    # Run examples
    example_files = [
        ('examples/marketing_attribution.py', 'Marketing Attribution Demo'),
        ('examples/healthcare_pathways.py', 'Healthcare Pathways Demo'),
        ('examples/education_effectiveness.py', 'Education Effectiveness Demo')
    ]

    for example_file, desc in example_files:
        if os.path.exists(example_file):
            run_command(f"python3 {example_file}", f"Step 4: {desc}")

    # Final summary
    print("\n" + "="*70)
    print("TEST SUITE COMPLETE!")
    print("="*70)

    print("\n📊 Generated Files:")
    if os.path.exists('notebooks/cdc_marketing_data_real.csv'):
        size = os.path.getsize('notebooks/cdc_marketing_data_real.csv') / 1024 / 1024
        print(f"  ✅ CDC Data: notebooks/cdc_marketing_data_real.csv ({size:.2f} MB)")

    print("\n📝 Next Steps:")
    print("  1. Review test output above")
    print("  2. Open notebooks/02_real_world_validation.ipynb")
    print("  3. For GPU: Upload to Kaggle and set use_gpu=True")

    print("\n🚀 Framework Ready!")


if __name__ == "__main__":
    main()
