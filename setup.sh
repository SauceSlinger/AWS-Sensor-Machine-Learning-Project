#!/bin/bash

# Quick Setup Script for Local Development
# Run this script to set up the complete local environment

echo "🚀 Setting up AWS Sensor ML Project..."
echo ""

# Step 1: Create virtual environment
echo "📦 Step 1/4: Creating Python virtual environment..."
python3 -m venv .venv
echo "✓ Virtual environment created"

# Step 2: Activate and install dependencies
echo ""
echo "📥 Step 2/4: Installing dependencies..."
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Dependencies installed (pandas, scikit-learn)"

# Step 3: Generate training data
echo ""
echo "📊 Step 3/4: Generating training data..."
python generate_logs.py
echo "✓ Training data generated"

# Step 4: Train ML model
echo ""
echo "🤖 Step 4/4: Training ML model..."
python train_model.py
echo "✓ ML model trained and serialized"

echo ""
echo "✅ Setup complete! Your project is ready."
echo ""
echo "📝 Next steps:"
echo "   1. Open index.html in a browser to see the dashboard"
echo "   2. Review DEPLOYMENT.md for AWS Lambda deployment instructions"
echo "   3. Initialize git and commit to repository"
echo ""
echo "🔧 To activate virtual environment later:"
echo "   source .venv/bin/activate"
echo ""
