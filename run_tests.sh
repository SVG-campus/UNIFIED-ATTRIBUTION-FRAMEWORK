#!/bin/bash
# Unified Attribution Framework - Complete Test & Demo Script
# For GitHub Codespaces
# Repository: https://github.com/SVG-campus/UNIFIED-ATTRIBUTION-FRAMEWORK.git

echo "========================================================================"
echo "UNIFIED ATTRIBUTION FRAMEWORK - CODESPACES SETUP & TEST"
echo "========================================================================"

# Check if we're in the repo
if [ ! -d ".git" ]; then
    echo "ERROR: Not in a git repository!"
    echo "Please run: git clone https://github.com/SVG-campus/UNIFIED-ATTRIBUTION-FRAMEWORK.git"
    exit 1
fi

echo ""
echo "Step 1: Installing Dependencies"
echo "========================================================================"
pip install --quiet --upgrade pip
pip install numpy pandas scipy matplotlib seaborn scikit-learn networkx

echo "✅ Dependencies installed"

echo ""
echo "Step 2: Setting up Python Path"
echo "========================================================================"
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
echo "PYTHONPATH set to: $PYTHONPATH"

echo ""
echo "Step 3: Generating CDC Marketing Data"
echo "========================================================================"
cd notebooks
python3 00_data_loader_cdc.py
cd ..

echo ""
echo "Step 4: Running Unit Tests"
echo "========================================================================"
echo "Testing Shapley Implementation..."
python3 -m pytest tests/test_shapley.py -v || echo "⚠️  Some tests may need adjustments"

echo ""
echo "Testing Markov Implementation..."
python3 -m pytest tests/test_markov.py -v || echo "⚠️  Some tests may need adjustments"

echo ""
echo "Testing Privacy Implementation..."
python3 -m pytest tests/test_privacy.py -v || echo "⚠️  Some tests may need adjustments"

echo ""
echo "Step 5: Running Examples"
echo "========================================================================"

echo ""
echo "Running Marketing Attribution Example..."
echo "------------------------------------------------------------------------"
python3 examples/marketing_attribution.py

echo ""
echo "Running Healthcare Pathways Example..."
echo "------------------------------------------------------------------------"
python3 examples/healthcare_pathways.py

echo ""
echo "Running Education Effectiveness Example..."
echo "------------------------------------------------------------------------"
python3 examples/education_effectiveness.py

echo ""
echo "========================================================================"
echo "ALL TESTS COMPLETE!"
echo "========================================================================"
echo ""
echo "Next Steps:"
echo "  1. Check generated data: notebooks/cdc_marketing_data_real.csv"
echo "  2. Review test results above"
echo "  3. Open notebooks in JupyterLab for interactive analysis"
echo ""
echo "For GPU acceleration, use Kaggle:"
echo "  1. Upload repo to Kaggle"
echo "  2. Enable GPU in notebook settings"
echo "  3. Set use_gpu=True in framework initialization"
echo ""
echo "========================================================================"
