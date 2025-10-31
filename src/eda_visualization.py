import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# === Paths ===
input_file = "../data/processed/merged/merged_df_annual.csv"
output_dir = "../data/eda_plots"
os.makedirs(output_dir, exist_ok=True)

# === Load data ===
df = pd.read_csv(input_file)

# Фильтруем данные с 1995 года
df = df[df['Year'] >= 1995].copy()

# === Define RQs and their indicators ===
RQs = {
    "RQ1_GDP_Trade_Passengers": {
        "indicators": ['GDP (Quarterly)', 'Exports (National Accounts)', 'Air Passenger Transport',
                       'Road Passenger Transport', 'Industrial Production Index', 'Retail Trade Turnover',
                       'Energy Prices'],
        "scatter_pairs": [('GDP (Quarterly)', 'Air Passenger Transport'),
                          ('GDP (Quarterly)', 'Road Passenger Transport'),
                          ('GDP (Quarterly)', 'Exports (National Accounts)')],
        "combined": ['GDP (Quarterly)', 'Exports (National Accounts)', 'Air Passenger Transport']
    },
    "RQ2_Unemployment_Migration": {
        "indicators": ['Unemployment Rate', 'Net Migration (World Bank)', 'Emigration of Citizens',
                       'Population', 'Industrial Production Index', 'Retail Trade Turnover'],
        "scatter_pairs": [('Unemployment Rate', 'Emigration of Citizens'),
                          ('Net Migration (World Bank)', 'Population')]
    },
    "RQ3_Transport_Inflation": {
        "indicators": ['Inflation (HICP Manufacturing)', 'Freight Transport', 'Air Passenger Transport',
                       'Road Passenger Transport', 'Industrial Production Index', 'Retail Trade Turnover',
                       'Energy Prices'],
        "scatter_pairs": [('Inflation (HICP Manufacturing)', 'Freight Transport'),
                          ('Inflation (HICP Manufacturing)', 'Air Passenger Transport'),
                          ('Inflation (HICP Manufacturing)', 'Road Passenger Transport')]
    }
}

# === Improved visual style ===
sns.set_theme(style="whitegrid", palette="Set2")
plt.rcParams.update({
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10
})

# === Function to generate plots for a given RQ ===
def generate_eda_plots(df, rq_name, indicators, scatter_pairs, combined=None):
    rq_dir = os.path.join(output_dir, rq_name)
    os.makedirs(rq_dir, exist_ok=True)

    # Time Series Plots (individual)
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

    # Combined Time Series (for RQ1)
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

    # Scatter Plots
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

    # Correlation Heatmap
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

# === Generate plots for all RQs ===
for rq_name, rq_info in RQs.items():
    generate_eda_plots(df, rq_name, rq_info['indicators'], rq_info['scatter_pairs'], rq_info.get('combined'))

print(f"🎯 EDA plots for all RQs saved in {output_dir}")
