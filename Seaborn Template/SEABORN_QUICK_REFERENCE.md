# Seaborn Configuration - Quick Reference Guide

## Setup (One Line)
```python
from seaborn_config import *
```
This automatically applies all standardized styling to your notebooks.

---

## Common Usage Patterns

### 1. Single Plot with Minimum Code
```python
fig, ax = plot_histogram(
    data=df['column_name'],
    title='Distribution Title',
    xlabel='X Label'
)
plt.show()
```

### 2. Manual Plot with Full Control
```python
fig, ax = get_figure_and_axes(plot_type='medium')

# Create your plot
ax.scatter(x, y, color=ACCENT_COLOR, alpha=0.6)

# Apply standardized styling
set_title_and_labels(ax, title='Title', xlabel='X', ylabel='Y')
style_axes(ax)

plt.tight_layout(**TIGHT_LAYOUT_PARAMS)
plt.show()
```

### 3. Multiple Plots Side by Side
```python
fig, axes = get_figure_and_axes(plot_type='double_row', num_plots=2)

# First plot
axes[0].hist(data1, bins=20, edgecolor='white', color=ACCENT_COLOR)
set_title_and_labels(axes[0], title='Plot 1')
style_axes(axes[0])

# Second plot
axes[1].hist(data2, bins=20, edgecolor='white', color=SUCCESS_COLOR)
set_title_and_labels(axes[1], title='Plot 2')
style_axes(axes[1])

plt.tight_layout(**TIGHT_LAYOUT_PARAMS)
plt.show()
```

### 4. Grid of Plots (2x2)
```python
fig, axes = get_figure_and_axes(plot_type='grid_2x2', num_plots=4)
axes = axes.flatten()  # Important: convert to 1D array

for idx, ax in enumerate(axes):
    # Create plot
    ax.hist(...)
    set_title_and_labels(ax, title=f'Plot {idx+1}')
    style_axes(ax)

plt.tight_layout(**TIGHT_LAYOUT_PARAMS)
plt.show()
```

### 5. Save High-Quality Figure
```python
fig, ax = plot_histogram(...)
save_figure(fig, './output/my_plot.png', dpi=300)
```

---

## Predefined Figure Sizes

| Size | Dimensions | Best For |
|------|-----------|----------|
| `small` | (8, 5) | Compact single plots |
| `medium` | (12, 6) | Standard single plot (default) |
| `large` | (14, 8) | Detailed single plot |
| `wide` | (16, 5) | Time series, horizontal data |
| `tall` | (10, 10) | Vertical data, stacked plots |
| `double_row` | (16, 6) | Two plots side by side |
| `triple_row` | (18, 5) | Three plots in a row |
| `grid_2x2` | (14, 10) | 2×2 grid |
| `grid_2x3` | (16, 10) | 2×3 grid |
| `grid_3x3` | (16, 12) | 3×3 grid |
| `heatmap` | (12, 8) | Correlation matrices |

---

## Font Sizes (Built-in)

| Purpose | Size |
|---------|------|
| `title` | 16pt (bold) |
| `subtitle` | 14pt (semibold) |
| `label` | 12pt (normal) |
| `tick` | 11pt (normal) |
| `legend` | 11pt (normal) |
| `annotation` | 10pt (normal) |
| `caption` | 9pt (normal) |

**Access in code:**
```python
FONT_SIZES['title']    # 16
FONT_SIZES['label']    # 12
```

---

## Color Palette

### Primary Colors
```python
ACCENT_COLOR    # #2E86AB (Deep Blue) - Main plot color
SUCCESS_COLOR   # #06A77D (Teal) - Positive/Success
WARNING_COLOR   # #D62828 (Red) - Warning/Negative
INFO_COLOR      # #F77F00 (Orange) - Info/Neutral
NEUTRAL_COLOR   # #6C757D (Gray) - Neutral
```

### Text Colors
```python
TEXT_COLORS['primary']      # Dark gray - Main text
TEXT_COLORS['secondary']    # Medium gray - Secondary text
TEXT_COLORS['light']        # Light gray - Tertiary text
```

### Usage Example
```python
# Use in plots
ax.hist(data, color=ACCENT_COLOR)
ax.scatter(x, y, color=SUCCESS_COLOR)
ax.bar(categories, values, color=WARNING_COLOR)

# Multiple plots with different colors
colors = [ACCENT_COLOR, SUCCESS_COLOR, WARNING_COLOR]
for idx, (ax, color) in enumerate(zip(axes, colors)):
    ax.plot(data, color=color)
```

---

## Helper Functions

### `get_figure_and_axes(plot_type='medium', num_plots=1, layout=None)`
Creates a figure with standardized sizing.
```python
# Single plot
fig, ax = get_figure_and_axes(plot_type='medium')

# Multiple plots
fig, axes = get_figure_and_axes(plot_type='grid_2x2', num_plots=4)
```

