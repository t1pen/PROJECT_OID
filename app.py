import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

# Configure page settings
st.set_page_config(
    page_title="EDA Dashboard",
    page_icon="chart",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Minimal styling
st.markdown("""
    <style>
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .main { padding: 1.5rem; }
    h1, h2, h3 { margin-top: 0; }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'filename' not in st.session_state:
    st.session_state.filename = None

# App title
st.title("EDA Dashboard - Project OID")

# Sidebar
st.sidebar.header("Data Upload")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV file",
    type=['csv']
)

if uploaded_file is not None:
    try:
        st.sidebar.info("Analyzing file structure...")
        
        # Auto-detect header with user selection
        header_options = [0, 1, 2, 3, None]
        header_row = st.sidebar.selectbox(
            "Select header row:",
            header_options,
            format_func=lambda x: f"Row {x}" if x is not None else "No header",
            index=3
        )
        
        uploaded_file.seek(0)
        if header_row is not None:
            df = pd.read_csv(uploaded_file, header=header_row)
        else:
            df = pd.read_csv(uploaded_file)
        
        # Data cleaning
        cols_to_drop = ["item_no", "remarks", "Unnamed: 0", "index", "Index"]
        existing_cols = [col for col in cols_to_drop if col in df.columns]
        if existing_cols:
            df.drop(columns=existing_cols, inplace=True)
        
        # Preprocess time columns
        for col in df.columns:
            if 'time' in col.lower() and df[col].dtype == 'object':
                try:
                    def convert_time(val):
                        if pd.isna(val):
                            return 0.0
                        parts = str(val).split(':')
                        try:
                            minutes = float(parts[0])
                            seconds = float(parts[1]) if len(parts) > 1 else 0
                            return minutes + seconds / 60
                        except:
                            return np.nan
                    df[col] = df[col].apply(convert_time)
                except:
                    pass
        
        st.session_state.df = df
        st.session_state.filename = uploaded_file.name
        st.sidebar.success(f"Loaded: {df.shape[0]} rows, {df.shape[1]} columns")
        
    except Exception as e:
        st.sidebar.error(f"Error: {str(e)}")

# Load default dataset if none loaded
if st.session_state.df is None:
    try:
        df = pd.read_csv("PAASE Dataset.csv", header=3)
        df.drop(columns=["item_no", "remarks"], inplace=True, errors='ignore')
        st.session_state.df = df
        st.session_state.filename = "PAASE Dataset.csv (default)"
        st.sidebar.info("Using default PAASE Dataset")
    except Exception as e:
        st.error(f"No dataset loaded. Please upload a CSV file. Error: {e}")
        st.stop()

df = st.session_state.df

# Data Info Section
st.sidebar.header("Data Info")
st.sidebar.metric("Rows", df.shape[0])
st.sidebar.metric("Columns", df.shape[1])

with st.sidebar.expander("View Data Details"):
    st.write("First 10 rows:")
    st.dataframe(df.head(10), use_container_width=True)
    st.write("Column Info:")
    col_info = pd.DataFrame({
        'Column': df.columns,
        'Type': df.dtypes,
        'Non-Null': df.count(),
        'Missing': df.isnull().sum()
    })
    st.dataframe(col_info, use_container_width=True)

# Data Engineering Tab
st.sidebar.header("Data Engineering")

if st.sidebar.button("Open Data Engineer"):
    st.session_state.show_engineer = True

if st.session_state.get('show_engineer', False):
    st.header("Data Engineering & Preprocessing")
    
    engineer_tab = st.selectbox(
        "Select transformation",
        [
            "View & Clean Data",
            "Convert Column Types",
            "Time Format Conversion",
            "Handle Missing Values",
            "Create Calculated Columns",
            "Remove Rows/Columns"
        ]
    )
    
    st.markdown("---")
    
    # 1. View & Clean Data
    if engineer_tab == "View & Clean Data":
        st.subheader("View & Clean Data")
        
        st.write("Current data shape:", df.shape)
        st.write("Preview:")
        st.dataframe(df.head(10), use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("Column Data Types:")
            type_summary = pd.DataFrame({
                'Column': df.columns,
                'Type': df.dtypes.astype(str),
                'Missing': df.isnull().sum(),
                'Missing %': (df.isnull().sum() / len(df) * 100).round(2)
            })
            st.dataframe(type_summary, use_container_width=True)
        
        with col2:
            st.write("Basic Statistics:")
            if numeric_cols:
                st.dataframe(df[numeric_cols].describe(), use_container_width=True)
            else:
                st.info("No numeric columns found")
        
        st.write("Duplicate rows:", df.duplicated().sum())
        if st.button("Remove Duplicates"):
            df = df.drop_duplicates()
            st.session_state.df = df
            st.success("Duplicates removed!")
    
    # 2. Convert Column Types
    elif engineer_tab == "Convert Column Types":
        st.subheader("Convert Column Types")
        
        selected_col = st.selectbox("Select column to convert", all_cols)
        current_type = str(df[selected_col].dtype)
        
        st.write(f"Current type: **{current_type}**")
        st.write(f"Sample values: {df[selected_col].head(3).tolist()}")
        
        new_type = st.selectbox(
            "Convert to",
            ["int64", "float64", "string", "category", "datetime64"]
        )
        
        try:
            if st.button("Apply Conversion"):
                if new_type == "int64":
                    df[selected_col] = pd.to_numeric(df[selected_col], errors='coerce').astype('int64')
                elif new_type == "float64":
                    df[selected_col] = pd.to_numeric(df[selected_col], errors='coerce').astype('float64')
                elif new_type == "string":
                    df[selected_col] = df[selected_col].astype(str)
                elif new_type == "category":
                    df[selected_col] = df[selected_col].astype('category')
                elif new_type == "datetime64":
                    df[selected_col] = pd.to_datetime(df[selected_col], errors='coerce')
                
                st.session_state.df = df
                st.success(f"Converted {selected_col} to {new_type}")
                st.write(f"New type: **{df[selected_col].dtype}**")
        except Exception as e:
            st.error(f"Conversion error: {str(e)}")
    
    # 3. Time Format Conversion
    elif engineer_tab == "Time Format Conversion":
        st.subheader("Convert Time Format to Decimal")
        
        st.write("Convert 'mm:ss' or 'hh:mm:ss' format to float (total minutes)")
        
        # Find potential time columns
        potential_time_cols = []
        for col in all_cols:
            if df[col].dtype == 'object':
                sample = df[col].head(1).values[0]
                if isinstance(sample, str) and ':' in str(sample):
                    potential_time_cols.append(col)
        
        if potential_time_cols:
            st.info(f"Detected potential time columns: {', '.join(potential_time_cols)}")
        
        time_col = st.selectbox("Select time column", all_cols)
        
        st.write("Sample values:")
        st.write(df[time_col].head(5).tolist())
        
        time_format = st.radio(
            "Select time format",
            ["mm:ss (minutes:seconds)", "hh:mm:ss (hours:minutes:seconds)"]
        )
        
        if st.button("Convert Time to Decimal"):
            try:
                def convert_time(val, fmt):
                    if pd.isna(val):
                        return np.nan
                    parts = str(val).split(':')
                    try:
                        if fmt == "mm:ss (minutes:seconds)":
                            minutes = float(parts[0])
                            seconds = float(parts[1]) if len(parts) > 1 else 0
                            return minutes + seconds / 60
                        else:  # hh:mm:ss
                            hours = float(parts[0])
                            minutes = float(parts[1]) if len(parts) > 1 else 0
                            seconds = float(parts[2]) if len(parts) > 2 else 0
                            return hours * 60 + minutes + seconds / 60
                    except:
                        return np.nan
                
                df[time_col] = df[time_col].apply(lambda x: convert_time(x, time_format))
                st.session_state.df = df
                st.success(f"Converted {time_col} to decimal (float64)")
                st.write("New values:")
                st.write(df[time_col].head(5).tolist())
            except Exception as e:
                st.error(f"Conversion error: {str(e)}")
    
    # 4. Handle Missing Values
    elif engineer_tab == "Handle Missing Values":
        st.subheader("Handle Missing Values")
        
        missing_summary = df.isnull().sum()
        cols_with_missing = missing_summary[missing_summary > 0]
        
        if len(cols_with_missing) > 0:
            st.write("Columns with missing values:")
            st.dataframe(pd.DataFrame({
                'Column': cols_with_missing.index,
                'Missing Count': cols_with_missing.values,
                'Missing %': (cols_with_missing.values / len(df) * 100).round(2)
            }), use_container_width=True)
            
            col = st.selectbox("Select column with missing values", cols_with_missing.index.tolist())
            
            strategy = st.radio(
                "Handling strategy",
                ["Drop rows with NaN", "Fill with mean (numeric)", "Fill with median (numeric)", 
                 "Fill with mode (most frequent)", "Fill with specific value"]
            )
            
            if strategy == "Fill with specific value":
                fill_value = st.text_input("Value to fill")
            
            if st.button("Apply Strategy"):
                try:
                    if strategy == "Drop rows with NaN":
                        df = df.dropna(subset=[col])
                    elif strategy == "Fill with mean (numeric)":
                        df[col] = df[col].fillna(df[col].mean())
                    elif strategy == "Fill with median (numeric)":
                        df[col] = df[col].fillna(df[col].median())
                    elif strategy == "Fill with mode (most frequent)":
                        df[col] = df[col].fillna(df[col].mode()[0])
                    elif strategy == "Fill with specific value":
                        df[col] = df[col].fillna(fill_value)
                    
                    st.session_state.df = df
                    st.success(f"Applied strategy to {col}")
                    st.write(f"Remaining missing: {df[col].isnull().sum()}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.success("No missing values found!")
    
    # 5. Create Calculated Columns
    elif engineer_tab == "Create Calculated Columns":
        st.subheader("Create Calculated Columns")
        
        col_name = st.text_input("New column name")
        
        operation = st.radio(
            "Select operation",
            ["Add columns", "Subtract columns", "Multiply columns", "Divide columns", 
             "Average of columns", "Custom formula"]
        )
        
        if operation != "Custom formula":
            if operation == "Average of columns":
                cols_to_use = st.multiselect("Select columns to average", numeric_cols, default=numeric_cols[:2])
            else:
                col1_sel = st.selectbox("Select first column", numeric_cols)
                col2_sel = st.selectbox("Select second column", numeric_cols)
                cols_to_use = [col1_sel, col2_sel]
        else:
            cols_to_use = None
        
        if operation == "Custom formula":
            formula = st.text_area("Enter formula (e.g., df['col1'] * 2 + df['col2'])")
            if st.button("Create Column"):
                try:
                    df[col_name] = eval(formula)
                    st.session_state.df = df
                    st.success(f"Created column: {col_name}")
                    st.write(df[col_name].head())
                except Exception as e:
                    st.error(f"Formula error: {str(e)}")
        else:
            if st.button("Create Column"):
                try:
                    if operation == "Add columns":
                        df[col_name] = df[cols_to_use[0]] + df[cols_to_use[1]]
                    elif operation == "Subtract columns":
                        df[col_name] = df[cols_to_use[0]] - df[cols_to_use[1]]
                    elif operation == "Multiply columns":
                        df[col_name] = df[cols_to_use[0]] * df[cols_to_use[1]]
                    elif operation == "Divide columns":
                        df[col_name] = df[cols_to_use[0]] / df[cols_to_use[1]]
                    elif operation == "Average of columns":
                        df[col_name] = df[cols_to_use].mean(axis=1)
                    
                    st.session_state.df = df
                    st.success(f"Created column: {col_name}")
                    st.write(df[col_name].head())
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    # 6. Remove Rows/Columns
    elif engineer_tab == "Remove Rows/Columns":
        st.subheader("Remove Rows or Columns")
        
        remove_type = st.radio("What to remove", ["Remove columns", "Remove rows by condition"])
        
        if remove_type == "Remove columns":
            cols_to_remove = st.multiselect("Select columns to remove", all_cols)
            if st.button("Remove Columns"):
                df = df.drop(columns=cols_to_remove)
                st.session_state.df = df
                st.success(f"Removed columns: {', '.join(cols_to_remove)}")
        
        else:  # Remove rows by condition
            col = st.selectbox("Select column for condition", all_cols)
            condition = st.selectbox("Condition", ["equals", "not equals", "greater than", "less than", "contains"])
            value = st.text_input("Value")
            
            if st.button("Remove Rows"):
                try:
                    if condition == "equals":
                        df = df[df[col] != value]
                    elif condition == "not equals":
                        df = df[df[col] == value]
                    elif condition == "greater than":
                        df = df[df[col] <= float(value)]
                    elif condition == "less than":
                        df = df[df[col] >= float(value)]
                    elif condition == "contains":
                        df = df[~df[col].astype(str).str.contains(value)]
                    
                    st.session_state.df = df
                    st.success(f"Rows removed. New shape: {df.shape}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    st.markdown("---")
    if st.button("Close Data Engineer"):
        st.session_state.show_engineer = False
    
    # Download engineered data
    st.markdown("---")
    st.subheader("Export Engineered Data")
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download Engineered Data (CSV)",
        data=csv,
        file_name=f"engineered_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

# Main Analysis Section
st.header("Analysis")

# Get numeric and categorical columns
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
all_cols = df.columns.tolist()
analysis_type = st.selectbox(
    "Select analysis type",
    [
        "Summary Statistics",
        "Distribution (Histogram)",
        "Box Plot",
        "Scatter Plot",
        "Line Plot",
        "Correlation Heatmap",
        "Violin Plot",
        "Count Plot"
    ]
)

st.markdown("---")

# Save function
def save_plot(fig):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"plot_{timestamp}.png"
    fig.savefig(filename, dpi=300, bbox_inches='tight')
    return filename

# Analysis implementations
try:
    if analysis_type == "Summary Statistics":
        st.subheader("Summary Statistics")
        
        selected_cols = st.multiselect(
            "Select columns",
            numeric_cols,
            default=numeric_cols[:3] if len(numeric_cols) >= 3 else numeric_cols
        )
        
        if selected_cols:
            st.dataframe(df[selected_cols].describe(), use_container_width=True)
            
            # Download statistics
            csv = df[selected_cols].describe().to_csv()
            st.download_button(
                label="Download Statistics",
                data=csv,
                file_name=f"statistics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    elif analysis_type == "Distribution (Histogram)":
        st.subheader("Histogram - Distribution Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            selected_col = st.selectbox("Select column", numeric_cols)
            bins = st.slider("Number of bins", 5, 100, 30)
        
        with col2:
            fig_width = st.slider("Figure width", 8, 16, 12)
            fig_height = st.slider("Figure height", 4, 10, 6)
        
        if selected_col:
            fig, ax = plt.subplots(figsize=(fig_width, fig_height))
            ax.hist(df[selected_col].dropna(), bins=bins, alpha=0.7, color='steelblue', edgecolor='black')
            ax.set_xlabel(selected_col)
            ax.set_ylabel('Frequency')
            ax.set_title(f'Distribution: {selected_col}')
            ax.grid(True, alpha=0.3, axis='y')
            plt.tight_layout()
            st.pyplot(fig)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Save Plot"):
                    filename = save_plot(fig)
                    st.success(f"Saved: {filename}")
            with col2:
                st.info("Use browser print (Ctrl+P) to print")
    
    elif analysis_type == "Box Plot":
        st.subheader("Box Plot - Distribution Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            x_col = st.selectbox("Group by (optional)", ["None"] + categorical_cols)
            if x_col == "None":
                x_col = None
        
        with col2:
            y_col = st.selectbox("Select column", numeric_cols)
        
        with col3:
            palette = st.selectbox("Color palette", ["Set2", "Set1", "husl", "coolwarm", "viridis", "muted"])
        
        fig_width = st.slider("Figure width", 8, 16, 12, key="box_width")
        fig_height = st.slider("Figure height", 4, 10, 6, key="box_height")
        
        if y_col:
            fig, ax = plt.subplots(figsize=(fig_width, fig_height))
            
            if x_col:
                sns.boxplot(data=df, x=x_col, y=y_col, palette=palette, ax=ax)
                ax.set_xlabel(x_col)
            else:
                sns.boxplot(data=df[y_col], ax=ax, palette=palette)
                ax.set_xlabel("Data")
            
            ax.set_ylabel(y_col)
            ax.set_title(f'Box Plot: {y_col}')
            ax.grid(True, alpha=0.3, axis='y')
            
            if x_col:
                plt.xticks(rotation=45, ha='right')
            
            plt.tight_layout()
            st.pyplot(fig)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Save Plot", key="save_box"):
                    filename = save_plot(fig)
                    st.success(f"Saved: {filename}")
            with col2:
                st.info("Use browser print (Ctrl+P) to print")
    
    elif analysis_type == "Scatter Plot":
        st.subheader("Scatter Plot - Relationship Analysis")
        
        col1, col2 = st.columns(2)
        with col1:
            x_col = st.selectbox("X-axis", numeric_cols)
        with col2:
            y_col = st.selectbox("Y-axis", numeric_cols, index=1 if len(numeric_cols) > 1 else 0)
        
        col1, col2 = st.columns(2)
        with col1:
            fig_width = st.slider("Figure width", 8, 16, 12, key="scatter_width")
        with col2:
            fig_height = st.slider("Figure height", 4, 10, 6, key="scatter_height")
        
        color_col = st.selectbox("Color by (optional)", ["None"] + categorical_cols)
        
        if x_col and y_col:
            fig, ax = plt.subplots(figsize=(fig_width, fig_height))
            
            if color_col != "None":
                for category in df[color_col].unique():
                    mask = df[color_col] == category
                    ax.scatter(df[mask][x_col], df[mask][y_col], label=category, alpha=0.6, s=50)
                ax.legend()
            else:
                ax.scatter(df[x_col], df[y_col], alpha=0.6, s=50)
            
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
            ax.set_title(f'{y_col} vs {x_col}')
            ax.grid(True, alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Save Plot", key="save_scatter"):
                    filename = save_plot(fig)
                    st.success(f"Saved: {filename}")
            with col2:
                st.info("Use browser print (Ctrl+P) to print")
    
    elif analysis_type == "Line Plot":
        st.subheader("Line Plot - Trend Analysis")
        
        col1, col2 = st.columns(2)
        with col1:
            x_col = st.selectbox("X-axis", all_cols)
        with col2:
            y_cols = st.multiselect("Y-axis (one or more)", numeric_cols, default=numeric_cols[:1])
        
        col1, col2 = st.columns(2)
        with col1:
            fig_width = st.slider("Figure width", 8, 16, 12, key="line_width")
        with col2:
            fig_height = st.slider("Figure height", 4, 10, 6, key="line_height")
        
        if x_col and y_cols:
            fig, ax = plt.subplots(figsize=(fig_width, fig_height))
            
            for y_col in y_cols:
                ax.plot(df[x_col], df[y_col], marker='o', label=y_col, linewidth=2, markersize=4)
            
            ax.set_xlabel(x_col)
            ax.set_ylabel('Value')
            ax.set_title(f'Trend Analysis')
            ax.legend()
            ax.grid(True, alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Save Plot", key="save_line"):
                    filename = save_plot(fig)
                    st.success(f"Saved: {filename}")
            with col2:
                st.info("Use browser print (Ctrl+P) to print")
    
    elif analysis_type == "Correlation Heatmap":
        st.subheader("Correlation Matrix")
        
        selected_cols = st.multiselect(
            "Select columns",
            numeric_cols,
            default=numeric_cols
        )
        
        fig_size = st.slider("Figure size", 6, 14, 10)
        
        if len(selected_cols) > 1:
            corr_matrix = df[selected_cols].corr()
            
            fig, ax = plt.subplots(figsize=(fig_size, fig_size * 0.9))
            sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdBu_r', center=0,
                       square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax)
            ax.set_title('Correlation Matrix')
            plt.tight_layout()
            st.pyplot(fig)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Save Plot", key="save_corr"):
                    filename = save_plot(fig)
                    st.success(f"Saved: {filename}")
            with col2:
                st.info("Use browser print (Ctrl+P) to print")
        else:
            st.warning("Select at least 2 columns")
    
    elif analysis_type == "Violin Plot":
        st.subheader("Violin Plot - Distribution Shape Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            x_col = st.selectbox("Group by", categorical_cols if categorical_cols else ["None"])
        
        with col2:
            y_col = st.selectbox("Select column", numeric_cols)
        
        with col3:
            palette = st.selectbox("Color palette", ["Set2", "Set1", "husl", "coolwarm", "viridis"], key="violin_palette")
        
        fig_width = st.slider("Figure width", 8, 16, 12, key="violin_width")
        fig_height = st.slider("Figure height", 4, 10, 6, key="violin_height")
        
        if y_col and x_col != "None":
            fig, ax = plt.subplots(figsize=(fig_width, fig_height))
            sns.violinplot(data=df, x=x_col, y=y_col, palette=palette, ax=ax)
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
            ax.set_title(f'Violin Plot: {y_col} by {x_col}')
            ax.grid(True, alpha=0.3, axis='y')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Save Plot", key="save_violin"):
                    filename = save_plot(fig)
                    st.success(f"Saved: {filename}")
            with col2:
                st.info("Use browser print (Ctrl+P) to print")
    
    elif analysis_type == "Count Plot":
        st.subheader("Count Plot - Categorical Analysis")
        
        if categorical_cols:
            col1, col2 = st.columns(2)
            
            with col1:
                selected_col = st.selectbox("Select categorical column", categorical_cols)
            
            with col2:
                palette = st.selectbox("Color palette", ["Set2", "Set1", "husl", "coolwarm"], key="count_palette")
            
            fig_width = st.slider("Figure width", 8, 16, 12, key="count_width")
            fig_height = st.slider("Figure height", 4, 10, 6, key="count_height")
            
            if selected_col:
                fig, ax = plt.subplots(figsize=(fig_width, fig_height))
                counts = df[selected_col].value_counts()
                ax.bar(counts.index, counts.values, color='steelblue', edgecolor='black')
                ax.set_xlabel(selected_col)
                ax.set_ylabel('Count')
                ax.set_title(f'Count Plot: {selected_col}')
                ax.grid(True, alpha=0.3, axis='y')
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                st.pyplot(fig)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Save Plot", key="save_count"):
                        filename = save_plot(fig)
                        st.success(f"Saved: {filename}")
                with col2:
                    st.info("Use browser print (Ctrl+P) to print")
        else:
            st.warning("No categorical columns found")

except Exception as e:
    st.error(f"Error: {str(e)}")

st.markdown("---")
st.caption("EDA Dashboard - Data Analysis & Visualization")

# Help Section
with st.sidebar.expander("Help - Data Engineering"):
    st.markdown("""
    **Data Engineering Features:**
    
    1. **View & Clean Data**
       - See data shape and types
       - View statistics and duplicates
       - Remove duplicate rows
    
    2. **Convert Column Types**
       - Convert between: int64, float64, string, category, datetime64
    
    3. **Time Format Conversion**
       - Convert 'mm:ss' to decimal minutes (float)
       - Convert 'hh:mm:ss' to decimal minutes
       - Automatically detected for time columns
    
    4. **Handle Missing Values**
       - Drop rows with NaN
       - Fill with mean, median, mode
       - Fill with custom values
    
    5. **Create Calculated Columns**
       - Add, subtract, multiply, divide columns
       - Calculate averages
       - Use custom formulas
    
    6. **Remove Rows/Columns**
       - Remove unwanted columns
       - Remove rows by conditions
    
    **Example: mm:ss Conversion**
    - Original: "5:30" → Converted: 5.5 (minutes)
    - Original: "10:42" → Converted: 10.7
    """)
