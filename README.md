# afs GbindView

A user-friendly Streamlit app for visualizing and comparing MMGBSA (Molecular Mechanics Generalized Born Surface Area) binding free energy trajectories from Schrödinger Prime outputs.

## Features

- **Upload and visualize** one or multiple MMGBSA CSV files.
- **Comparison mode**: Compare multiple ligands side-by-side with per-ligand color and style customization.
- **Customizable plots**: Per-ligand color and style, running mean, error bars, and more.
- **Download**: Publication-quality PNG plots and statistics (TXT, CSV).
- **Session state**: Settings persist during your session.
- **Reset**: One-click reset to default settings.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/afs-gbindview.git
   cd afs-gbindview
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the app:
   ```bash
   streamlit run mmgbsa_ui_v2.py
   ```

2. Open your browser to the provided local URL.

3. Upload your `thermal_MMGBSA.csv` files and explore the visualization and analysis options.

## Example Data

You can find example MMGBSA CSV files in the `examples/` folder (add your own or request sample data).

## Screenshots

Add screenshots to a `screenshots/` folder and reference them here, e.g.:

![Comparison Mode Example](screenshots/comparison_mode.png)

## Citation

If you use afs GbindView in your research, please cite this repository.

## License

MIT License

---

## Acknowledgements

- Built with [Streamlit](https://streamlit.io/)
- Inspired by Schrödinger Prime MMGBSA workflows 