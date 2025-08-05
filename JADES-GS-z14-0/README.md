# JADES-GS-z14-0 Analysis: High-Redshift Galaxy Spectroscopy

## Overview

This repository contains analysis tools for processing and analyzing JWST (James Webb Space Telescope) JADES-GS-z14-0 spectroscopic data. The project focuses on extremely high-redshift galaxies (z ≈ 30-42) and implements a time delay model for cosmological interpretation.

## 🚀 Key Results

- **48 high-redshift galaxies** analyzed from JADES-GS-z14-0 dataset
- **Redshift range**: z ≈ 29.4 - 42.6 (among the most distant objects ever observed)
- **Distance range**: ~359,000 - 523,000 Mpc
- **Age range**: ~0.059 - 0.099 Gyr (very young universe at these redshifts)

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
    ├── generate_charts_from_fits.py  # Chart generation script
    ├── data/
    │   └── *.x1d.fits          # 1D extracted spectra (included in repo)
    ├── images/                  # Generated charts and plots
    │   ├── age_vs_z.png        # Age vs redshift comparison
    │   ├── avg_age_bar.png     # Average age comparison
    │   ├── delta_z_vs_distance.png # Redshift shift vs distance
    │   ├── sample_spectrum.png # Sample spectrum visualization
    │   └── jades_spectra_plot.png  # Complete spectra plot
    └── jades_results_table.csv  # Complete analysis results
```

## 🔬 Scientific Background

### JADES-GS-z14-0
The JADES (JWST Advanced Deep Extragalactic Survey) GS-z14-0 field targets extremely high-redshift galaxies to understand the early universe. This dataset contains some of the most distant galaxies ever observed.

### Time Delay Model
The analysis implements a cosmological model that accounts for time delays in light propagation, providing an alternative interpretation of high-redshift observations.

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/bahman2017/faidm.git
cd faidm
```

2. Navigate to the analysis folder:
```bash
cd jades_analysis
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 📊 Usage

### Basic Analysis
```bash
cd jades_analysis
python jades.py
```
- Lists all FITS files
- Displays file structure information
- Creates basic spectrum plots

### Advanced Analysis
```bash
cd jades_analysis
python jades_z14_analysis.py
```
- Performs comprehensive redshift analysis
- Calculates cosmological parameters
- Compares ΛCDM vs time delay model
- Generates results table and visualization

## 📈 Results Summary

### Model Comparison
- **Average observed redshift**: z ≈ 40.20
- **Average model redshift**: z ≈ 40.15
- **Average ΛCDM age**: ~0.07 Gyr
- **Average model age**: ~0.07 Gyr

### Key Findings
1. **Extremely high redshifts**: Galaxies at z > 40 challenge current cosmological models
2. **Time delay effects**: Model shows slight age differences due to propagation delays
3. **JWST capabilities**: Demonstrates JWST's ability to observe the earliest galaxies
4. **Data quality**: Excellent signal-to-noise for cosmological studies

## 🔧 Technical Details

### File Types Handled
- **x1d files**: 1D extracted spectra (EXTRACT1D extensions)
- **s2d files**: 2D spectral data (SCI extensions)
- **cal files**: Calibrated data (skipped for spectral analysis)

### Analysis Pipeline
1. **File detection**: Automatically identifies FITS file types
2. **Data extraction**: Handles different FITS structures appropriately
3. **Redshift calculation**: Uses Lyman-alpha line identification
4. **Cosmological calculations**: Implements Planck18 cosmology
5. **Model comparison**: Compares standard ΛCDM with time delay model

## 📊 Output Files

### jades_results_table.csv
Contains comprehensive analysis results:
- File names and types
- Observed vs model redshifts
- Distance calculations (Mpc)
- Time delays (seconds)
- Age comparisons (Gyr)

### images/ folder
Contains all generated visualizations:

**jades_spectra_plot.png**
- All analyzed spectra
- Redshift labels
- Wavelength vs flux plots
- Professional formatting for publications

**age_vs_z.png**
- Age vs redshift comparison
- ΛCDM vs Time Delay Model
- Scatter plot with clear model distinction

**avg_age_bar.png**
- Average age comparison
- Error bars showing statistical uncertainty
- Direct model comparison visualization

**delta_z_vs_distance.png**
- Redshift shift vs distance relationship
- Trend line analysis
- Distance correlation study

**sample_spectrum.png**
- High-quality sample spectrum
- Individual galaxy spectrum example
- Wavelength calibration demonstration

## 🎯 Scientific Applications

This analysis is useful for:
- **Cosmological studies**: Understanding the early universe
- **Galaxy evolution**: Studying the most distant galaxies
- **JWST data analysis**: Template for processing JWST spectroscopic data
- **Model testing**: Comparing different cosmological frameworks

## 📚 References

- JADES Collaboration (2024): JWST Advanced Deep Extragalactic Survey
- Planck Collaboration (2018): Planck 2018 results
- JWST Documentation: NIRSpec data processing

## 🤝 Contributing

Contributions are welcome! Please feel free to:
- Report issues
- Suggest improvements
- Add new analysis features
- Improve documentation

## 📄 License

This project is open source and available under the MIT License.
=======
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
>>>>>>> 37e7373ffe794dcec9927c01da1f4104b29e8cd1

## 👨‍💻 Author

**Bahman Masarratbakhsh**
- GitHub: [@bahman2017](https://github.com/bahman2017)
- Repository: [faidm](https://github.com/bahman2017/faidm.git)

---

*This analysis demonstrates the power of JWST for studying the most distant galaxies in the universe and provides tools for cosmological model testing.* 