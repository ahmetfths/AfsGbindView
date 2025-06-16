# AfsGbindView - MM-GBSA Trajectory Viewer

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A powerful, interactive web application for visualizing and analyzing Molecular Mechanics Generalized Born Surface Area (MM-GBSA) binding energy trajectories from molecular dynamics simulations.

## 🎯 Features

### Core Functionality
- **Interactive Visualization**: Upload Schrödinger `thermal_MMGBSA.csv` files and instantly visualize ΔGbind vs time
- **Automatic Ligand Detection**: Extracts ligand names from CSV files and auto-populates plot titles
- **Running Mean Analysis**: Customizable sliding window for smoothed trajectory analysis
- **Multiple Export Formats**: Download plots as PNG and statistics as CSV/TXT

### Advanced Visualization Options
- **Customizable Plot Elements**:
  - Editable plot title, axis labels, and legend positioning
  - Color pickers for frame lines and running mean traces
  - Line style options (solid, dashed, dotted, dash-dot)
  - Adjustable line widths and transparency
- **Error Analysis**:
  - Standard Error, Standard Deviation, or 95% Confidence Intervals
  - Customizable error bar transparency
- **Show/Hide Controls**: Toggle individual frames and running mean visibility

### Multi-Ligand Comparison Mode
- **Side-by-side Analysis**: Compare up to 6 ligands simultaneously
- **Per-ligand Customization**: Individual color and style settings for each ligand
- **Professional Color Palette**: Automatically assigned distinct colors
- **Comparison Statistics**: Comprehensive statistical comparison table

### User Experience
- **Persistent Settings**: All customizations saved during session
- **Reset Functionality**: One-click return to default settings
- **Responsive Design**: Optimized for different screen sizes
- **Real-time Updates**: Instant plot updates as settings change

## 🚀 Quick Start

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/AfsGbindView.git
cd AfsGbindView
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the application**:
```bash
streamlit run mmgbsa_ui_v2.py
```

4. **Open in browser**: The app will automatically open at `http://localhost:8501`

### Docker Installation (Optional)

```bash
# Build the image
docker build -t afsgbindview .

# Run the container
docker run -p 8501:8501 afsgbindview
```

## 📊 Usage Guide

### Single Ligand Analysis

1. **Upload Data**: Drag and drop your `thermal_MMGBSA.csv` file
2. **Set Time Range**: Enter the total MD simulation time in nanoseconds
3. **Customize Visualization**:
   - Adjust running mean window size (1-50 frames)
   - Choose colors and line styles
   - Toggle error bars and select error type
4. **Download Results**: Export plots and statistics

### Multi-Ligand Comparison

1. **Enable Comparison Mode**: Check "Comparison Mode" in the sidebar
2. **Upload Multiple Files**: Select up to 6 CSV files for comparison
3. **Customize Each Ligand**: Expand individual ligand settings for personalization
4. **Analyze Results**: View side-by-side comparison with statistical summary

### File Format Requirements

Your CSV file should contain:
- Column `r_psp_MMGBSA_dG_Bind`: Binding energy values (kcal/mol)
- Column `title`: Ligand identifier (optional, used for auto-naming)

Example CSV structure:
```csv
title,r_psp_MMGBSA_dG_Bind,frame
"MyLigand_1",-45.23,1
"MyLigand_1",-44.87,2
"MyLigand_1",-46.12,3
...
```

## 🛠️ Configuration Options

### Plot Customization
- **Title & Labels**: Fully editable plot title and axis labels
- **Colors**: Color pickers for all plot elements
- **Styles**: Line styles (solid, dashed, dotted, dash-dot)
- **Transparency**: Adjustable alpha values for overlays
- **Legend**: Configurable position and labels

### Analysis Parameters
- **Window Size**: Running mean calculation window (1-50 frames)
- **Error Types**: Standard Error, Standard Deviation, 95% CI
- **Visibility**: Toggle individual elements on/off

### Export Options
- **PNG**: High-resolution plot images (300 DPI)
- **CSV**: Statistical summaries with raw numerical data
- **TXT**: Human-readable statistics reports

## 📈 Examples

### Example 1: Basic Single Ligand Analysis
```python
# Upload file: ligand_A_mmgbsa.csv
# Set MD time: 100 ns
# Result: Automatic title "ΔGbind vs Time (ns) - ligand_A"
```

### Example 2: Multi-Ligand Comparison
```python
# Upload files: compound_1.csv, compound_2.csv, compound_3.csv
# Enable comparison mode
# Result: Overlay plot with distinct colors and statistical comparison
```

### Example 3: Publication-Ready Plot
```python
# Customize colors to journal requirements
# Add error bars (95% CI)
# Export high-resolution PNG
# Download statistics as CSV for supplementary data
```

## 🔧 Technical Details

### Dependencies
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Matplotlib**: Plotting and visualization
- **NumPy**: Numerical computations
- **SciPy**: Statistical functions

### System Requirements
- Python 3.7 or higher
- 2GB RAM minimum (4GB recommended for large datasets)
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Performance Notes
- Optimized for datasets up to 10,000 frames per ligand
- Real-time plot updates with minimal latency
- Efficient memory usage for multiple ligand comparisons

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/AfsGbindView.git

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Start development server
streamlit run mmgbsa_ui_v2.py --server.runOnSave true
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Schrödinger Suite for MM-GBSA methodology and output format
- Streamlit team for the excellent web framework
- Scientific Python ecosystem (NumPy, Pandas, Matplotlib, SciPy)

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/AfsGbindView/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/AfsGbindView/discussions)
- **Email**: your.email@domain.com

## 🔄 Version History

### v2.0.0 (Current)
- Multi-ligand comparison mode
- Enhanced customization options
- Automatic ligand detection and naming
- Error bar analysis
- Professional color palette

### v1.0.0
- Basic single ligand visualization
- Running mean calculation
- PNG/TXT export functionality

---

**Made with ❤️ for the computational chemistry community** 