import pandas as pd
import matplotlib.pyplot as plt
import os


# ==========================================
# 1. LOAD PRODUCT PROFITABILITY DATA
# ==========================================

file_path = "outputs/product_profitability_analysis.csv"

df = pd.read_csv(file_path)


# ==========================================
# 2. SORT PRODUCTS BY PROFIT
# ==========================================

df = df.sort_values(
    by="Gross_Profit",
    ascending=False
).reset_index(drop=True)


# ==========================================
# 3. CALCULATE CUMULATIVE PROFIT
# ==========================================

total_profit = df["Gross_Profit"].sum()

df["Cumulative_Profit"] = df["Gross_Profit"].cumsum()


# ==========================================
# 4. CALCULATE CUMULATIVE PROFIT %
# ==========================================

df["Cumulative_Profit_%"] = (
    df["Cumulative_Profit"]
    / total_profit
    * 100
)


# ==========================================
# 5. IDENTIFY PRODUCTS CONTRIBUTING
#    TO FIRST 80% OF PROFIT
# ==========================================

pareto_products = df[
    df["Cumulative_Profit_%"] <= 80
].copy()


# Include the first product that crosses 80%
crossing_products = df[
    df["Cumulative_Profit_%"] > 80
].head(1)

pareto_products = pd.concat(
    [pareto_products, crossing_products]
).drop_duplicates()


# ==========================================
# 6. DISPLAY PARETO TABLE
# ==========================================

print("\n========== PARETO PROFIT ANALYSIS ==========")

print(
    df[
        [
            "Product Name",
            "Gross_Profit",
            "Profit_Contribution_%",
            "Cumulative_Profit_%"
        ]
    ].to_string(index=False)
)


# ==========================================
# 7. DISPLAY 80% PROFIT PRODUCTS
# ==========================================

print("\n========== PRODUCTS CONTRIBUTING TO ~80% OF PROFIT ==========")

print(
    pareto_products[
        [
            "Product Name",
            "Gross_Profit",
            "Profit_Contribution_%",
            "Cumulative_Profit_%"
        ]
    ].to_string(index=False)
)


# ==========================================
# 8. CALCULATE PERCENTAGE OF PRODUCTS
# ==========================================

number_of_products = len(df)

number_for_80_percent = len(pareto_products)

product_percentage = (
    number_for_80_percent
    / number_of_products
    * 100
)


print("\n========== PARETO SUMMARY ==========")

print(
    "Total products:",
    number_of_products
)

print(
    "Products needed to reach ~80% profit:",
    number_for_80_percent
)

print(
    f"Percentage of products: {product_percentage:.2f}%"
)


# ==========================================
# 9. CREATE CHART FOLDER
# ==========================================

os.makedirs(
    "outputs/charts",
    exist_ok=True
)


# ==========================================
# 10. CREATE PARETO CHART
# ==========================================

fig, ax1 = plt.subplots(
    figsize=(14, 7)
)


# Bar chart — profit

ax1.bar(
    df["Product Name"],
    df["Gross_Profit"]
)

ax1.set_xlabel(
    "Product"
)

ax1.set_ylabel(
    "Gross Profit"
)

ax1.tick_params(
    axis="x",
    rotation=75
)


# ==========================================
# 11. CUMULATIVE PROFIT LINE
# ==========================================

ax2 = ax1.twinx()

ax2.plot(
    df["Product Name"],
    df["Cumulative_Profit_%"],
    marker="o"
)

ax2.set_ylabel(
    "Cumulative Profit (%)"
)

ax2.axhline(
    80,
    linestyle="--"
)


# ==========================================
# 12. CHART TITLE
# ==========================================

plt.title(
    "Pareto Analysis — Product Profit Contribution"
)

plt.tight_layout()


# ==========================================
# 13. SAVE CHART
# ==========================================

output_chart = (
    "outputs/charts/pareto_profit_analysis.png"
)

plt.savefig(
    output_chart,
    dpi=300
)

plt.close()


# ==========================================
# 14. SAVE PARETO DATA
# ==========================================

output_csv = (
    "outputs/pareto_profit_analysis.csv"
)

df.to_csv(
    output_csv,
    index=False
)


# ==========================================
# 15. COMPLETION MESSAGE
# ==========================================

print("\n========== OUTPUT ==========")

print(
    "Pareto data saved to:",
    output_csv
)

print(
    "Pareto chart saved to:",
    output_chart
)

print("\nPareto analysis completed successfully.")