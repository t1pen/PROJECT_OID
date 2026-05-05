# EDA Interactive Dashboard - Setup & Usage Guide

## Overview
This is an interactive web application built with **Streamlit** that enables you to perform Exploratory Data Analysis (EDA) on your dataset dynamically. Upload your CSV, engineer your data, select features, choose analysis types, and generate publication-quality visualizations—all from your browser!

## Features

- **Dynamic Data Upload** - Load any CSV file (default: PAASE Dataset.csv)
- **Data Engineering** - Transform and preprocess your data interactively:
  - Convert time formats (mm:ss → float64)
  - Change column types (int, float, string, category, datetime)
  - Handle missing values
  - Create calculated columns
  - Remove rows/columns
  - Clean duplicates
- **8 Analysis Types:**
  - Summary Statistics
  - Distribution (Histogram)
  - Box Plot
  - Scatter Plot
  - Line Plot
  - Correlation Heatmap
  - Violin Plot
  - Count Plot
- **Customization Options:**
  - Select multiple metrics/columns
  - Choose color palettes
  - Adjust figure size
  - Dynamic column selection
- **Save & Export:**
  - Export plots as PNG (300 DPI)
  - Download engineered data as CSV
  - Download statistics as CSV
  - Print visualizations directly

## Quick Start

### Step 1: Install Dependencies
Open PowerShell and navigate to your project directory:

```powershell
cd C:\Users\saloj\Documents\GitHub\PROJECT_OID
pip install -r requirements.txt
```

### Step 2: Run the Application
```powershell
streamlit run app.py
```

The app will automatically open in your default browser at `http://localhost:8501`

### Step 3: Start Analyzing!
1. Upload your CSV file or use the default dataset
2. (Optional) Use Data Engineering to transform your data
3. Select an analysis type
4. Choose your metrics/columns
5. Customize colors and figure size
6. Save or print your visualizations

---

## Data Engineering & Preprocessing

The dashboard includes a comprehensive Data Engineering section to transform and clean your data interactively before analysis.

### How to Use Data Engineering

1. Click **"Open Data Engineer"** in the left sidebar
2. Choose transformation type from dropdown
3. Apply the transformation
4. View results preview
5. Download engineered data when ready
6. Click **"Close Data Engineer"** to return to analysis

### Available Transformations

#### 1. View & Clean Data
- Preview your full dataset
- See data types and statistics
- Check for missing values and duplicates
- Remove duplicate rows with one click

**Example:** 
- Contains full data overview and quick access to basic statistics

#### 2. Convert Column Types
- Change column data type (int64, float64, string, category, datetime)
- Useful for fixing misinterpreted data
- Preview current type before conversion

**Example:**
- Column loaded as "object" (text) → Convert to float64 for analysis

#### 3. Time Format Conversion
- Convert 'mm:ss' format to decimal minutes (float64)
- Convert 'hh:mm:ss' format to decimal minutes
- Auto-detects time columns

**How it works:**
```
Input: "5:30" (5 minutes, 30 seconds)
Output: 5.5 (decimal minutes in float64)

Input: "10:42" (10 minutes, 42 seconds)  
Output: 10.7 (decimal minutes in float64)

Input: "1:30:45" (1 hour, 30 minutes, 45 seconds)
Output: 90.75 (decimal minutes in float64)
```

**Use Case:**
If your dataset has print times like "5:30", "6:15", "7:00", use this to convert them to 5.5, 6.25, 7.0 for correlation analysis and regression plots.

#### 4. Handle Missing Values
Replace NaN values with:
- Drop entire row
- Fill with column mean (numeric)
- Fill with column median (numeric)
- Fill with most frequent value (mode)
- Fill with custom value

**Example:**
- Energy column has 5 NaN values
- Choose "Fill with median" → filled with 0.0145 kWh

#### 5. Create Calculated Columns
Perform calculations on existing columns:
- Add two columns: col1 + col2
- Subtract: col1 - col2
- Multiply: col1 * col2
- Divide: col1 / col2
- Average: mean of multiple columns
- Custom formula: enter any pandas expression

**Example:**
- Create "energy_per_gram" = energy_used_kwh / actual_specimen_mass_g
- Create "print_efficiency" = actual_specimen_mass_g / print_time_actual

#### 6. Remove Rows/Columns
- Delete unwanted columns
- Remove rows matching conditions (equals, not equals, >/<, contains)

