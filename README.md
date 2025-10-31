# **Exploratory Data Analysis — Latvia**
**Author:** *Igor Latii*  
**Course:** *European Development Indicators (Alexandru Monahov, 2025)*  

---

## 🧭 **Project Overview**

This project analyzes key **economic**, **transport**, and **demographic** indicators of **Latvia (LV)** using data from **Eurostat** and the **World Bank**.  
The goal is to explore **macroeconomic relationships**, identify **trends**, and visualize **correlations** among major indicators.

### 🎯 **Research Questions**

1. **RQ1:** How has the evolution of external trade and passenger flows correlated with Latvia’s GDP and overall economic activity?  
2. **RQ2:** What is the relationship between unemployment, migration, and international departures of Latvian residents?  
3. **RQ3:** How do freight and passenger transport volumes relate to inflation?

---

## 📁 **Project Structure**
```
├── /data
│   ├── /raw/                             # Original Eurostat & World Bank datasets
│   ├── /processed/
│   │   ├── /transformed_to_long_format/  # Converted from wide to long format
│   │   ├── /formatted_time_periods/      # Cleaned and harmonized datasets
│   │   └── /merged/                      # Merged & aggregated CSV files
│   └── /eda_plots/                       # Visual outputs (RQ1–RQ3)
│
├── /reports/
│   ├── indicators.csv / indicators.xlsx  # Selected indicators and metadata
│   └── final_report.pdf                  # Comprehensive report with analysis
│
├── /src/
│   ├── collecting_data.py
│   ├── transform_to_long_format_EStat.py
│   ├── transform_to_long_format_WB.py
│   ├── format_time_periods.py
│   ├── make_merged_df.py
│   ├── aggregate_annual_indicators.py
│   └── eda_visualization.py
│
└── README.md
```

---

## ⚙️ **Execution Workflow**

### **1️⃣ Data Collection**
- **Script:** `collecting_data.py`  
- Downloads all selected indicators for Latvia (`geo = LV`) from:
  - Eurostat API  
  - World Bank Open Data (for *Net Migration* manually)  
- **Output:** `/data/raw/*.csv`

---

### **2️⃣ Transformation to Long Format**
- **Scripts:**  
  - `transform_to_long_format_EStat.py`  
  - `transform_to_long_format_WB.py`
- Converts wide tables (years as columns) to long format with standardized columns:  
  `TIME_PERIOD`, `VALUE`, and metadata fields.
- **Output:** `/data/processed/transformed_to_long_format/`

---

### **3️⃣ Formatting and Cleaning**
- **Script:** `format_time_periods.py`
- Standardizes time formats (YYYY, YYYY-MM, YYYY-Qn, YYYY-Sn → `datetime`).
- Removes missing and zero values.
- **Output:** `/data/processed/formatted_time_periods/`

---

### **4️⃣ Merging All Indicators**
- **Script:** `make_merged_df.py`
- Aggregates values per `TIME_PERIOD`, renames indicators to readable names,  
  and merges datasets using **outer join** to avoid data loss.
- **Output:** `/data/processed/merged/merged_df_readable.csv`

---

### **5️⃣ Annual Aggregation**
- **Script:** `aggregate_annual_indicators.py`
- Converts mixed-frequency data (monthly/quarterly/annual) to **annual format**.

| Indicator Type | Operation | Examples |
|----------------|------------|-----------|
| Continuous | Summed | GDP, Exports, Transport, Energy Prices |
| Discrete | Averaged | Unemployment, Migration, Emigration |
| Interpolation | Linear | Applied to continuous indicators |
| Non-interpolated | Preserved | Event-based indicators |

- **Output:** `/data/processed/merged/merged_df_annual.csv`

---

### **6️⃣ Exploratory Data Analysis (EDA)**
- **Script:** `eda_visualization.py`  
- Automatically generates plots for each RQ:
  - 📈 *Time series plots* — show long-term trends  
  - 🔹 *Scatter plots* — visualize pairwise correlations  
  - 🔥 *Correlation heatmaps* — quantify variable relationships  
  - 📊 *Combined plots* (GDP, Exports, Air Transport for RQ1)

- **Output:** `/data/eda_plots/RQ1_RQ2_RQ3/`

---

## 🧩 **How to Run**

### **Setup Environment**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd src
python collecting_data.py
python transform_to_long_format_EStat.py
python transform_to_long_format_WB.py
python format_time_periods.py
python make_merged_df.py
python aggregate_annual_indicators.py
python eda_visualization.py
```
---

## 📊 Outputs

| Step | Output | Description |
|------|---------|-------------|
| **Data Collection** | `/data/raw/*.csv` | Raw Eurostat & World Bank datasets |
| **Long Format** | `/data/processed/transformed_to_long_format/*.csv` | Unified structure (tidy format) |
| **Cleaned Data** | `/data/processed/formatted_time_periods/*.csv` | Cleaned & time-formatted datasets |
| **Merged Data** | `/data/processed/merged/merged_df_readable.csv` | All indicators combined into a single dataset |
| **Annual Data** | `/data/processed/merged/merged_df_annual.csv` | Harmonized annual dataset for EDA |
| **EDA Visuals** | `/data/eda_plots/` | Time series, scatter plots, and correlation heatmaps (RQ1–RQ3) |

---

## 🔁 Reproducibility

- All scripts are **fully modular**, **commented**, and can be executed independently.  
- The workflow can be **re-run end-to-end** from raw data to visual outputs.  
- Compatible with **Python ≥ 3.10** (tested on Windows & Linux).  
- Final results are deterministic – re-running the pipeline produces **identical outputs**.

---

## 🧠 Notes

- Focused on **macroeconomic relationships**: GDP, trade, transport, inflation, migration, labor.  
- Category-level details (e.g., gender, transport type) were **aggregated** for clarity and comparability.  
- The final analytical report (`/reports/final_report.pdf`) provides interpretation and context for all RQs.  

---

✅ **Ready for submission:**  
This pipeline delivers a **complete, transparent, and reproducible analysis** —  
from **data acquisition** to **EDA visualization** and **report interpretation**.
