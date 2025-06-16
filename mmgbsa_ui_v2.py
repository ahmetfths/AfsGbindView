# -*- coding: utf-8 -*-
"""
MM‑GBSA CSV quick‑look app (Streamlit)
=====================================
Upload Schrödinger `thermal_MMGBSA.csv`, enter total MD length (ns).
The app plots ΔGbind vs. time, shows running mean, and lets you download
  • a PNG of the graph (per‑frame line = **orange**, running mean = **dark‑red**)
  • a TXT file with mean / SD / range values
**New features**
  • User‑editable plot title (defaults to "ΔGbind vs Time — <LigID>") after ligand ID is parsed.
  • Customizable running mean window size
  • Option to show/hide individual frames and running mean
  • Customizable plot colors and styles
  • Error bars and confidence intervals
  • Reset settings to defaults
  • Multiple ligand comparison
Each file is named automatically with the ligand ID.
"""

import io
import re
from pathlib import Path
import numpy as np
from scipy import stats

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import matplotlib as mpl

# ------------------------
# Default settings
# ------------------------
DEFAULT_SETTINGS = {
    "window_size": 10,
    "show_frames": True,
    "show_running_mean": True,
    "show_error_bars": False,
    "error_type": "Standard Error",
    "error_alpha": 0.3,
    "frame_color": "#FFA500",  # Orange
    "frame_alpha": 0.7,
    "frame_style": "solid",
    "running_mean_color": "#8B0000",  # Darkred
    "running_mean_width": 2.0,
    "running_mean_style": "solid",
    "comparison_mode": False,
    "max_ligands": 4,
    "plot_title": "ΔGbind vs Time (ns)",
    "x_label": "Time (ns)",
    "y_label": "ΔGbind (kcal/mol)",
    "legend_position": "best",
    "frame_legend_label": "Frame",
    "mean_legend_label": "Mean"
}

# Color palette for comparison mode
COLOR_PALETTE = [
    '#4E79A7', '#F28E2B', '#E15759', '#76B7B2', '#59A14F', '#EDC948',
    '#B07AA1', '#FF9DA7', '#9C755F', '#BAB0AC'
]

# ------------------------
# Matplotlib global style
# ------------------------
plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.titleweight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"

# ------------------------
# Helper functions
# ------------------------

def generate_random_color():
    """Generate a random color in hex format."""
    return f"#{np.random.randint(0, 16777215):06x}"

def parse_ligand_id(title: str) -> str:
    """Return the entire title as the ligand ID."""
    return title if title else "Ligand"


def compute_stats(series: pd.Series):
    series = series.astype(float)
    return {
        "frames": int(series.count()),
        "mean": series.mean(),
        "stdev": series.std(),
        "minimum": series.min(),
        "maximum": series.max(),
    }


def calculate_confidence_interval(data, confidence=0.95):
    """Calculate confidence interval for a series of data."""
    mean = np.mean(data)
    std_err = stats.sem(data)
    ci = stats.t.interval(confidence, len(data)-1, loc=mean, scale=std_err)
    return mean, ci[0], ci[1]