**Example:**
- Remove all rows where infill_density = 10%
- Delete the "remarks" column

### Export Engineered Data

After transformations, download your engineered dataset:
- Button: **"Download Engineered Data (CSV)"**
- File format: CSV (comma-separated values)
- Timestamp added to filename for version tracking

---

## Analysis Types

### 1. **Summary Statistics**
- View mean, std, min, max for selected columns
- Download statistics as CSV

### 2. **Distribution (Histogram)**
- Visualize frequency distribution
- Adjust bin count for granularity
- Identify data spread and outliers

### 3. **Box Plot**
- Compare distributions across groups
- Optional grouping by categorical variable
- See quartiles, medians, outliers

### 4. **Scatter Plot**
- Show relationship between two variables
- Optional color coding by category
- Identify patterns and correlations

### 5. **Line Plot**
- Track trends across continuous values
- Multiple Y variables on same plot
- Useful for time series data

### 6. **Correlation Heatmap**
- Show correlations between multiple variables
- Color-coded: red=positive, blue=negative
- Identify relationships between columns

### 7. **Violin Plot**
- Compare distributions across groups
- Shows full distribution shape
- Useful for identifying modes and skewness

### 8. **Count Plot**
- Analyze categorical variables
- See frequency of each category
- Useful for understanding data composition

---

## Saving & Printing Visualizations

### Save as Image
1. Generate your visualization
2. Click **Save Plot** button
3. Image is saved with timestamp: `plot_YYYYMMDD_HHMMSS.png`
4. Location: Your project's root directory
5. Resolution: 300 DPI (publication-quality)

### Print Visualization
1. Click **Print** info message
2. Use browser's print (Ctrl+P)
3. Select printer and adjust settings
4. Print directly or save as PDF

---

## Complete Workflow Example

### Scenario: Analyze print times and convert from mm:ss to decimal

**Step 1: Load & Inspect Data**
- Upload CSV file
- Select appropriate header row
- Review data in sidebar

**Step 2: Data Engineering**
- Click "Open Data Engineer"
- Go to "Time Format Conversion"
- Select print_time column
- Choose format: mm:ss
- Click "Convert Time to Decimal"
- Verify conversion worked
- Download engineered data if desired

**Step 3: Analyze**
- Click "Close Data Engineer"
- Select Analysis Type: "Scatter Plot"
- Choose X-axis: infill_density_percent
- Choose Y-axis: print_time_actual (now in decimal)
- Optional: Color by replicate_no
- Generate visualization

**Step 4: Export Results**
- Click "Save Plot" to save PNG
- Use browser print to save as PDF
- Or download statistics as CSV

---

## Customization Options

### Color Palettes
- `viridis` - Perceptually uniform
- `muted` - Subtle, professional tones
- `pastel` - Light, gentle colors

### Figure Size Controls
- **Width**: 8-20 inches (default: 14)
- **Height**: 4-16 inches (default: 6)
- Adjust for better visibility of specific data

---

## � Data Requirements

### Supported Column Names (for automatic analysis)
- `infill_density_percent` - For density-based analysis
- `replicate_no` - For replicate comparison
- `print_time_actual` - Actual print time (converted from mm:ss)
- `print_time_slicer` - Predicted print time (converted from mm:ss)
- `actual_specimen_mass_g` - Actual specimen mass
- `slicer_specimen_mass_g` - Predicted specimen mass
- `energy_used_kwh` - Energy consumption

### Data Format
- CSV file with headers in any row (configurable)
- Removes `item_no` and `remarks` columns automatically
- Handles time format conversion (mm:ss → decimal minutes)

---

## 🛠️ Troubleshooting CSV Loading Issues

### Problem: "CSV file doesn't load" or "Headers not recognized"

**Solution: Use the Header Row Selector**

When you upload a CSV file, the app now asks you to select which row contains your headers:

```
Select which row contains headers:
├─ Row 0 (first row)
├─ Row 1 (second row)
├─ Row 2 (third row)
├─ Row 3 (fourth row) ← DEFAULT for PAASE Dataset
└─ No header
```

**How to find the correct row:**

1. **Open your CSV file in Excel or a text editor**
2. **Count from row 1 (not 0)** to find your actual header row
3. **If Excel shows "Row 1, Row 2, Row 3"**, the headers are at **Row 3** in the app (which uses 0-indexing)

