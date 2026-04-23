import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import io
from datetime import datetime
import os

# Configure page settings
st.set_page_config(
    page_title="EDA Dashboard",
    page_icon="chart",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Minimal styling - no emojis
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

# Main Analysis Section
st.header("Analysis")

# Get numeric and categorical columns
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
all_cols = df.columns.tolist()

# User selects analysis type
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
            st.error("⚠️ 'infill_density_percent' column not found in data")
        else:
            st.subheader("Distribution Analysis: Box Plots by Infill Density")
            
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            # Remove density from selection
            if 'infill_density_percent' in numeric_cols:
                numeric_cols.remove('infill_density_percent')
            
            selected_metrics = st.multiselect(
                "Select metrics to visualize",
                numeric_cols,
                default=numeric_cols[:3] if len(numeric_cols) >= 3 else numeric_cols
            )
            
            if selected_metrics:
                fig, axes = plt.subplots(1, len(selected_metrics), figsize=(fig_width, fig_height))
                
                if len(selected_metrics) == 1:
                    axes = [axes]
                
                fig.suptitle('Distribution Analysis: Metrics by Infill Density', 
                           fontsize=14, fontweight='bold', y=1.02)
                
                for idx, col in enumerate(selected_metrics):
                    sns.boxplot(data=df, x='infill_density_percent', y=col, 
                               ax=axes[idx], palette=palette)
                    axes[idx].set_xlabel('Infill Density (%)', fontweight='bold')
                    axes[idx].set_ylabel(col, fontweight='bold')
                    axes[idx].grid(True, alpha=0.3)
                    
                    y_min, y_max = axes[idx].get_ylim()
                    y_range = y_max - y_min
                    axes[idx].set_ylim(y_min, y_max + 0.1 * y_range)
                
                plt.tight_layout()
                st.pyplot(fig)
                
                # Save and download option
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("💾 Save Plot", key="save_box"):
                        filename, image_data = save_plot_image(fig, "BoxPlot_ByDensity")
                        st.success(f"✅ Saved as {filename}")
                
                with col2:
                    if st.button("🖨️ Print Plot", key="print_box"):
                        st.info("Use your browser's print function (Ctrl+P or Cmd+P) to print")
    
    elif analysis_type == "Regression Plot (Trend Analysis)":
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        x_col = st.selectbox("Select X-axis variable", numeric_cols)
        y_cols = st.multiselect(
            "Select Y-axis variables",
            [col for col in numeric_cols if col != x_col],
            default=[col for col in numeric_cols if col != x_col][:3]
        )
        
        if y_cols:
            num_plots = len(y_cols)
            num_cols = min(3, num_plots)
            num_rows = (num_plots + num_cols - 1) // num_cols
            
            fig, axes = plt.subplots(num_rows, num_cols, figsize=(fig_width, fig_height))
            axes = axes.flatten() if hasattr(axes, 'flatten') else [axes]
            
            fig.suptitle(f'Trend Analysis: Regression Plots', fontsize=14, fontweight='bold')
            
            for idx, col in enumerate(y_cols):
                if idx < len(axes):
                    sns.regplot(data=df, x=x_col, y=col, ax=axes[idx], 
                               scatter_kws={'alpha': 0.5, 's': 50}, 
                               line_kws={'color': 'red', 'linewidth': 2})
                    axes[idx].set_xlabel(x_col, fontweight='bold')
                    axes[idx].set_ylabel(col, fontweight='bold')
                    axes[idx].grid(True, alpha=0.3)
                    
                    y_min, y_max = axes[idx].get_ylim()
                    y_range = y_max - y_min
                    axes[idx].set_ylim(y_min, y_max + 0.1 * y_range)
            
            for idx in range(num_plots, len(axes)):
                fig.delaxes(axes[idx])
            
            plt.tight_layout()
            st.pyplot(fig)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Save Plot", key="save_reg"):
                    filename, image_data = save_plot_image(fig, "RegressionPlot")
                    st.success(f"✅ Saved as {filename}")
            with col2:
                if st.button("🖨️ Print Plot", key="print_reg"):
                    st.info("Use your browser's print function (Ctrl+P or Cmd+P) to print")
    
    elif analysis_type == "Violin Plot by Replicate":
        if 'replicate_no' not in df.columns:
            st.error("⚠️ 'replicate_no' column not found in data")
        else:
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if 'replicate_no' in numeric_cols:
                numeric_cols.remove('replicate_no')
            
            selected_metrics = st.multiselect(
                "Select metrics to visualize",
                numeric_cols,
                default=numeric_cols[:3] if len(numeric_cols) >= 3 else numeric_cols,
                key="violin_select"
            )
            
            if selected_metrics:
                fig, axes = plt.subplots(1, len(selected_metrics), figsize=(fig_width, fig_height))
                
                if len(selected_metrics) == 1:
                    axes = [axes]
                
                fig.suptitle('Replicate Comparison: Distribution of Key Metrics', 
                           fontsize=14, fontweight='bold', y=1.02)
                
                for idx, col in enumerate(selected_metrics):
                    sns.violinplot(data=df, x='replicate_no', y=col, 
                                  ax=axes[idx], palette=palette)
                    axes[idx].set_xlabel('Replicate', fontweight='bold')
                    axes[idx].set_ylabel(col, fontweight='bold')
                    axes[idx].grid(True, alpha=0.3, axis='y')
                    
                    y_min, y_max = axes[idx].get_ylim()
                    y_range = y_max - y_min
                    axes[idx].set_ylim(y_min, y_max + 0.1 * y_range)
                
                plt.tight_layout()
                st.pyplot(fig)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("💾 Save Plot", key="save_violin"):
                        filename, image_data = save_plot_image(fig, "ViolinPlot_ByReplicate")
                        st.success(f"✅ Saved as {filename}")
                with col2:
                    if st.button("🖨️ Print Plot", key="print_violin"):
                        st.info("Use your browser's print function (Ctrl+P or Cmd+P) to print")
    
    elif analysis_type == "Correlation Heatmap":
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        selected_cols = st.multiselect(
            "Select columns for correlation analysis",
            numeric_cols,
            default=numeric_cols
        )
        
        if len(selected_cols) > 1:
            correlation_matrix = df[selected_cols].corr()
            
            fig, ax = plt.subplots(figsize=(fig_width, fig_width * 0.8))
            sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='RdBu_r', 
                       center=0, square=True, linewidths=1, 
                       cbar_kws={"shrink": 0.8}, ax=ax)
            ax.set_title('Correlation Matrix', fontsize=14, fontweight='bold', pad=20)
            plt.tight_layout()
            st.pyplot(fig)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Save Plot", key="save_corr"):
                    filename, image_data = save_plot_image(fig, "CorrelationHeatmap")
                    st.success(f"✅ Saved as {filename}")
            with col2:
                if st.button("🖨️ Print Plot", key="print_corr"):
                    st.info("Use your browser's print function (Ctrl+P or Cmd+P) to print")
        else:
            st.warning("⚠️ Please select at least 2 columns for correlation analysis")
    
    elif analysis_type == "Scatter Plot (Actual vs Predicted)":
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        col1, col2 = st.columns(2)
        with col1:
            x_col = st.selectbox("Select X-axis (Predicted)", numeric_cols, key="scatter_x")
        with col2:
            y_col = st.selectbox("Select Y-axis (Actual)", numeric_cols, key="scatter_y", 
                                index=1 if len(numeric_cols) > 1 else 0)
        
        fig, ax = plt.subplots(figsize=(fig_width, fig_height))
        ax.scatter(df[x_col], df[y_col], alpha=0.6, s=100)
        
        min_val = min(df[x_col].min(), df[y_col].min())
        max_val = max(df[x_col].max(), df[y_col].max())
        ax.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Perfect Agreement')
        
        ax.set_xlabel(x_col, fontweight='bold')
        ax.set_ylabel(y_col, fontweight='bold')
        ax.set_title(f'{y_col} vs {x_col}', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save Plot", key="save_scatter"):
                filename, image_data = save_plot_image(fig, "ScatterPlot")
                st.success(f"✅ Saved as {filename}")
        with col2:
            if st.button("🖨️ Print Plot", key="print_scatter"):
                st.info("Use your browser's print function (Ctrl+P or Cmd+P) to print")
    
    elif analysis_type == "Histograms & Distributions":
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        selected_cols = st.multiselect(
            "Select columns for histograms",
            numeric_cols,
            default=numeric_cols[:4] if len(numeric_cols) >= 4 else numeric_cols
        )
        
        if selected_cols:
            num_plots = len(selected_cols)
            num_cols_plot = min(3, num_plots)
            num_rows = (num_plots + num_cols_plot - 1) // num_cols_plot
            
            fig, axes = plt.subplots(num_rows, num_cols_plot, figsize=(fig_width, fig_height))
            axes = axes.flatten() if hasattr(axes, 'flatten') else [axes]
            
            fig.suptitle('Distributions: Histograms with KDE', fontsize=14, fontweight='bold')
            
            for idx, col in enumerate(selected_cols):
                axes[idx].hist(df[col].dropna(), bins=20, alpha=0.7, color='skyblue', edgecolor='black')
                ax2 = axes[idx].twinx()
                df[col].plot(kind='kde', ax=ax2, color='red', linewidth=2, label='KDE')
                axes[idx].set_xlabel(col, fontweight='bold')
                axes[idx].set_ylabel('Frequency', fontweight='bold')
                axes[idx].grid(True, alpha=0.3, axis='y')
            
            for idx in range(num_plots, len(axes)):
                fig.delaxes(axes[idx])
            
            plt.tight_layout()
            st.pyplot(fig)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Save Plot", key="save_hist"):
                    filename, image_data = save_plot_image(fig, "Histograms")
                    st.success(f"✅ Saved as {filename}")
            with col2:
                if st.button("🖨️ Print Plot", key="print_hist"):
                    st.info("Use your browser's print function (Ctrl+P or Cmd+P) to print")
    
    elif analysis_type == "Pairplot":
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        selected_cols = st.multiselect(
            "Select columns for pairplot (select 2-5 columns)",
            numeric_cols,
            default=numeric_cols[:3] if len(numeric_cols) >= 3 else numeric_cols
        )
        
        if 2 <= len(selected_cols) <= 5:
            fig = sns.pairplot(df[selected_cols], diag_kind='kde', plot_kws={'alpha': 0.6})
            fig.fig.suptitle('Pairplot: Relationships Between Variables', 
                           fontsize=14, fontweight='bold', y=1.00)
            st.pyplot(fig)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Save Plot", key="save_pair"):
                    filename, image_data = save_plot_image(fig.fig, "Pairplot")
                    st.success(f"✅ Saved as {filename}")
            with col2:
                if st.button("🖨️ Print Plot", key="print_pair"):
                    st.info("Use your browser's print function (Ctrl+P or Cmd+P) to print")
        else:
            st.warning("⚠️ Please select between 2-5 columns for pairplot")
    
    elif analysis_type == "Count Plot":
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        if not categorical_cols:
            st.error("⚠️ No categorical columns found in the dataset")
        else:
            selected_col = st.selectbox("Select categorical column", categorical_cols)
            
            fig, ax = plt.subplots(figsize=(fig_width, fig_height))
            sns.countplot(data=df, x=selected_col, palette=palette, ax=ax)
            ax.set_title(f'Count Plot: {selected_col}', fontsize=14, fontweight='bold')
            ax.set_xlabel(selected_col, fontweight='bold')
            ax.set_ylabel('Count', fontweight='bold')
            ax.grid(True, alpha=0.3, axis='y')
            
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Save Plot", key="save_count"):
                    filename, image_data = save_plot_image(fig, "CountPlot")
                    st.success(f"✅ Saved as {filename}")
            with col2:
                if st.button("🖨️ Print Plot", key="print_count"):
                    st.info("Use your browser's print function (Ctrl+P or Cmd+P) to print")
    
    elif analysis_type == "Custom Column Analysis":
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        st.subheader("Create Your Custom Analysis")
        
        col1, col2 = st.columns(2)
        with col1:
            chart_type = st.selectbox(
                "Select Chart Type",
                ["Histogram", "Box Plot", "Bar Chart", "Scatter Plot"]
            )
        
        with col2:
            if chart_type in ["Scatter Plot"]:
                x_var = st.selectbox("X-axis", numeric_cols)
                y_var = st.selectbox("Y-axis", numeric_cols)
            elif chart_type in ["Box Plot"]:
                x_var = st.selectbox("Categories (X-axis)", categorical_cols if categorical_cols else numeric_cols)
                y_var = st.selectbox("Values (Y-axis)", numeric_cols)
            elif chart_type in ["Bar Chart"]:
                x_var = st.selectbox("Categories (X-axis)", categorical_cols if categorical_cols else numeric_cols)
                y_var = st.selectbox("Values (Y-axis)", numeric_cols, key="bar_y")
            else:  # Histogram
                y_var = st.selectbox("Column", numeric_cols)
                x_var = None
        
        fig, ax = plt.subplots(figsize=(fig_width, fig_height))
        
        try:
            if chart_type == "Histogram":
                ax.hist(df[y_var].dropna(), bins=30, alpha=0.7, color='skyblue', edgecolor='black')
                ax.set_xlabel(y_var, fontweight='bold')
                ax.set_ylabel('Frequency', fontweight='bold')
            
            elif chart_type == "Scatter Plot":
                ax.scatter(df[x_var], df[y_var], alpha=0.6, s=100)
                ax.set_xlabel(x_var, fontweight='bold')
                ax.set_ylabel(y_var, fontweight='bold')
            
            elif chart_type == "Box Plot":
                sns.boxplot(data=df, x=x_var, y=y_var, palette=palette, ax=ax)
                ax.set_xlabel(x_var, fontweight='bold')
                ax.set_ylabel(y_var, fontweight='bold')
            
            elif chart_type == "Bar Chart":
                df_grouped = df.groupby(x_var)[y_var].mean().reset_index()
                ax.bar(df_grouped[x_var], df_grouped[y_var], color='skyblue', edgecolor='black')
                ax.set_xlabel(x_var, fontweight='bold')
                ax.set_ylabel(f'Mean {y_var}', fontweight='bold')
                plt.xticks(rotation=45, ha='right')
            
            ax.set_title(f'{chart_type}: {y_var}', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            st.pyplot(fig)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Save Plot", key="save_custom"):
                    filename, image_data = save_plot_image(fig, "CustomAnalysis")
                    st.success(f"✅ Saved as {filename}")
            with col2:
                if st.button("🖨️ Print Plot", key="print_custom"):
                    st.info("Use your browser's print function (Ctrl+P or Cmd+P) to print")
        
        except Exception as e:
            st.error(f"❌ Error creating chart: {e}")

except Exception as e:
    st.error(f"❌ An error occurred: {e}")
    st.write(str(e))

# CSV Inspector - Help users understand their file structure
st.markdown("---")
st.sidebar.markdown("---")
st.sidebar.subheader("🔎 CSV Inspector Tool")

with st.sidebar.expander("📋 Preview Different Header Options"):
    st.markdown("""
    **Having trouble loading your CSV?**
    
    Use this tool to see how your data looks with different header row settings.
    """)
    
    if 'filename' in st.session_state:
        filename = st.session_state.filename
        
        st.markdown(f"**File:** `{filename}`")
        
        inspect_option = st.selectbox(
            "Select header row to preview:",
            [0, 1, 2, 3, 4, "No header (use default)"],
            key="inspector_select"
        )
        
        try:
            if inspect_option == "No header (use default)":
                preview_df = pd.read_csv(f"{filename}")
            else:
                preview_df = pd.read_csv(f"{filename}", header=inspect_option, nrows=5)
            
            st.markdown(f"**Preview with header option = {inspect_option}:**")
            st.dataframe(preview_df, use_container_width=True)
            
            st.caption(f"Shape: {preview_df.shape[0]} rows × {preview_df.shape[1]} columns")
            
            if inspect_option != "No header (use default)":
                st.success(f"✓ This looks correct? Upload the file again and select 'Row {inspect_option}' as header")
        
        except FileNotFoundError:
            st.warning("File not found in project directory. Please use the file uploader above.")
        except Exception as e:
            st.error(f"Error reading file: {e}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p><small>EDA Interactive Dashboard for Project OID | Data Analysis & Visualization Tool</small></p>
</div>
""", unsafe_allow_html=True)
