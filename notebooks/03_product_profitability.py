import pandas as pd

# ==========================================
# 1. LOAD CLEANED DATA
# ==========================================

file_path = "data/Nassau Candy Distributor_Cleaned.csv"

df = pd.read_csv(file_path)


# ==========================================
# 2. CREATE PRODUCT-LEVEL SUMMARY
# ==========================================

product_summary = (
    df.groupby(["Product ID", "Product Name"], as_index=False)
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Cost=("Cost", "sum"),
        Total_Units=("Units", "sum"),
        Gross_Profit=("Gross Profit", "sum")
    )
)


# ==========================================
# 3. CALCULATE GROSS MARGIN %
# ==========================================

product_summary["Gross_Margin_%"] = (
    product_summary["Gross_Profit"]
    / product_summary["Total_Sales"]
    * 100
)


# ==========================================
# 4. CALCULATE PROFIT PER UNIT
# ==========================================

product_summary["Profit_Per_Unit"] = (
    product_summary["Gross_Profit"]
    / product_summary["Total_Units"]
)


# ==========================================
# 5. CALCULATE REVENUE CONTRIBUTION %
# ==========================================

total_sales = product_summary["Total_Sales"].sum()

product_summary["Revenue_Contribution_%"] = (
    product_summary["Total_Sales"]
    / total_sales
    * 100
)


# ==========================================
# 6. CALCULATE PROFIT CONTRIBUTION %
# ==========================================

total_profit = product_summary["Gross_Profit"].sum()

product_summary["Profit_Contribution_%"] = (
    product_summary["Gross_Profit"]
    / total_profit
    * 100
)


# ==========================================
# 7. SORT BY PROFIT
# ==========================================

product_summary = product_summary.sort_values(
    by="Gross_Profit",
    ascending=False
)


# ==========================================
# 8. DISPLAY TOP 10 PRODUCTS BY PROFIT
# ==========================================

print("\n========== TOP 10 PRODUCTS BY GROSS PROFIT ==========")

print(
    product_summary[
        [
            "Product Name",
            "Total_Sales",
            "Total_Cost",
            "Total_Units",
            "Gross_Profit",
            "Gross_Margin_%",
            "Profit_Per_Unit"
        ]
    ].head(10).to_string(index=False)
)


# ==========================================
# 9. TOP 10 PRODUCTS BY GROSS MARGIN
# ==========================================

print("\n========== TOP 10 PRODUCTS BY GROSS MARGIN ==========")

top_margin = product_summary.sort_values(
    by="Gross_Margin_%",
    ascending=False
)

print(
    top_margin[
        [
            "Product Name",
            "Total_Sales",
            "Gross_Profit",
            "Gross_Margin_%",
            "Profit_Per_Unit"
        ]
    ].head(10).to_string(index=False)
)


# ==========================================
# 10. LOWEST MARGIN PRODUCTS
# ==========================================

print("\n========== LOWEST 10 PRODUCTS BY GROSS MARGIN ==========")

low_margin = product_summary.sort_values(
    by="Gross_Margin_%",
    ascending=True
)

print(
    low_margin[
        [
            "Product Name",
            "Total_Sales",
            "Gross_Profit",
            "Gross_Margin_%",
            "Profit_Per_Unit"
        ]
    ].head(10).to_string(index=False)
)


# ==========================================
# 11. SAVE PRODUCT ANALYSIS
# ==========================================

output_file = "outputs/product_profitability_analysis.csv"

product_summary.to_csv(
    output_file,
    index=False
)

print("\n========== OUTPUT ==========")

print("Product analysis saved to:")
print(output_file)

print("\nNumber of products analyzed:", len(product_summary))