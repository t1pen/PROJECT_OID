"""
Seaborn Configuration Module
Standardized styling for all EDA visualizations
Import and use: from seaborn_config import *
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ============================================================================
# 1. COLOR PALETTES & THEMES
# ============================================================================

# Primary color palette
PRIMARY_PALETTE = "husl"  # Options: "husl", "Set2", "Set1", "Dark2", "Pastel1"
ACCENT_COLOR = "#2E86AB"      # Deep blue
SUCCESS_COLOR = "#06A77D"     # Teal/Green
WARNING_COLOR = "#D62828"     # Red
INFO_COLOR = "#F77F00"        # Orange
NEUTRAL_COLOR = "#6C757D"     # Gray

# Color maps for continuous data
CONTINUOUS_CMAP = "viridis"  # Options: "viridis", "coolwarm", "RdYlBu", "plasma"
DIVERGING_CMAP = "RdBu_r"    # For diverging data (positive/negative)

# ============================================================================
# 2. SEABORN STYLE & CONTEXT SETTINGS
# ============================================================================

SEABORN_STYLE = "whitegrid"  # Options: "darkgrid", "whitegrid", "dark", "white", "ticks"
SEABORN_CONTEXT = "notebook"  # Options: "paper", "notebook", "talk", "poster"

# ============================================================================
# 3. FONT CONFIGURATION
# ============================================================================

FONT_FAMILY = "sans-serif"
FONT_NAMES = ["Arial", "Helvetica", "DejaVu Sans"]  # Fallback order

# Font sizes (in points)
FONT_SIZES = {
    "title": 16,          # Main plot title
    "subtitle": 14,       # Subtitle/secondary title
    "label": 12,          # Axis labels
    "tick": 11,           # Tick labels
    "legend": 11,         # Legend text
    "annotation": 10,     # Annotations on plots
    "caption": 9,         # Small text/captions
}

# Font weights
FONT_WEIGHTS = {
    "title": "bold",
    "subtitle": "semibold",
    "label": "normal",
    "tick": "normal",
    "legend": "normal",
}

# Text colors
TEXT_COLORS = {
    "primary": "#1F2937",    # Dark gray (main text)
    "secondary": "#6B7280",  # Medium gray (secondary text)
    "light": "#9CA3AF",      # Light gray (tertiary text)
}

# ============================================================================
# 4. FIGURE SIZE STANDARDS
# ============================================================================

FIGURE_SIZES = {
    "small": (8, 5),           # Single plot, compact
    "medium": (12, 6),         # Standard single plot
    "large": (14, 8),          # Larger single plot or detailed viz
    "wide": (16, 5),           # Wide format (good for time series)
    "tall": (10, 10),          # Tall format
    "square": (10, 10),        # Square format
    
    # Multi-plot layouts
    "double_row": (16, 6),     # Two plots side by side
    "triple_row": (18, 5),     # Three plots in a row
    "grid_2x2": (14, 10),      # 2x2 grid
    "grid_2x3": (16, 10),      # 2x3 grid
    "grid_3x3": (16, 12),      # 3x3 grid
    
    # Special cases
    "heatmap": (12, 8),        # Correlation heatmaps
    "distribution": (12, 5),   # Distribution plots
    "boxplot": (12, 6),        # Box plot comparison
    "violin": (14, 7),         # Violin plots
    "scatter": (10, 8),        # Scatter plots
    "histogram": (12, 6),      # Histograms
    "barplot": (12, 6),        # Bar plots
    "line": (14, 6),           # Line plots/time series
}

# Default DPI for saving figures
DEFAULT_DPI = 300

# ============================================================================
# 5. MARGIN & SPACING SETTINGS
# ============================================================================

TIGHT_LAYOUT_PARAMS = {
    "pad": 1.2,        # Padding between subplots
    "w_pad": 2.0,      # Width padding
    "h_pad": 2.5,      # Height padding
}

# ============================================================================
# 6. SETUP FUNCTION (Apply all settings at once)
# ============================================================================

def apply_style_config(style=SEABORN_STYLE, context=SEABORN_CONTEXT, palette=PRIMARY_PALETTE):
    """
    Apply standardized Seaborn styling to all subsequent plots.
    
    Parameters:
    -----------
    style : str
        Seaborn style ('darkgrid', 'whitegrid', 'dark', 'white', 'ticks')
    context : str
        Seaborn context ('paper', 'notebook', 'talk', 'poster')
    palette : str
        Color palette ('husl', 'Set2', 'Set1', 'Dark2', 'Pastel1')
    """
    
    # Set Seaborn style and context
    sns.set_style(style)
    sns.set_context(context, font_scale=1.0)
    sns.set_palette(palette)
    
    # Configure matplotlib
    plt.rcParams.update({
        # Font settings
        'font.family': FONT_FAMILY,
        'font.sans-serif': FONT_NAMES,
        
        # Font sizes
        'font.size': FONT_SIZES['label'],
        'axes.titlesize': FONT_SIZES['title'],
        'axes.labelsize': FONT_SIZES['label'],
        'xtick.labelsize': FONT_SIZES['tick'],
        'ytick.labelsize': FONT_SIZES['tick'],
        'legend.fontsize': FONT_SIZES['legend'],
        
        # Font weights
        'axes.titleweight': FONT_WEIGHTS['title'],
        'axes.labelweight': 'normal',
        
        # Text colors
        'text.color': TEXT_COLORS['primary'],
        'axes.labelcolor': TEXT_COLORS['primary'],
        'xtick.color': TEXT_COLORS['secondary'],
        'ytick.color': TEXT_COLORS['secondary'],
        'axes.edgecolor': TEXT_COLORS['light'],
        
        # Figure background
        'figure.facecolor': 'white',
        'axes.facecolor': '#F8F9FA',  # Very light gray
        'savefig.facecolor': 'white',
        
        # Grid
        'grid.color': '#E5E7EB',
        'grid.linestyle': '--',
        'grid.linewidth': 0.6,
        'grid.alpha': 0.5,
        
        # Spines
        'axes.spines.left': True,
        'axes.spines.bottom': True,
        'axes.spines.right': False,
        'axes.spines.top': False,
        'axes.linewidth': 0.8,
        
        # Legend
        'legend.frameon': True,
        'legend.framealpha': 0.95,
        'legend.edgecolor': TEXT_COLORS['light'],
        'legend.fancybox': True,
        'legend.shadow': False,
        'legend.loc': 'best',
        
        # Figure
        'figure.figsize': FIGURE_SIZES['medium'],
        'figure.dpi': 100,
        'savefig.dpi': DEFAULT_DPI,
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.3,
        
        # Lines
        'lines.linewidth': 2.0,
        'lines.markersize': 6,
        'patch.linewidth': 0.5,
        'patch.edgecolor': 'gray',
        
        # Ticks
        'xtick.major.size': 5,
        'xtick.minor.size': 3,
        'ytick.major.size': 5,
        'ytick.minor.size': 3,
    })
    
    print("✓ Seaborn configuration applied successfully!")

# ============================================================================
# 7. HELPER FUNCTIONS FOR COMMON PLOT CONFIGURATIONS
# ============================================================================

def get_figure_and_axes(plot_type='medium', num_plots=1, layout=None):
    """
    Create a figure with standardized sizing based on plot type.
    
    Parameters:
    -----------
    plot_type : str
        Type of plot ('small', 'medium', 'large', 'wide', 'tall', etc.)
    num_plots : int
        Number of subplots needed
    layout : tuple
        Custom layout (rows, cols) - overrides default sizing
    
    Returns:
    --------
    fig : matplotlib.figure.Figure
    axes : matplotlib.axes.Axes or np.ndarray of Axes
    """
    
    if plot_type not in FIGURE_SIZES:
        plot_type = 'medium'
    
    if num_plots == 1:
        figsize = FIGURE_SIZES[plot_type]
        fig, ax = plt.subplots(figsize=figsize, dpi=100)
        return fig, ax
    
    elif layout is None:
        # Auto-determine layout based on number of plots
        if num_plots <= 2:
            layout = (1, num_plots)
        elif num_plots <= 3:
            layout = (1, num_plots)
        elif num_plots <= 4:
            layout = (2, 2)
        elif num_plots <= 6:
            layout = (2, 3)
        else:
            layout = (3, 3)
    
    figsize = FIGURE_SIZES.get(plot_type, FIGURE_SIZES['medium'])
    fig, axes = plt.subplots(*layout, figsize=figsize, dpi=100)
    
    return fig, axes

def set_title_and_labels(ax, title=None, xlabel=None, ylabel=None, fontsize_title=None, fontsize_label=None):
    """
    Set title and labels with standardized font sizing.
    
    Parameters:
    -----------
    ax : matplotlib.axes.Axes
        Axes object
    title : str
        Plot title
    xlabel : str
        X-axis label
    ylabel : str
        Y-axis label
    fontsize_title : int
        Custom title font size
    fontsize_label : int
        Custom label font size
    """
    
    fontsize_title = fontsize_title or FONT_SIZES['title']
    fontsize_label = fontsize_label or FONT_SIZES['label']
    
    if title:
        ax.set_title(title, fontsize=fontsize_title, fontweight=FONT_WEIGHTS['title'], pad=15)
    
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=fontsize_label, fontweight='normal')
    
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=fontsize_label, fontweight='normal')
    
    return ax

def style_axes(ax, remove_spines=['top', 'right'], grid=True):
    """
    Apply standardized styling to axes.
    
    Parameters:
    -----------
    ax : matplotlib.axes.Axes
        Axes object
    remove_spines : list
        Spines to remove ('top', 'right', 'bottom', 'left')
    grid : bool
        Whether to show grid
    """
    
    for spine in remove_spines:
        ax.spines[spine].set_visible(False)
    
    if grid:
        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.6)
    
    return ax

def add_legend(ax, title=None, loc='best', framealpha=0.95):
    """
    Add standardized legend to axes.
    
    Parameters:
    -----------
    ax : matplotlib.axes.Axes
        Axes object
    title : str
        Legend title
    loc : str
        Legend location
    framealpha : float
        Legend frame transparency
    """
    
    legend = ax.legend(
        title=title,
        loc=loc,
        fontsize=FONT_SIZES['legend'],
        framealpha=framealpha,
        edgecolor=TEXT_COLORS['light'],
        fancybox=True,
    )
    
    if title:
        legend.get_title().set_fontsize(FONT_SIZES['label'])
        legend.get_title().set_fontweight('semibold')
    
    return legend

def save_figure(fig, filename, dpi=DEFAULT_DPI, bbox_inches='tight', pad_inches=0.3):
    """
    Save figure with standardized settings.
    
    Parameters:
    -----------
    fig : matplotlib.figure.Figure
        Figure object
    filename : str
        Output filename (with path and extension)
    dpi : int
        Resolution in DPI
    bbox_inches : str
        Bounding box setting
    pad_inches : float
        Padding around the figure
    """
    
    fig.savefig(filename, dpi=dpi, bbox_inches=bbox_inches, pad_inches=pad_inches)
    print(f"✓ Figure saved: {filename}")

# ============================================================================
# 8. PRESET STYLES FOR SPECIFIC PLOT TYPES
# ============================================================================

class PlotStyles:
    """Preset configurations for specific plot types"""
    
    @staticmethod
    def histogram_style(ax, bins=30, edgecolor='white', alpha=0.8):
        """Configure histogram styling"""
        ax.hist_params = {
            'bins': bins,
            'edgecolor': edgecolor,
            'alpha': alpha,
            'color': ACCENT_COLOR,
        }
        return ax
    
    @staticmethod
    def distribution_style(ax, kde=True):
        """Configure distribution plot styling"""
        return ax
    
    @staticmethod
    def boxplot_style(ax):
        """Configure boxplot styling"""
        return ax
    
    @staticmethod
    def heatmap_style(ax, cmap=CONTINUOUS_CMAP, annot=True, fmt='.2f', cbar=True):
        """Configure heatmap styling"""
        heatmap_params = {
            'cmap': cmap,
            'annot': annot,
            'fmt': fmt,
            'cbar': cbar,
            'linewidths': 0.5,
            'linecolor': 'white',
            'square': True,
        }
        return heatmap_params

# ============================================================================
# 9. QUICK START FUNCTIONS
# ============================================================================

def plot_histogram(data, title="Distribution", xlabel=None, ylabel="Frequency", bins=30):
    """
    Create a standardized histogram.
    
    Parameters:
    -----------
    data : array-like
        Data to plot
    title : str
        Plot title
    xlabel : str
        X-axis label
    ylabel : str
        Y-axis label
    bins : int
        Number of bins
    """
    
    fig, ax = get_figure_and_axes('medium')
    
    ax.hist(data, bins=bins, edgecolor='white', alpha=0.8, color=ACCENT_COLOR)
    
    set_title_and_labels(ax, title=title, xlabel=xlabel or 'Value', ylabel=ylabel)
    style_axes(ax)
    
    plt.tight_layout(**TIGHT_LAYOUT_PARAMS)
    return fig, ax

def plot_scatter(x, y, title="Scatter Plot", xlabel=None, ylabel=None, hue=None):
    """
    Create a standardized scatter plot.
    
    Parameters:
    -----------
    x : array-like
        X-axis data
    y : array-like
        Y-axis data
    title : str
        Plot title
    xlabel : str
        X-axis label
    ylabel : str
        Y-axis label
    hue : array-like, optional
        Color by this variable
    """
    
    fig, ax = get_figure_and_axes('medium')
    
    scatter = ax.scatter(x, y, alpha=0.6, s=80, color=ACCENT_COLOR, edgecolors='white', linewidth=0.5)
    
    set_title_and_labels(ax, title=title, xlabel=xlabel or 'X', ylabel=ylabel or 'Y')
    style_axes(ax)
    
    plt.tight_layout(**TIGHT_LAYOUT_PARAMS)
    return fig, ax

def plot_boxplot(data, title="Box Plot", ylabel=None):
    """
    Create a standardized box plot.
    
    Parameters:
    -----------
    data : array-like or dict
        Data to plot
    title : str
        Plot title
    ylabel : str
        Y-axis label
    """
    
    fig, ax = get_figure_and_axes('medium')
    
    box_parts = ax.boxplot(data, patch_artist=True)
    
    # Color the boxes
    for patch in box_parts['boxes']:
        patch.set_facecolor(ACCENT_COLOR)
        patch.set_alpha(0.7)
    
    set_title_and_labels(ax, title=title, ylabel=ylabel or 'Value')
    style_axes(ax)
    
    plt.tight_layout(**TIGHT_LAYOUT_PARAMS)
    return fig, ax

# ============================================================================
# INITIALIZATION
# ============================================================================

# Apply configuration when module is imported
apply_style_config()

print("=" * 70)
print("Seaborn Configuration Module Loaded")
print("=" * 70)
print(f"Style: {SEABORN_STYLE} | Context: {SEABORN_CONTEXT}")
print(f"Color Palette: {PRIMARY_PALETTE}")
print(f"Font Family: {FONT_FAMILY}")
print(f"Title Font Size: {FONT_SIZES['title']}pt | Label Font Size: {FONT_SIZES['label']}pt")
print("=" * 70)
