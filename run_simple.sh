#!/bin/bash

echo "=========================================="
echo "UNIFIED ATTRIBUTION FRAMEWORK"
echo "Enhanced Analysis Runner"
echo "=========================================="
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -q numpy scipy scikit-learn

echo ""
echo "Running analysis..."
python3 run_simple_enhanced.py

echo ""
echo "Done!"
