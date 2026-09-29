from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "retail_sales.csv"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA_FILE, parse_dates=["Order_Date"])

print("\n--- DATASET OVERVIEW ---")
print("Rows:", len(df))
print("Columns:", len(df.columns))
print("\nData types:")
print(df.dtypes)
print("\nMissing values:")
print(df.isna().sum())
print("\nDuplicate rows:", df.duplicated().sum())

numeric_cols = df.select_dtypes(include="number").columns
stats = df[numeric_cols].describe().T
stats["median"] = df[numeric_cols].median()
stats.to_csv(OUTPUT_DIR / "descriptive_statistics.csv")
print("\n--- DESCRIPTIVE STATISTICS ---")
print(stats.round(2))

product_summary = (df.groupby("Product")
    .agg(Orders=("Product", "size"), Quantity=("Quantity", "sum"),
         Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    .sort_values("Sales", ascending=False))
product_summary.to_csv(OUTPUT_DIR / "product_summary.csv")

region_summary = (df.groupby("Region", dropna=False)
    .agg(Orders=("Region", "size"), Sales=("Sales", "sum"),
         Profit=("Profit", "sum"))
    .sort_values("Sales", ascending=False))
region_summary.to_csv(OUTPUT_DIR / "region_summary.csv")

df["Month"] = df["Order_Date"].dt.to_period("M").astype(str)
monthly = df.groupby("Month")[["Sales", "Profit"]].sum()
monthly.to_csv(OUTPUT_DIR / "monthly_summary.csv")

correlation = df[numeric_cols].corr(numeric_only=True)
correlation.to_csv(OUTPUT_DIR / "correlation_matrix.csv")

def find_outliers(data, column):
    q1 = data[column].quantile(.25)
    q3 = data[column].quantile(.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    mask = (data[column] < lower) | (data[column] > upper)
    return data.loc[mask].copy(), lower, upper

frames = []
limits = []
for column in ["Quantity", "Sales", "Profit"]:
    found, lower, upper = find_outliers(df, column)
    found["Outlier_Variable"] = column
    frames.append(found)
    limits.append([column, lower, upper, len(found)])

pd.concat(frames, ignore_index=True).to_csv(OUTPUT_DIR / "outliers.csv", index=False)
pd.DataFrame(limits, columns=["Variable", "Lower_Bound", "Upper_Bound", "Outlier_Count"]).to_csv(
    OUTPUT_DIR / "outlier_summary.csv", index=False)

# Charts
monthly["Sales"].plot(figsize=(10,5), marker="o", title="Monthly Sales Trend")
plt.xlabel("Month"); plt.ylabel("Sales"); plt.xticks(rotation=45); plt.tight_layout()
plt.savefig(OUTPUT_DIR / "01_monthly_sales.png", dpi=150); plt.close()

product_summary["Sales"].sort_values().plot(kind="barh", figsize=(10,5), title="Sales by Product")
plt.xlabel("Sales"); plt.ylabel("Product"); plt.tight_layout()
plt.savefig(OUTPUT_DIR / "02_sales_by_product.png", dpi=150); plt.close()

region_summary["Sales"].plot(kind="bar", figsize=(8,5), title="Sales by Region")
plt.xlabel("Region"); plt.ylabel("Sales"); plt.xticks(rotation=0); plt.tight_layout()
plt.savefig(OUTPUT_DIR / "03_sales_by_region.png", dpi=150); plt.close()

df["Sales"].plot(kind="hist", bins=30, figsize=(9,5), title="Distribution of Sales")
plt.xlabel("Sales"); plt.ylabel("Number of Orders"); plt.tight_layout()
plt.savefig(OUTPUT_DIR / "04_sales_distribution.png", dpi=150); plt.close()

df.boxplot(column="Quantity", figsize=(8,5))
plt.title("Quantity Distribution and Outliers"); plt.ylabel("Quantity"); plt.tight_layout()
plt.savefig(OUTPUT_DIR / "05_quantity_boxplot.png", dpi=150); plt.close()

plt.figure(figsize=(8,5))
plt.scatter(df["Sales"], df["Profit"], alpha=.55)
plt.title("Sales vs Profit"); plt.xlabel("Sales"); plt.ylabel("Profit"); plt.tight_layout()
plt.savefig(OUTPUT_DIR / "06_sales_vs_profit.png", dpi=150); plt.close()

plt.figure(figsize=(9,7))
plt.imshow(correlation, aspect="auto")
plt.colorbar(label="Correlation")
plt.xticks(range(len(correlation.columns)), correlation.columns, rotation=45, ha="right")
plt.yticks(range(len(correlation.index)), correlation.index)
plt.title("Correlation Matrix"); plt.tight_layout()
plt.savefig(OUTPUT_DIR / "07_correlation_matrix.png", dpi=150); plt.close()

print("\nAnalysis completed. Check the output folder for tables, charts and the findings report.")
