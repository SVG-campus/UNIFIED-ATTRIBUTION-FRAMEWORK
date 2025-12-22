#!/bin/bash

echo "=========================================="
echo "UNIFIED ATTRIBUTION FRAMEWORK"
echo "Enhanced Test Suite with Relationship Discovery"
echo "=========================================="
echo ""

# Check Python version
python3 --version

echo ""
echo "Installing dependencies..."
pip install -q numpy scipy scikit-learn

echo ""
echo "Running enhanced test suite..."
python3 run_enhanced_tests.py

echo ""
echo "=========================================="
echo "RESULTS GENERATED"
echo "=========================================="
echo ""
echo "Check the following files for results:"
echo "  1. enhanced_test_report.json - Complete test results"
echo "  2. relationship_report.json - Cross-domain relationships"
echo ""
echo "To view results:"
echo "  cat enhanced_test_report.json | python3 -m json.tool"
echo "  cat relationship_report.json | python3 -m json.tool"
echo ""
