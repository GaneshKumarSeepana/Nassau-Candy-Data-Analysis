import pandas as pd
import matplotlib.pyplot as plt
import os


# ==========================================
# 1. LOAD PRODUCT PROFITABILITY DATA
# ==========================================

file_path = "outputs/product_profitability_analysis.csv"

df = pd.read_csv(file_path)


# ==========================================
# 2. CREATE RISK CATEGORIES
# ==========================================

# Median values are used as a simple
# data-driven benchmark.

sales_median = df["Total_Sales"].median()

margin_median = df["Gross_Margin_%"].median()

cost_median = df["Total_Cost"].median()


# ==========================================
# 3. CLASSIFY PRODUCTS
# ==========================================

def classify_product(row):

    high_sales = row["Total_Sales"] >= sales_median
    high_margin = row["Gross_Margin_%"] >= margin_median
    high_cost = row["Total_Cost"] >= cost_median

    if high_sales and high_margin:
        return "High Sales / High Margin"

    elif high_sales and not high_margin:
        return "High Sales / Low Margin"

    elif not high_sales and high_margin:
        return "Low Sales / High Margin"

    else:
        return "Low Sales / Low Margin"


df["Performance_Category"] = df.apply(
    classify_product,
    axis=1
)


# ==========================================
# 4. IDENTIFY COST-HEAVY PRODUCTS
# ==========================================

df["Cost_to_Sales_%"] = (
    df["Total_Cost"]
    / df["Total_Sales"]
    * 100
)


# ==========================================
# 5. IDENTIFY MARGIN RISK
# ==========================================

df["Margin_Risk"] = df["Gross_Margin_%"] < margin_median


# ==========================================
# 6. DISPLAY PRODUCT RISK ANALYSIS
# ==========================================

print("\n========== PRODUCT PERFORMANCE CATEGORIES ==========")

print(
    df[
        [
            "Product Name",
            "Total_Sales",
            "Total_Cost",
            "Gross_Profit",
            "Gross_Margin_%",
            "Performance_Category"
        ]
    ]
    .sort_values(
        by="Gross_Margin_%",
        ascending=False
    )
    .to_string(index=False)
)


# ==========================================
# 7. HIGH SALES / LOW MARGIN PRODUCTS
# ==========================================

high_sales_low_margin = df[
    df["Performance_Category"]
    == "High Sales / Low Margin"
]


print(
    "\n========== HIGH SALES / LOW MARGIN =========="
)

print(
    high_sales_low_margin[
        [
            "Product Name",
            "Total_Sales",
            "Total_Cost",
            "Gross_Profit",
            "Gross_Margin_%",
            "Cost_to_Sales_%"
        ]
    ]
    .sort_values(
        by="Total_Sales",
        ascending=False
    )
    .to_string(index=False)
)


# ==========================================
# 8. LOW SALES / LOW MARGIN PRODUCTS
# ==========================================

low_sales_low_margin = df[
    df["Performance_Category"]
    == "Low Sales / Low Margin"
]


print(
    "\n========== LOW SALES / LOW MARGIN =========="
)

print(
    low_sales_low_margin[
        [
            "Product Name",
            "Total_Sales",
            "Total_Cost",
            "Gross_Profit",
            "Gross_Margin_%",
            "Cost_to_Sales_%"
        ]
    ]
    .sort_values(
        by="Gross_Margin_%",
        ascending=True
    )
    .to_string(index=False)
)


# ==========================================
# 9. COST-HEAVY PRODUCTS
# ==========================================

cost_heavy = df[
    df["Cost_to_Sales_%"] >= 80
]


print(
    "\n========== COST-HEAVY PRODUCTS =========="
)

print(
    cost_heavy[
        [
            "Product Name",
            "Total_Sales",
            "Total_Cost",
            "Cost_to_Sales_%",
            "Gross_Margin_%"
        ]
    ]
    .sort_values(
        by="Cost_to_Sales_%",
        ascending=False
    )
    .to_string(index=False)
)


# ==========================================
# 10. LOWEST MARGIN PRODUCTS
# ==========================================

lowest_margin = df.sort_values(
    by="Gross_Margin_%",
    ascending=True
).head(5)


print(
    "\n========== 5 LOWEST MARGIN PRODUCTS =========="
)

print(
    lowest_margin[
        [
            "Product Name",
            "Total_Sales",
            "Gross_Profit",
            "Gross_Margin_%",
            "Cost_to_Sales_%"
        ]
    ].to_string(index=False)
)


# ==========================================
# 11. CREATE CHART FOLDER
# ==========================================

os.makedirs(
    "outputs/charts",
    exist_ok=True
)


# ==========================================
# 12. COST VS SALES SCATTER PLOT
# ==========================================

plt.figure(figsize=(12, 7))

plt.scatter(
    df["Total_Sales"],
    df["Total_Cost"],
    s=100
)

plt.xlabel("Total Sales")

plt.ylabel("Total Cost")

plt.title(
    "Cost vs Sales Analysis"
)

plt.grid(
    True,
    alpha=0.3
)

plt.tight_layout()

plt.savefig(
    "outputs/charts/cost_vs_sales.png",
    dpi=300
)

plt.close()


# ==========================================
# 13. SALES VS MARGIN SCATTER PLOT
# ==========================================

plt.figure(figsize=(12, 7))

plt.scatter(
    df["Total_Sales"],
    df["Gross_Margin_%"],
    s=100
)

plt.xlabel("Total Sales")

plt.ylabel("Gross Margin (%)")

plt.title(
    "Sales vs Gross Margin Analysis"
)

plt.grid(
    True,
    alpha=0.3
)

plt.tight_layout()

plt.savefig(
    "outputs/charts/sales_vs_margin.png",
    dpi=300
)

plt.close()


# ==========================================
# 14. SAVE RISK ANALYSIS
# ==========================================

output_file = (
    "outputs/margin_risk_analysis.csv"
)

df.to_csv(
    output_file,
    index=False
)


# ==========================================
# 15. SUMMARY
# ==========================================

print(
    "\n========== RISK ANALYSIS SUMMARY =========="
)

print(
    "High Sales / Low Margin products:",
    len(high_sales_low_margin)
)

print(
    "Low Sales / Low Margin products:",
    len(low_sales_low_margin)
)

print(
    "Cost-heavy products:",
    len(cost_heavy)
)


# ==========================================
# 16. COMPLETION MESSAGE
# ==========================================

print(
    "\n========== OUTPUT =========="
)

print(
    "Risk analysis saved to:",
    output_file
)

print(
    "Cost vs Sales chart saved to:"
)

print(
    "outputs/charts/cost_vs_sales.png"
)

print(
    "Sales vs Margin chart saved to:"
)

print(
    "outputs/charts/sales_vs_margin.png"
)

print(
    "\nMargin risk analysis completed successfully."
)