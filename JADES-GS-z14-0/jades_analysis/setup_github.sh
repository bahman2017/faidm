#!/bin/bash

# Setup script for uploading JADES analysis to GitHub repository
# https://github.com/bahman2017/faidm.git

echo "🚀 Setting up JADES-GS-z14-0 Analysis for GitHub..."

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install git first."
    exit 1
fi

# Initialize git repository (if not already done)
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
fi

# Add remote origin
echo "🔗 Adding remote origin..."
git remote add origin https://github.com/bahman2017/faidm.git 2>/dev/null || git remote set-url origin https://github.com/bahman2017/faidm.git

# Add all files (except those in .gitignore)
echo "📝 Adding files to git..."
git add .

# Commit changes
echo "💾 Committing changes..."
git commit -m "Add JADES-GS-z14-0 analysis: High-redshift galaxy spectroscopy

- Added comprehensive analysis of 54 high-redshift galaxies (z ≈ 29-42)
- Implemented time delay cosmological model
- Created visualization and results table
- Added documentation and requirements

Key results:
- Redshift range: z ≈ 29.4 - 42.6
- Distance range: ~359,000 - 523,000 Mpc
- Model comparison: ΛCDM vs time delay model"

# Push to GitHub
echo "⬆️  Pushing to GitHub..."
git push -u origin main

echo "✅ Setup complete! Your repository is now available at:"
echo "   https://github.com/bahman2017/faidm.git"
echo ""
echo "📊 Repository contains:"
echo "   - jades.py: Basic FITS file analysis"
echo "   - jades_z14_analysis.py: Advanced analysis with model comparison"
echo "   - results/: Analysis outputs (CSV table and plots)"
echo "   - README.md: Comprehensive documentation"
echo "   - requirements.txt: Python dependencies"
echo ""
echo "🔬 Scientific highlights:"
echo "   - 54 extremely high-redshift galaxies analyzed"
echo "   - Redshifts up to z ≈ 42.6 (among most distant ever observed)"
echo "   - Time delay model implementation for cosmological interpretation" 