def plot_ligand_data(ax, time_ns, dg, running, settings, ligand_id, show_error_bars=False, yerr=None, ci_lower=None, ci_upper=None, color=None, frame_color=None, frame_style=None, running_style=None, show_frames=True, running_mean_width=None):
    """Helper function to plot a single ligand's data."""
    frame_color = frame_color or settings['frame_color']
    running_color = color or settings['running_mean_color']
    running_mean_width = running_mean_width or settings['running_mean_width']
    # Set default line widths
    frame_linewidth = 2.0
    mean_linewidth = running_mean_width
    # Legend labels
    frame_label = 'ΔGbind / frame'
    mean_label = f"{settings.get('window_size', 10)} - running mean"
    if show_frames:
        ax.plot(
            time_ns, dg,
            color=frame_color,
            alpha=settings['frame_alpha'],
            linestyle=frame_style,
            linewidth=frame_linewidth,
            label=frame_label
        )
    ax.plot(
        time_ns, running,
        color=running_color,
        linewidth=mean_linewidth,
        linestyle=running_style,
        label=mean_label
    )
    # Always show both legend entries
    ax.legend(loc=settings.get('legend_position', 'best'))
    # Add error bars if requested
    if settings['show_running_mean'] and show_error_bars:
        try:
            x = np.array(time_ns)
            y = running.values
            if settings['error_type'] == "Standard Error" or settings['error_type'] == "Standard Deviation":
                yerr = np.array(yerr)
                valid_mask = ~np.isnan(yerr)
                if np.any(valid_mask):
                    ax.errorbar(
                        x[valid_mask],
                        y[valid_mask],
                        yerr=yerr[valid_mask],
                        color=running_color,
                        alpha=settings['error_alpha'],
                        fmt='none',
                        capsize=3,
                        label=None
                    )
            else:
                yerr_lower = np.abs(y - np.array(ci_lower))
                yerr_upper = np.abs(np.array(ci_upper) - y)
                valid_mask = ~np.isnan(yerr_lower) & ~np.isnan(yerr_upper)
                if np.any(valid_mask):
                    ax.errorbar(
                        x[valid_mask],
                        y[valid_mask],
                        yerr=[yerr_lower[valid_mask], yerr_upper[valid_mask]],
                        color=running_color,
                        alpha=settings['error_alpha'],
                        fmt='none',
                        capsize=3,
                        label=None
                    )
        except Exception as e:
            st.warning(f"Could not plot error bars for {ligand_id}: {str(e)}")


# ------------------------
# Streamlit UI
# ------------------------

st.set_page_config(page_title="MM‑GBSA Viewer", layout="centered")
st.title("MM‑GBSA Trajectory Viewer")

# Initialize session state for settings if not exists
if 'settings' not in st.session_state:
    st.session_state.settings = DEFAULT_SETTINGS.copy()
else:
    # Ensure all default settings exist in session state
    for key, value in DEFAULT_SETTINGS.items():
        if key not in st.session_state.settings:
            st.session_state.settings[key] = value

# Track last ligand name for legend label defaults
if 'last_ligand_id' not in st.session_state:
    st.session_state['last_ligand_id'] = None
if 'last_frame_label_default' not in st.session_state:
    st.session_state['last_frame_label_default'] = None
if 'last_mean_label_default' not in st.session_state:
    st.session_state['last_mean_label_default'] = None

# Track last window size for mean label default
if 'last_window_size' not in st.session_state:
    st.session_state['last_window_size'] = None

# --- Robust legend label logic (final, professional version) ---
current_window_size = st.session_state.settings.get('window_size', 10)
default_frame_label = 'ΔGbind / frame'
default_mean_label = f'{current_window_size} - running mean'

# Frame label logic
frame_label = st.session_state.settings.get('frame_legend_label', None)
if not frame_label or frame_label.strip() == '':
    frame_label = default_frame_label

# Mean label logic
mean_label = st.session_state.settings.get('mean_legend_label', None)
if not mean_label or mean_label.strip() == '' or mean_label == f"{st.session_state.get('last_window_size', 10)} - running mean":
    mean_label = default_mean_label
st.session_state['last_window_size'] = current_window_size

# File upload section (moved before sidebar to update titles properly)
comparison_mode = st.session_state.settings.get('comparison_mode', False)

if comparison_mode:
    st.subheader("Upload Multiple Ligand Data")
    uploaded_files = st.file_uploader(
        "Upload thermal_MMGBSA.csv files",
        type="csv",
        accept_multiple_files=True
    )
    max_ligands = st.session_state.settings.get('max_ligands', 4)
    if len(uploaded_files) > max_ligands:
        st.warning(f"Maximum {max_ligands} ligands allowed. Only the first {max_ligands} files will be used.")
        uploaded_files = uploaded_files[:max_ligands]
    # --- Read each file ONCE and store DataFrame and ligand_id ---
    file_data = []
    for idx, csv_file in enumerate(uploaded_files):
        try:
            csv_file.seek(0)
            df = pd.read_csv(csv_file)
            ligand_id = parse_ligand_id(df.get("title", pd.Series(["Ligand"])).iloc[0])
            file_data.append({'df': df, 'ligand_id': ligand_id, 'csv_file': csv_file})
        except Exception:
            ligand_id = f"Ligand_{idx+1}"
            file_data.append({'df': None, 'ligand_id': ligand_id, 'csv_file': csv_file})
