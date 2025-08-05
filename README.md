# FAIDM: JADES-GS-z14-0 Analysis Repository

## Overview

This repository contains comprehensive analysis tools and results for JWST (James Webb Space Telescope) JADES-GS-z14-0 spectroscopic data, focusing on extremely high-redshift galaxies and implementing a time delay cosmological model.

## 📁 Repository Structure

```
faidm/
├── README.md                    # This file
├── .gitignore                   # Git ignore rules
└── jades_analysis/              # Main analysis folder
    ├── README.md                # Detailed documentation
    ├── requirements.txt         # Python dependencies
    ├── jades.py                 # Basic FITS file analysis
    ├── jades_z14_analysis.py    # Advanced analysis with model comparison
    ├── setup_github.sh          # Automated setup script
    ├── jades_results_table.csv  # Complete analysis results
    └── jades_spectra_plot.png   # High-resolution visualization
```

## 🚀 Quick Start

1. **Navigate to the analysis folder:**
   ```bash
   cd jades_analysis
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the analysis:**
   ```bash
   python jades_z14_analysis.py
   ```

## 🔬 Key Results

- **54 high-redshift galaxies** analyzed from JADES-GS-z14-0 dataset
- **Redshift range**: z ≈ 29.4 - 42.6 (among the most distant objects ever observed)
- **Distance range**: ~359,000 - 523,000 Mpc
- **Time delay model** implementation for cosmological interpretation

## 📊 Scientific Highlights

- **Extremely high redshifts**: Galaxies at z > 40 challenge current cosmological models
- **JWST capabilities**: Demonstrates JWST's ability to observe the earliest galaxies
- **Model comparison**: Compares standard ΛCDM with time delay framework
- **Publication-ready**: High-quality visualizations and data tables

## 📚 Documentation

For detailed documentation, scientific background, and usage instructions, see:
**[jades_analysis/README.md](jades_analysis/README.md)**

## 👨‍💻 Author

**Bahman Masarratbakhsh**
- GitHub: [@bahman2017](https://github.com/bahman2017)
- Repository: [faidm](https://github.com/bahman2017/faidm.git)

---

*This analysis demonstrates the power of JWST for studying the most distant galaxies in the universe and provides tools for cosmological model testing.* 