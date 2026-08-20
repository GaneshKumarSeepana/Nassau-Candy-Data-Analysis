import pandas as pd

# ==========================================
# 1. LOAD CLEANED DATA
# ==========================================

file_path = "data/Nassau Candy Distributor_Cleaned.csv"

df = pd.read_csv(file_path)


# ==========================================
# 2. CONVERT ORDER DATE
# ==========================================

df["Order Date"] = pd.to_datetime(
    df["Order Date"]
)


# ==========================================
# 3. CREATE TIME COLUMNS
# ==========================================

df["Year"] = df["Order Date"].dt.year

df["Month"] = df["Order Date"].dt.month

df["Month_Name"] = df["Order Date"].dt.month_name()

df["Year_Month"] = (
    df["Order Date"]
    .dt.to_period("M")
    .astype(str)
)


# ==========================================
# 4. MONTHLY TREND ANALYSIS
# ==========================================

monthly_trend = (
    df.groupby("Year_Month", as_index=False)
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Cost=("Cost", "sum"),
        Total_Profit=("Gross Profit", "sum"),
        Total_Units=("Units", "sum"),
        Order_Count=("Order ID", "nunique")
    )
)


# ==========================================
# 5. MONTHLY GROSS MARGIN
# ==========================================

monthly_trend["Gross_Margin_%"] = (
    monthly_trend["Total_Profit"]
    / monthly_trend["Total_Sales"]
    * 100
)


# ==========================================
# 6. SORT CHRONOLOGICALLY
# ==========================================

monthly_trend = monthly_trend.sort_values(
    "Year_Month"
)


# ==========================================
# 7. DISPLAY MONTHLY TREND
# ==========================================

print("\n========== MONTHLY TREND ==========")

print(
    monthly_trend.to_string(index=False)
)


# ==========================================
# 8. YEARLY TREND
# ==========================================

yearly_trend = (
    df.groupby("Year", as_index=False)
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Cost=("Cost", "sum"),
        Total_Profit=("Gross Profit", "sum"),
        Total_Units=("Units", "sum"),
        Order_Count=("Order ID", "nunique")
    )
)


# ==========================================
# 9. YEARLY GROSS MARGIN
# ==========================================

yearly_trend["Gross_Margin_%"] = (
    yearly_trend["Total_Profit"]
    / yearly_trend["Total_Sales"]
    * 100
)


# ==========================================
# 10. DISPLAY YEARLY TREND
# ==========================================

print("\n========== YEARLY TREND ==========")

print(
    yearly_trend.to_string(index=False)
)


# ==========================================
# 11. BEST MONTH BY SALES
# ==========================================

best_sales_month = monthly_trend.loc[
    monthly_trend["Total_Sales"].idxmax()
]

print("\n========== BEST MONTH BY SALES ==========")

print(
    "Month:",
    best_sales_month["Year_Month"]
)

print(
    f"Sales: ₹{best_sales_month['Total_Sales']:,.2f}"
)


# ==========================================
# 12. BEST MONTH BY PROFIT
# ==========================================

best_profit_month = monthly_trend.loc[
    monthly_trend["Total_Profit"].idxmax()
]

print("\n========== BEST MONTH BY PROFIT ==========")

print(
    "Month:",
    best_profit_month["Year_Month"]
)

print(
    f"Profit: ₹{best_profit_month['Total_Profit']:,.2f}"
)


# ==========================================
# 13. BEST MONTH BY MARGIN
# ==========================================

best_margin_month = monthly_trend.loc[
    monthly_trend["Gross_Margin_%"].idxmax()
]

print("\n========== BEST MONTH BY MARGIN ==========")

print(
    "Month:",
    best_margin_month["Year_Month"]
)

print(
    f"Margin: {best_margin_month['Gross_Margin_%']:.2f}%"
)


# ==========================================
# 14. LOWEST MARGIN MONTH
# ==========================================

lowest_margin_month = monthly_trend.loc[
    monthly_trend["Gross_Margin_%"].idxmin()
]

print("\n========== LOWEST MONTH BY MARGIN ==========")

print(
    "Month:",
    lowest_margin_month["Year_Month"]
)

print(
    f"Margin: {lowest_margin_month['Gross_Margin_%']:.2f}%"
)


# ==========================================
# 15. SAVE MONTHLY TREND
# ==========================================

monthly_output = (
    "outputs/monthly_trend_analysis.csv"
)

monthly_trend.to_csv(
    monthly_output,
    index=False
)


# ==========================================
# 16. SAVE YEARLY TREND
# ==========================================

yearly_output = (
    "outputs/yearly_trend_analysis.csv"
)

yearly_trend.to_csv(
    yearly_output,
    index=False
)


print("\n========== OUTPUT ==========")

print(
    "Monthly trend saved to:",
    monthly_output
)

print(
    "Yearly trend saved to:",
    yearly_output
)