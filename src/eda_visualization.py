"""
===============================================================================
 Script Name: eda_visualization.py
 Author: Igor Latii
 Description:
     This script performs Exploratory Data Analysis (EDA) on the final annual
     dataset of Latvia’s economic, demographic, and transport indicators.

     It automatically generates visualizations for three research questions (RQ1–RQ3):
         • RQ1: Relationship between GDP, trade, and passenger transport.
         • RQ2: Interaction between unemployment, migration, and population change.
         • RQ3: Correlation between transport volumes and inflation.

 Workflow:
     1. Load the annual dataset (merged_df_annual.csv).
     2. Filter observations from 1995 onwards to ensure consistent data coverage.
     3. For each Research Question (RQ):
         - Generate individual time series plots for all indicators.
         - Create scatter plots for selected variable pairs to visualize relationships.
         - Compute and visualize correlation matrices as heatmaps.
         - Produce combined plots for multi-indicator comparison (RQ1 only).
     4. Save all generated figures into dedicated subfolders under `/data/eda_plots/`.

 Output:
     • Time series plots for each indicator.
     • Scatter plots for pairwise relationships.
     • Correlation heatmaps for grouped indicators.
     • Combined GDP–Exports–Transport visualization (for RQ1).

 Dependencies:
     - pandas
     - matplotlib
     - seaborn
     - os
===============================================================================
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# === PATH CONFIGURATION ===
# Define paths for the input (merged dataset) and output (plots) directories.
input_file = "../data/processed/merged/merged_df_annual.csv"
output_dir = "../data/eda_plots"
os.makedirs(output_dir, exist_ok=True)  # Create output directory if it doesn’t exist

# === DATA LOADING ===
# Load the merged dataset that contains all relevant economic indicators.
df = pd.read_csv(input_file)

# Filter data to include only observations from 1995 onward.
# Earlier data may be sparse or inconsistent across indicators.
df = df[df['Year'] >= 1995].copy()

# === DEFINE RESEARCH QUESTIONS (RQs) AND ASSOCIATED INDICATORS ===
# Each RQ focuses on a thematic relationship between several economic factors.
# Indicators define which variables are analyzed for each question,
# and scatter_pairs specify variable combinations for correlation plots.
RQs = {
    "RQ1_GDP_Trade_Passengers": {
        # Investigates how GDP relates to trade and transport indicators.
        "indicators": ['GDP (Quarterly)', 'Exports (National Accounts)', 'Air Passenger Transport',
                       'Road Passenger Transport', 'Industrial Production Index', 'Retail Trade Turnover',
                       'Energy Prices'],
        "scatter_pairs": [('GDP (Quarterly)', 'Air Passenger Transport'),
                          ('GDP (Quarterly)', 'Road Passenger Transport'),
                          ('GDP (Quarterly)', 'Exports (National Accounts)')],
        "combined": ['GDP (Quarterly)', 'Exports (National Accounts)', 'Air Passenger Transport']
    },
    "RQ2_Unemployment_Migration": {
        # Analyzes how unemployment correlates with migration trends and population changes.
        "indicators": ['Unemployment Rate', 'Net Migration (World Bank)', 'Emigration of Citizens',
                       'Population', 'Industrial Production Index', 'Retail Trade Turnover'],
        "scatter_pairs": [('Unemployment Rate', 'Emigration of Citizens'),
                          ('Net Migration (World Bank)', 'Population')]
    },
    "RQ3_Transport_Inflation": {
        # Explores how transport activity correlates with inflation and production levels.
        "indicators": ['Inflation (HICP Manufacturing)', 'Freight Transport', 'Air Passenger Transport',
                       'Road Passenger Transport', 'Industrial Production Index', 'Retail Trade Turnover',
                       'Energy Prices'],
        "scatter_pairs": [('Inflation (HICP Manufacturing)', 'Freight Transport'),
                          ('Inflation (HICP Manufacturing)', 'Air Passenger Transport'),
                          ('Inflation (HICP Manufacturing)', 'Road Passenger Transport')]
    }
}

# === VISUAL STYLE SETTINGS ===
# Apply a consistent theme and font size for all plots for readability and publication-quality visuals.
sns.set_theme(style="whitegrid", palette="Set2")
plt.rcParams.update({
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10
})

# === FUNCTION: GENERATE EDA PLOTS FOR EACH RESEARCH QUESTION ===
def generate_eda_plots(df, rq_name, indicators, scatter_pairs, combined=None):
    """
    Generates exploratory data analysis (EDA) plots for a specific Research Question (RQ).
    Creates:
      - Time series plots for each indicator
      - Scatter plots for selected variable pairs
      - Correlation heatmap across all indicators
      - Combined multi-indicator plot (for RQ1)
    Saves all figures to the respective output folder.
    """
    rq_dir = os.path.join(output_dir, rq_name)
    os.makedirs(rq_dir, exist_ok=True)

    # === TIME SERIES PLOTS ===
    # For each indicator, create a line plot showing its trend over time.
    for ind in indicators:
        plt.figure(figsize=(12, 4))
        sns.lineplot(data=df, x='Year', y=ind, linewidth=2)
        plt.title(f'Time Series of {ind}')
        plt.xlabel('Year')
        plt.ylabel(ind)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(rq_dir, f'timeseries_{ind}.png'))
        plt.close()

    # === COMBINED TIME SERIES (RQ1 ONLY) ===
    # Overlay multiple indicators to compare their evolution on the same plot.
    if combined:
        plt.figure(figsize=(12, 6))
        for ind in combined:
            sns.lineplot(data=df, x='Year', y=ind, label=ind, linewidth=2)
        plt.title("Combined Time Series: GDP, Exports and Air Passenger Transport")
        plt.xlabel('Year')
        plt.ylabel('Value')
        plt.legend(title="Indicators")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(rq_dir, "combined_timeseries_GDP_Exports_Transport.png"))
        plt.close()

    # === SCATTER PLOTS ===
    # Scatter plots help visualize pairwise relationships between two variables.
    for x, y in scatter_pairs:
        if x in df.columns and y in df.columns:
            plt.figure(figsize=(6, 4))
            sns.scatterplot(data=df, x=x, y=y, s=60, alpha=0.8, edgecolor="w")
            plt.title(f'Scatter Plot: {y} vs {x}')
            plt.xlabel(x)
            plt.ylabel(y)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(os.path.join(rq_dir, f'scatter_{y}_vs_{x}.png'))
            plt.close()

    # === CORRELATION HEATMAP ===
    # Compute and visualize correlations between all indicators.
    # Values close to +1 indicate a strong positive correlation,
    # values near -1 indicate an inverse relationship.
    corr_data = df[indicators].replace(0, pd.NA).dropna()
    if corr_data.empty:
        print(f"⚠️ Warning: No non-zero data for correlation heatmap in {rq_name}")
    else:
        plt.figure(figsize=(10, 8))
        corr = corr_data.corr()
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", cbar=True, square=True)
        plt.title(f'Correlation Heatmap of {rq_name}')
        plt.tight_layout()
        plt.savefig(os.path.join(rq_dir, 'correlation_heatmap.png'))
        plt.close()

# === MAIN EXECUTION LOOP ===
# Iterate over all defined research questions and generate their respective EDA outputs.
for rq_name, rq_info in RQs.items():
    generate_eda_plots(df, rq_name, rq_info['indicators'], rq_info['scatter_pairs'], rq_info.get('combined'))

print(f"SUCCESS: EDA plots for all RQs saved in {output_dir}")