### `set_title_and_labels(ax, title=None, xlabel=None, ylabel=None)`
Apply standardized font sizes to titles and labels.
```python
set_title_and_labels(
    ax,
    title='My Plot Title',
    xlabel='X Axis Label',
    ylabel='Y Axis Label'
)
```

### `style_axes(ax, remove_spines=['top', 'right'], grid=True)`
Apply standardized styling to axes.
```python
style_axes(ax)  # Remove top and right spines, add grid

style_axes(ax, remove_spines=['top', 'right', 'left'], grid=False)  # Custom
```

### `add_legend(ax, title=None, loc='best')`
Add a standardized legend.
```python
add_legend(ax, title='Legend Title', loc='upper left')
```

### `save_figure(fig, filename, dpi=300)`
Save with standardized settings.
```python
save_figure(fig, './output/plot.png', dpi=300)
```

### `apply_style_config(style='whitegrid', context='notebook', palette='husl')`
Change global styling options.
```python
# Use 'talk' context for larger fonts (presentations)
apply_style_config(style='white', context='talk', palette='Set2')
```

---

## Full Example: EDA with Standard Styling

```python
from seaborn_config import *
import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('data.csv')

# === Example 1: Basic histogram ===
fig, ax = plot_histogram(
    data=df['column'],
    title='Column Distribution',
    xlabel='Value',
    bins=30
)
plt.show()

# === Example 2: Multiple comparisons ===
fig, axes = get_figure_and_axes(plot_type='double_row', num_plots=2)

axes[0].hist(df['col1'], bins=20, color=ACCENT_COLOR, edgecolor='white')
set_title_and_labels(axes[0], title='Column 1', ylabel='Frequency')
style_axes(axes[0])

axes[1].hist(df['col2'], bins=20, color=SUCCESS_COLOR, edgecolor='white')
set_title_and_labels(axes[1], title='Column 2', ylabel='Frequency')
style_axes(axes[1])

plt.tight_layout(**TIGHT_LAYOUT_PARAMS)
plt.show()

# === Example 3: Correlation heatmap ===
fig, ax = get_figure_and_axes(plot_type='heatmap')
sns.heatmap(df.corr(), annot=True, fmt='.2f', cmap='viridis', ax=ax, square=True)
set_title_and_labels(ax, title='Correlation Matrix')
plt.tight_layout(**TIGHT_LAYOUT_PARAMS)
plt.show()

# === Save high-quality version ===
save_figure(fig, './output/correlation.png', dpi=300)
```

---

## Customization

### Change Font Sizes Globally (don't modify seaborn_config.py)
```python
# After importing, modify rcParams
import matplotlib.pyplot as plt
plt.rcParams['axes.titlesize'] = 18  # Larger titles
plt.rcParams['axes.labelsize'] = 13  # Larger labels
```

### Change Default Figure Size
```python
# For the next plots
apply_style_config()  # Reset
# Then manually specify each time:
fig, ax = get_figure_and_axes(plot_type='large')
```

### Change Color Scheme (for a specific plot)
```python
fig, ax = get_figure_and_axes()
ax.hist(data, color='#FF6B6B', edgecolor='white')  # Custom color
set_title_and_labels(ax, title='Custom Color Plot')
plt.show()
```

---

## Best Practices

1. **Always use helper functions** for consistent sizing
2. **Always call `style_axes()`** after creating a plot
3. **Always use `tight_layout()`** with the `TIGHT_LAYOUT_PARAMS`
4. **Use color constants** instead of hardcoding hex values
5. **Save figures at 300 DPI** for publications and reports
6. **For presentations**, use `apply_style_config(context='talk')` for larger fonts
7. **For papers**, use `apply_style_config(context='paper')` for smaller fonts
8. **Check `FONT_SIZES` dict** before hardcoding font sizes

---

## Troubleshooting

### Plots look different from expected?
- Make sure you imported from `seaborn_config`: `from seaborn_config import *`
- Check that `apply_style_config()` was called (happens automatically on import)

### Text overlapping?
- Increase figure size: `get_figure_and_axes(plot_type='large')`
- Adjust `TIGHT_LAYOUT_PARAMS` padding values

### Colors don't match?
- Use the predefined colors: `ACCENT_COLOR`, `SUCCESS_COLOR`, etc.
- Check color values in the module

### Legend not showing?
- Make sure to call `add_legend(ax)` or add handles/labels before calling
- Try different locations: `loc='upper left'`, `loc='best'`, etc.

---

## File Structure

```
project/
├── seaborn_config.py              # Main configuration module
├── seaborn_config_example.ipynb   # Example notebook
├── EDA_analysis.ipynb             # Your analysis notebook
└── output/                        # Save figures here
    ├── plot1.png
    ├── plot2.png
    └── ...
```

---

## Version Info
- **Matplotlib**: 3.5+
- **Seaborn**: 0.12+
- **Python**: 3.7+