**Example:**
```
Excel Row → App Header Setting
Row 1     → No header or Row 0
Row 2     → Row 1 (header=1)
Row 3     → Row 2 (header=2)
Row 4     → Row 3 (header=3) ← PAASE Dataset uses this
```

### Problem: "Data looks wrong or has extra columns"

**Use the CSV Inspector:**

1. Open the **CSV Inspector Tool** in the left sidebar
2. Go to **🔎 CSV Inspector Tool** > **📋 Preview Different Header Options**
3. Try different header row settings to see what looks correct
4. Once you find the right setting, upload again and select that option

### Problem: "Column names not recognized"

The app automatically cleans these common non-data columns:
- `item_no` ✓ Removed
- `remarks` ✓ Removed
- `Unnamed: 0` ✓ Removed
- `index` / `Index` ✓ Removed

If your CSV has other unwanted columns, they'll still load—just don't select them in the analysis options.

### Problem: "Time columns not converting"

The app auto-converts these formats:
- **mm:ss format** → decimal minutes (e.g., "5:30" → 5.5)
- **HH:MM:SS format** → time object

For other time formats, the columns will load as text. You can still analyze them in the **Custom Column Analysis** section.

---

## 🔧 Troubleshooting

### App Won't Start
```powershell
# If streamlit is not found, install it explicitly:
pip install streamlit

# Then run:
streamlit run app.py
```

### Data Not Loading
- **Check file location**: Upload using the sidebar file uploader (recommended)
- **If local file**: Ensure CSV is in the same directory as `app.py`
- **Check headers**: Use the CSV Inspector Tool to preview different header rows
- **Verify format**: File must be valid CSV (not XLSX or other formats)

### CSV Loads but Headers are Wrong
- Use **🔎 CSV Inspector Tool** to preview different header options
- Select the correct row number when uploading
- Click **🔄 Reload Dataset** to try again with different settings

### Visualizations Not Appearing
- Verify selected columns exist in your dataset
- Check data types match selection (numeric for plots, categorical for count plots)
- Try the **Custom Column Analysis** to diagnose issues
- Refresh the page (Ctrl+R or Cmd+R)

### "Empty DataFrame" or All Columns are NaN
- Your header row setting is wrong
- Use CSV Inspector to find the correct row
- Or try with "No header" option and preview

### Memory Issues with Large Datasets
- Select fewer columns for pairplot analysis (max 5)
- Reduce figure size sliders
- Use scatter plots instead of pairplots for many points
- Close other applications

---

## 📋 Example CSV Files

### Example 1: Standard Header at Row 1 (header=0)
```
Column1,Column2,Column3
Value1,Value2,Value3
Value4,Value5,Value6
```
**Upload setting**: Select **Row 0**

### Example 2: Header after metadata (like PAASE) - Row 4 (header=3)
```
File Info: Project OID
Date: 2024-01-01
Version: 1.0
Column1,Column2,Column3
Value1,Value2,Value3
Value4,Value5,Value6
```
**Upload setting**: Select **Row 3** (the 4th line)

### Example 3: Header with blank rows
```
[Blank line]
[Blank line]
Column1,Column2,Column3
Value1,Value2,Value3
```
**Upload setting**: Select **Row 2**

---

## 📈 Example Workflow

1. **Load Data**: Use default PAASE Dataset or upload your own
2. **Box Plot Analysis**: Examine distributions by density
3. **Correlation**: Check which variables are related
4. **Trend Analysis**: See regression slopes for key metrics
5. **Distribution Comparison**: Use violin plots across replicates
6. **Custom Analysis**: Deep-dive into specific relationships
7. **Save Results**: Export all visualizations for reports

---

## 🎓 Tips for Better Analysis

- **Start with correlation heatmap** to understand relationships
- **Use box plots** to identify outliers
- **Compare replicates** with violin plots for consistency checks
- **Validate predictions** with scatter plots (actual vs slicer)
- **Save high-quality images** (300 DPI) for publications
- **Use appropriate palettes** for colorblind accessibility

---

## 🆘 Need Help?

For Streamlit documentation: https://docs.streamlit.io/

For Seaborn visualization: https://seaborn.pydata.org/

For Pandas data manipulation: https://pandas.pydata.org/docs/

---

## 📝 Notes

- All plots automatically include gridlines for easier reading
- Y-axis has 10% extra headroom to prevent label cutoff
- Timestamps added to saved images for version tracking
- Session state remembers your loaded data
- No data is sent anywhere—all analysis is local

---

**Happy Analyzing! 📊**
