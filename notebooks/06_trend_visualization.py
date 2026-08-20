import pandas as pd
import matplotlib.pyplot as plt


# ==========================================
# 1. LOAD MONTHLY TREND DATA
# ==========================================

file_path = "outputs/monthly_trend_analysis.csv"

df = pd.read_csv(file_path)


# ==========================================
# 2. CREATE CHART OUTPUT FOLDER
# ==========================================

import os

os.makedirs("outputs/charts", exist_ok=True)


# ==========================================
# 3. MONTHLY SALES TREND
# ==========================================

plt.figure(figsize=(12, 6))

plt.plot(
    df["Year_Month"],
    df["Total_Sales"],
    marker="o"
)

plt.title("Monthly Sales Trend")

plt.xlabel("Month")

plt.ylabel("Total Sales")

plt.xticks(rotation=45)

plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    "outputs/charts/monthly_sales_trend.png",
    dpi=300
)

plt.close()


# ==========================================
# 4. MONTHLY PROFIT TREND
# ==========================================

plt.figure(figsize=(12, 6))

plt.plot(
    df["Year_Month"],
    df["Total_Profit"],
    marker="o"
)

plt.title("Monthly Gross Profit Trend")

plt.xlabel("Month")

plt.ylabel("Gross Profit")

plt.xticks(rotation=45)

plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    "outputs/charts/monthly_profit_trend.png",
    dpi=300
)

plt.close()


# ==========================================
# 5. MONTHLY GROSS MARGIN TREND
# ==========================================

plt.figure(figsize=(12, 6))

plt.plot(
    df["Year_Month"],
    df["Gross_Margin_%"],
    marker="o"
)

plt.title("Monthly Gross Margin Trend")

plt.xlabel("Month")

plt.ylabel("Gross Margin (%)")

plt.xticks(rotation=45)

plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    "outputs/charts/monthly_margin_trend.png",
    dpi=300
)

plt.close()


# ==========================================
# 6. MONTHLY UNITS SOLD TREND
# ==========================================

plt.figure(figsize=(12, 6))

plt.plot(
    df["Year_Month"],
    df["Total_Units"],
    marker="o"
)

plt.title("Monthly Units Sold Trend")

plt.xlabel("Month")

plt.ylabel("Total Units")

plt.xticks(rotation=45)

plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    "outputs/charts/monthly_units_trend.png",
    dpi=300
)

plt.close()


# ==========================================
# 7. COMPLETION MESSAGE
# ==========================================

print("\n========== TREND VISUALIZATION COMPLETE ==========")

print("Charts created successfully.")

print("\nSaved charts:")

print("1. outputs/charts/monthly_sales_trend.png")

print("2. outputs/charts/monthly_profit_trend.png")

print("3. outputs/charts/monthly_margin_trend.png")

print("4. outputs/charts/monthly_units_trend.png")