else:
    csv_file = st.file_uploader("Upload thermal_MMGBSA.csv", type="csv")
    uploaded_files = [csv_file] if csv_file else []
    file_data = []
    if csv_file:
        try:
            csv_file.seek(0)
            df = pd.read_csv(csv_file)
            ligand_id = parse_ligand_id(df.get("title", pd.Series(["Ligand"])).iloc[0])
            file_data.append({'df': df, 'ligand_id': ligand_id, 'csv_file': csv_file})
            # Update plot title with ligand name when file is uploaded (single ligand mode)
            default_title_with_ligand = f"ΔGbind vs Time (ns) - {ligand_id}"
            if (st.session_state.settings['plot_title'] == "ΔGbind vs Time (ns)" or 
                not st.session_state.settings['plot_title'] or
                st.session_state.settings['plot_title'].startswith("ΔGbind vs Time (ns) - ") and 
                " - " in st.session_state.settings['plot_title']):
                st.session_state.settings['plot_title'] = default_title_with_ligand
        except Exception:
            ligand_id = "Ligand_1"
            file_data.append({'df': None, 'ligand_id': ligand_id, 'csv_file': csv_file})

# Add sidebar for visualization controls
with st.sidebar:
    st.header("Visualization Settings")
    
    # Reset button at the top
    if st.button("Reset All Settings to Defaults"):
        st.session_state.settings = DEFAULT_SETTINGS.copy()
        st.rerun()
    
    # Comparison mode toggle
    st.session_state.settings['comparison_mode'] = st.checkbox(
        "Comparison Mode",
        value=st.session_state.settings['comparison_mode'],
        help="Enable to compare multiple ligands"
    )
    
    if st.session_state.settings['comparison_mode']:
        st.session_state.settings['max_ligands'] = st.slider(
            "Maximum Number of Ligands",
            min_value=2,
            max_value=6,
            value=st.session_state.settings['max_ligands'],
            help="Maximum number of ligands to compare"
        )
    
    # Plot visibility controls
    st.subheader("Plot Elements")
    st.session_state.settings['show_frames'] = st.checkbox(
        "Show Individual Frames",
        value=st.session_state.settings['show_frames']
    )
    st.session_state.settings['show_running_mean'] = st.checkbox(
        "Show Running Mean",
        value=st.session_state.settings['show_running_mean']
    )
    
    # Running mean settings
    st.subheader("Running Mean Settings")
    st.session_state.settings['window_size'] = st.slider(
        "Window Size",
        min_value=1,
        max_value=50,
        value=st.session_state.settings['window_size'],
        help="Number of frames to use for calculating the running mean"
    )
    
    # Error bars settings
    st.subheader("Error Bars Settings")
    st.session_state.settings['show_error_bars'] = st.checkbox(
        "Show Error Bars",
        value=st.session_state.settings['show_error_bars']
    )
    if st.session_state.settings['show_error_bars']:
        st.session_state.settings['error_type'] = st.selectbox(
            "Error Type",
            ["Standard Error", "Standard Deviation", "95% Confidence Interval"],
            index=["Standard Error", "Standard Deviation", "95% Confidence Interval"].index(
                st.session_state.settings['error_type']
            )
        )
        st.session_state.settings['error_alpha'] = st.slider(
            "Error Bar Transparency",
            0.0, 1.0,
            value=st.session_state.settings['error_alpha'],
            step=0.1
        )
    
    # Style settings
    st.subheader("Style Settings")
    
    # Plot labels
    st.subheader("Plot Labels")
    if st.session_state.settings['comparison_mode']:
        st.session_state.settings['plot_title'] = st.text_input(
            "Plot Title",
            value=st.session_state.settings.get('plot_title', "ΔGbind Comparison"),
            help="Customize the plot title"
        )
    else:
        st.session_state.settings['plot_title'] = st.text_input(
            "Plot Title",
            value=st.session_state.settings['plot_title'],
            help="Customize the plot title"
        )
    st.session_state.settings['x_label'] = st.text_input(
        "X-axis Label",
        value=st.session_state.settings.get('x_label', "Time (ns)"),
        help="Customize the X-axis label"
    )
    st.session_state.settings['y_label'] = st.text_input(
        "Y-axis Label",
        value=st.session_state.settings.get('y_label', "ΔGbind (kcal/mol)"),
        help="Customize the Y-axis label"
    )
    
    st.session_state.settings['frame_color'] = st.color_picker(
        "Frame Color",
        value=st.session_state.settings['frame_color']
    )
    st.session_state.settings['frame_alpha'] = st.slider(
        "Frame Transparency",
        0.0, 1.0,
        value=st.session_state.settings['frame_alpha'],
        step=0.1
    )
    st.session_state.settings['frame_style'] = st.selectbox(
        "Frame Line Style",
        ["solid", "dashed", "dotted", "dashdot"],
        index=["solid", "dashed", "dotted", "dashdot"].index(
            st.session_state.settings['frame_style']
        )
    )
    
    st.session_state.settings['running_mean_color'] = st.color_picker(
        "Running Mean Color",
        value=st.session_state.settings['running_mean_color']
    )
    st.session_state.settings['running_mean_width'] = st.slider(
        "Running Mean Line Width",
        0.1, 5.0,
        value=st.session_state.settings['running_mean_width'],
        step=0.1
    )
    st.session_state.settings['running_mean_style'] = st.selectbox(
        "Running Mean Line Style",
        ["solid", "dashed", "dotted", "dashdot"],
        index=["solid", "dashed", "dotted", "dashdot"].index(
            st.session_state.settings['running_mean_style']
        )
    )

    # Legend settings
    st.subheader("Legend Settings")
    st.session_state.settings['legend_position'] = st.selectbox(
        "Legend Position",
        ["best", "upper right", "upper left", "lower left", "lower right", "center left", "center right", "lower center", "upper center", "center"],
        index=["best", "upper right", "upper left", "lower left", "lower right", "center left", "center right", "lower center", "upper center", "center"].index(
            st.session_state.settings.get('legend_position', "best")
        ),
        help="Choose where to place the legend"
    )

