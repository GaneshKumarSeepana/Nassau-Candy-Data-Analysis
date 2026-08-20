import pandas as pd

# ==========================================
# 1. LOAD CLEANED DATA
# ==========================================

file_path = "data/Nassau Candy Distributor_Cleaned.csv"

df = pd.read_csv(file_path)


# ==========================================
# 2. CREATE DIVISION SUMMARY
# ==========================================

division_summary = (
    df.groupby("Division", as_index=False)
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Cost=("Cost", "sum"),
        Total_Units=("Units", "sum"),
        Gross_Profit=("Gross Profit", "sum"),
        Order_Count=("Order ID", "nunique"),
        Product_Count=("Product ID", "nunique")
    )
)


# ==========================================
# 3. CALCULATE GROSS MARGIN %
# ==========================================

division_summary["Gross_Margin_%"] = (
    division_summary["Gross_Profit"]
    / division_summary["Total_Sales"]
    * 100
)


# ==========================================
# 4. CALCULATE PROFIT PER UNIT
# ==========================================

division_summary["Profit_Per_Unit"] = (
    division_summary["Gross_Profit"]
    / division_summary["Total_Units"]
)


# ==========================================
# 5. REVENUE CONTRIBUTION %
# ==========================================

total_sales = division_summary["Total_Sales"].sum()

division_summary["Revenue_Contribution_%"] = (
    division_summary["Total_Sales"]
    / total_sales
    * 100
)


# ==========================================
# 6. PROFIT CONTRIBUTION %
# ==========================================

total_profit = division_summary["Gross_Profit"].sum()

division_summary["Profit_Contribution_%"] = (
    division_summary["Gross_Profit"]
    / total_profit
    * 100
)


# ==========================================
# 7. SORT BY PROFIT
# ==========================================

division_summary = division_summary.sort_values(
    by="Gross_Profit",
    ascending=False
)


# ==========================================
# 8. DISPLAY DIVISION SUMMARY
# ==========================================

print("\n========== DIVISION PROFITABILITY ==========")

print(
    division_summary.to_string(index=False)
)


# ==========================================
# 9. BEST DIVISION BY SALES
# ==========================================

best_sales = division_summary.loc[
    division_summary["Total_Sales"].idxmax()
]

print("\n========== HIGHEST SALES DIVISION ==========")

print("Division:", best_sales["Division"])
print(
    f"Sales: ₹{best_sales['Total_Sales']:,.2f}"
)


# ==========================================
# 10. BEST DIVISION BY PROFIT
# ==========================================

best_profit = division_summary.loc[
    division_summary["Gross_Profit"].idxmax()
]

print("\n========== HIGHEST PROFIT DIVISION ==========")

print("Division:", best_profit["Division"])
print(
    f"Profit: ₹{best_profit['Gross_Profit']:,.2f}"
)


# ==========================================
# 11. BEST DIVISION BY MARGIN
# ==========================================

best_margin = division_summary.loc[
    division_summary["Gross_Margin_%"].idxmax()
]

print("\n========== HIGHEST MARGIN DIVISION ==========")

print("Division:", best_margin["Division"])
print(
    f"Gross Margin: {best_margin['Gross_Margin_%']:.2f}%"
)


# ==========================================
# 12. SAVE DIVISION ANALYSIS
# ==========================================

output_file = "outputs/division_profitability_analysis.csv"

division_summary.to_csv(
    output_file,
    index=False
)

print("\n========== OUTPUT ==========")

print("Division analysis saved to:")
print(output_file)