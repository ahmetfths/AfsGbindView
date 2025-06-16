# Changelog

All notable changes to AfsGbindView will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2024-03-19

### Added
- **Multi-ligand Comparison Mode**: Compare up to 6 ligands simultaneously
- **Automatic Ligand Detection**: Extract ligand names from CSV title column
- **Enhanced Customization Options**:
  - Color pickers for all plot elements
  - Line style selection (solid, dashed, dotted, dash-dot)
  - Adjustable line widths and transparency
  - Editable plot titles and axis labels
- **Error Bar Analysis**: 
  - Standard Error calculation
  - Standard Deviation visualization
  - 95% Confidence Intervals
  - Customizable error bar transparency
- **Professional Color Palette**: Automatic color assignment for comparison mode
- **Per-ligand Settings**: Individual customization for each ligand in comparison mode
- **Session State Management**: Persistent settings during application session
- **Reset Functionality**: One-click return to default settings
- **Enhanced Export Options**:
  - High-resolution PNG plots (300 DPI)
  - CSV export for statistical data
  - Improved TXT statistics format
- **Improved User Interface**:
  - Organized sidebar with collapsible sections
  - Better error handling and user feedback
  - Responsive design improvements
- **Font Compatibility**: Linux-compatible font selection (DejaVu Sans)
- **Docker Support**: Containerization for easy deployment

### Changed
- **Plot Title Behavior**: Automatic population with ligand name, still fully editable
- **Legend Labels**: Standardized to "ΔGbind / frame" and "X - running mean" format
- **Default Line Widths**: Increased for better visibility (frame: 2.0, mean: 3.5)
- **File Upload Logic**: Improved handling and error detection
- **Code Structure**: Better organization and documentation

### Fixed
- **File Reading Issues**: Resolved pointer problems in comparison mode
- **Numpy Warnings**: Proper handling of small window sizes in error calculations
- **Session State Bugs**: Improved state management and persistence
- **Legend Positioning**: Fixed customization and positioning issues
- **CSV Export Formatting**: Consistent numerical data output
- **Table Indexing**: Start at 1 instead of 0 for better user experience

### Technical Improvements
- Enhanced error handling throughout the application
- Improved performance for large datasets
- Better memory management in comparison mode
- More robust file parsing and validation
- Comprehensive documentation and code comments

## [1.0.0] - 2024-03-01

### Added
- **Initial Release**: Basic MM-GBSA trajectory visualization
- **Core Features**:
  - Single ligand CSV file upload
  - ΔGbind vs time plotting
  - Running mean calculation with fixed window size
  - Basic customization options
- **Export Functionality**:
  - PNG plot export
  - TXT statistics export
- **Basic UI**:
  - Streamlit-based web interface
  - Simple file upload mechanism
  - Basic color and style options

### Features
- Upload Schrödinger `thermal_MMGBSA.csv` files
- Interactive plot generation
- Running mean with 10-frame window
- Basic statistics calculation (mean, std, min, max)
- Simple export options

---

## Future Roadmap

### [2.1.0] - Planned
- **Interactive Plotly Backend**: Optional plotly integration for enhanced interactivity
- **Data Filtering**: Time range selection and frame filtering
- **Advanced Statistics**: Additional statistical measures and tests
- **Batch Processing**: Support for processing multiple files at once
- **Custom Color Palettes**: User-defined color schemes

### [3.0.0] - Future
- **Multiple File Formats**: Support for additional input formats
- **Advanced Analysis Tools**: Convergence analysis, binding kinetics
- **Machine Learning Integration**: Predictive modeling features
- **API Development**: RESTful API for programmatic access
- **Database Integration**: Store and retrieve analysis results

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for information on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 