# Use settings from session state
settings = st.session_state.settings

md_length_ns = st.number_input("Total MD time (ns)", value=100, min_value=1)

# --- Per-ligand settings in comparison mode ---
if settings['comparison_mode'] and file_data:
    if 'ligand_settings' not in st.session_state:
        st.session_state.ligand_settings = {}
    ligand_settings = st.session_state.ligand_settings
    ligand_ids = []
    for idx, entry in enumerate(file_data):
        ligand_id = entry['ligand_id']
        ligand_ids.append(ligand_id)
        # Assign palette color by default
        default_color = COLOR_PALETTE[idx % len(COLOR_PALETTE)]
        if ligand_id not in ligand_settings:
            ligand_settings[ligand_id] = {
                'frame_color': default_color,
                'frame_style': 'solid',
                'running_mean_color': default_color,
                'running_mean_style': 'solid',
                'show_frames': False,  # Hide frame lines by default in comparison mode
            }
    st.sidebar.subheader("Per-Ligand Plot Settings")
    for ligand_id in ligand_ids:
        with st.sidebar.expander(f"{ligand_id}"):
            ligand_settings[ligand_id]['show_frames'] = st.checkbox(
                f"Show Frame Line ({ligand_id})", value=ligand_settings[ligand_id]['show_frames'], key=f"show_frames_{ligand_id}")
            ligand_settings[ligand_id]['frame_color'] = st.color_picker(
                f"Frame Color ({ligand_id})", value=ligand_settings[ligand_id]['frame_color'], key=f"frame_color_{ligand_id}")
            ligand_settings[ligand_id]['frame_style'] = st.selectbox(
                f"Frame Line Style ({ligand_id})", ["solid", "dashed", "dotted", "dashdot"],
                index=["solid", "dashed", "dotted", "dashdot"].index(ligand_settings[ligand_id]['frame_style']), key=f"frame_style_{ligand_id}")
            ligand_settings[ligand_id]['running_mean_color'] = st.color_picker(
                f"Running Mean Color ({ligand_id})", value=ligand_settings[ligand_id]['running_mean_color'], key=f"running_color_{ligand_id}")
            ligand_settings[ligand_id]['running_mean_style'] = st.selectbox(
                f"Running Mean Line Style ({ligand_id})", ["solid", "dashed", "dotted", "dashdot"],
                index=["solid", "dashed", "dotted", "dashdot"].index(ligand_settings[ligand_id]['running_mean_style']), key=f"running_style_{ligand_id}")
    st.session_state.ligand_settings = ligand_settings

if file_data and md_length_ns > 0:
    # Store data for comparison
    all_stats = []
    # Create figure for plotting
    if settings['comparison_mode']:
        fig, ax = plt.subplots(figsize=(10, 6))
    else:
        fig, ax = plt.subplots(figsize=(8, 4))
    for entry in file_data:
        df = entry['df']
        ligand_id = entry['ligand_id']
        if df is None or df.empty:
            st.error(f"File {entry['csv_file'].name} is empty or has no valid data. Please check the file format.")
            continue
        if "r_psp_MMGBSA_dG_Bind" not in df.columns:
            st.error(f"Column 'r_psp_MMGBSA_dG_Bind' not found in {entry['csv_file'].name}. Please check if this is a valid MMGBSA output file.")
            continue
        dg = df["r_psp_MMGBSA_dG_Bind"].astype(float)
        # Use per-ligand settings if in comparison mode
        if settings['comparison_mode'] and 'ligand_settings' in st.session_state and ligand_id in st.session_state.ligand_settings:
            ligand_cfg = st.session_state.ligand_settings[ligand_id]
            color = ligand_cfg['running_mean_color']
            frame_color = ligand_cfg['frame_color']
            frame_style = ligand_cfg['frame_style']
            running_color = ligand_cfg['running_mean_color']
            running_style = ligand_cfg['running_mean_style']
            show_frames = ligand_cfg.get('show_frames', False)
        else:
            color = None
            frame_color = settings['frame_color']
            frame_style = settings['frame_style']
            running_color = settings['running_mean_color']
            running_style = settings['running_mean_style']
            show_frames = settings['show_frames']
        # Time axis in ns
        dt = md_length_ns / max(len(dg) - 1, 1)
        time_ns = [i * dt for i in range(len(dg))]
        # Running mean with customizable window size
        running = dg.rolling(window=settings['window_size'], min_periods=1).mean()
        # Calculate error bars if requested
        yerr = None
        ci_lower = None
        ci_upper = None
        if settings['show_error_bars']:
            if settings['error_type'] == "Standard Error":
                running_std = dg.rolling(window=settings['window_size'], min_periods=2).std()
                running_count = dg.rolling(window=settings['window_size'], min_periods=2).count()
                running_std = running_std / np.sqrt(running_count)
                yerr = running_std.fillna(0)
            elif settings['error_type'] == "Standard Deviation":
                running_std = dg.rolling(window=settings['window_size'], min_periods=2).std()
                yerr = running_std.fillna(0)
            else:  # 95% Confidence Interval
                ci_lower = []
                ci_upper = []
                for i in range(len(dg)):
                    if i < 2:
                        ci_lower.append(dg.iloc[i])
                        ci_upper.append(dg.iloc[i])
                    else:
                        window_data = dg.iloc[max(0, i-settings['window_size']+1):i+1]
                        if len(window_data) >= 2:
                            _, lower, upper = calculate_confidence_interval(window_data)
                            ci_lower.append(lower)
                            ci_upper.append(upper)
                        else:
                            ci_lower.append(dg.iloc[i])
                            ci_upper.append(dg.iloc[i])
        # Plot the data with ligand-specific settings
        plot_ligand_data(
            ax, time_ns, dg, running, settings, ligand_id,
            settings['show_error_bars'], yerr, ci_lower, ci_upper,
            color=running_color, frame_color=frame_color, frame_style=frame_style, running_style=running_style, show_frames=show_frames, running_mean_width=settings['running_mean_width']
        )
        # Store statistics
        stats = compute_stats(dg)
        stats['ligand_id'] = ligand_id
        all_stats.append(stats)
    # Only proceed with plotting if we have valid data
    if not all_stats:
        st.error("No valid data to plot. Please check your input files.")
        st.stop()
    # Set plot properties
    ax.set_xlabel(st.session_state.settings['x_label'])
    ax.set_ylabel(st.session_state.settings['y_label'])
    title = st.session_state.settings['plot_title']
    if not title:
        title = "ΔGbind vs Time (ns)"
    ax.set_title(title)
    
    fig.tight_layout()

    # Display plot
    st.pyplot(fig, use_container_width=True)

    # PNG download
    png_buf = io.BytesIO()
    fig.savefig(png_buf, format="png", dpi=300)
    png_buf.seek(0)
    st.download_button(
        label="Download PNG",
        data=png_buf,
        file_name=f"mmgbsa_comparison.png" if settings['comparison_mode'] else f"{all_stats[0]['ligand_id']}_dg_time.png",
        mime="image/png",
    )

    # Display comparison statistics
    st.markdown("### ΔGbind Statistics")
    if settings['comparison_mode']:
        # Create a comparison table
        comparison_data_display = []
        comparison_data_csv = []
        for stats in all_stats:
            comparison_data_display.append({
                "Ligand": stats['ligand_id'],
                "Mean ΔGbind": f"{stats['mean']:.2f}",
                "StdDev": f"{stats['stdev']:.2f}",
                "Min (Best)": f"{stats['minimum']:.2f}",
                "Max (Worst)": f"{stats['maximum']:.2f}",
                "Frames": stats['frames']
            })
            comparison_data_csv.append({
                "Ligand": stats['ligand_id'],
                "Mean_dGbind": stats['mean'],
                "StdDev": stats['stdev'],
                "Min_Best": stats['minimum'],
                "Max_Worst": stats['maximum'],
                "Frames": stats['frames']
            })
        df_stats_display = pd.DataFrame(comparison_data_display)
        df_stats_csv = pd.DataFrame(comparison_data_csv)
        df_stats_display.index = df_stats_display.index + 1  # Start index at 1
        st.table(df_stats_display)
        # --- Download CSV button ---
        csv_buf = io.StringIO()
        df_stats_csv.to_csv(csv_buf, index=False)
        st.download_button(
            label="Download CSV table",
            data=csv_buf.getvalue(),
            file_name="mmgbsa_comparison_stats.csv",
            mime="text/csv",
        )
    else:
        st.write(all_stats[0])

    # TXT download
    txt_lines = []
    if settings['comparison_mode']:
        txt_lines.append("MMGBSA Comparison Statistics")
        txt_lines.append("=" * 30)
        for stats in all_stats:
            txt_lines.extend([
                f"\nLigand: {stats['ligand_id']}",
                f"Mean ΔGbind: {stats['mean']:.2f} kcal/mol",
                f"StdDev: {stats['stdev']:.2f}",
                f"Range: {stats['minimum']:.2f} to {stats['maximum']:.2f}",
                f"Frames: {stats['frames']}",
                "-" * 30
            ])
    else:
        txt_lines.extend([
            f"Ligand: {all_stats[0]['ligand_id']}",
            f"Mean ΔGbind: {all_stats[0]['mean']:.2f} kcal/mol",
            f"StdDev: {all_stats[0]['stdev']:.2f}",
            f"Range: {all_stats[0]['minimum']:.2f} to {all_stats[0]['maximum']:.2f}",
            f"Frames: {all_stats[0]['frames']}",
            f"Running mean window size: {settings['window_size']}",
            f"Frame style: {settings['frame_style']}",
            f"Running mean style: {settings['running_mean_style']}"
        ])
        if settings['show_error_bars']:
            txt_lines.append(f"Error bars: {settings['error_type']}")

    txt_buf = io.BytesIO("\n".join(txt_lines).encode())
    st.download_button(
        label="Download TXT stats",
        data=txt_buf,
        file_name=f"mmgbsa_comparison_stats.txt" if settings['comparison_mode'] else f"{all_stats[0]['ligand_id']}_dg_stats.txt",
        mime="text/plain",
    )
else:
    st.info("Upload CSV file(s) and set the total simulation time to begin.")
