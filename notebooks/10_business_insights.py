import pandas as pd


# ==========================================
# 1. LOAD ANALYSIS FILES
# ==========================================

product = pd.read_csv(
    "outputs/product_profitability_analysis.csv"
)

division = pd.read_csv(
    "outputs/division_profitability_analysis.csv"
)

monthly = pd.read_csv(
    "outputs/monthly_trend_analysis.csv"
)

factory = pd.read_csv(
    "outputs/factory_profitability_analysis.csv"
)

risk = pd.read_csv(
    "outputs/margin_risk_analysis.csv"
)

pareto = pd.read_csv(
    "outputs/pareto_profit_analysis.csv"
)


# ==========================================
# 2. PRODUCT INSIGHTS
# ==========================================

top_profit_product = product.loc[
    product["Gross_Profit"].idxmax()
]

top_margin_product = product.loc[
    product["Gross_Margin_%"].idxmax()
]

lowest_margin_product = product.loc[
    product["Gross_Margin_%"].idxmin()
]


# ==========================================
# 3. DIVISION INSIGHTS
# ==========================================

top_sales_division = division.loc[
    division["Total_Sales"].idxmax()
]

top_profit_division = division.loc[
    division["Gross_Profit"].idxmax()
]

top_margin_division = division.loc[
    division["Gross_Margin_%"].idxmax()
]


# ==========================================
# 4. TREND INSIGHTS
# ==========================================

best_sales_month = monthly.loc[
    monthly["Total_Sales"].idxmax()
]

best_profit_month = monthly.loc[
    monthly["Total_Profit"].idxmax()
]

best_margin_month = monthly.loc[
    monthly["Gross_Margin_%"].idxmax()
]

lowest_margin_month = monthly.loc[
    monthly["Gross_Margin_%"].idxmin()
]


# ==========================================
# 5. FACTORY INSIGHTS
# ==========================================

top_factory_profit = factory.loc[
    factory["Total_Profit"].idxmax()
]

top_factory_margin = factory.loc[
    factory["Gross_Margin_%"].idxmax()
]

lowest_factory_margin = factory.loc[
    factory["Gross_Margin_%"].idxmin()
]


# ==========================================
# 6. RISK INSIGHTS
# ==========================================

high_sales_low_margin = risk[
    risk["Performance_Category"]
    == "High Sales / Low Margin"
]

low_sales_low_margin = risk[
    risk["Performance_Category"]
    == "Low Sales / Low Margin"
]


# ==========================================
# 7. PRINT BUSINESS INSIGHTS
# ==========================================

print("\n")
print("=" * 60)
print("        NASSAU CANDY BUSINESS INSIGHTS")
print("=" * 60)


print("\n1. PRODUCT PROFITABILITY")
print("-" * 60)

print(
    f"Highest profit product: "
    f"{top_profit_product['Product Name']}"
)

print(
    f"Gross profit: "
    f"${top_profit_product['Gross_Profit']:,.2f}"
)

print(
    f"Highest margin product: "
    f"{top_margin_product['Product Name']}"
)

print(
    f"Gross margin: "
    f"{top_margin_product['Gross_Margin_%']:.2f}%"
)

print(
    f"Lowest margin product: "
    f"{lowest_margin_product['Product Name']}"
)

print(
    f"Gross margin: "
    f"{lowest_margin_product['Gross_Margin_%']:.2f}%"
)


print("\n2. DIVISION PERFORMANCE")
print("-" * 60)

print(
    f"Highest sales division: "
    f"{top_sales_division['Division']}"
)

print(
    f"Sales: "
    f"${top_sales_division['Total_Sales']:,.2f}"
)

print(
    f"Highest profit division: "
    f"{top_profit_division['Division']}"
)

print(
    f"Profit: "
    f"${top_profit_division['Gross_Profit']:,.2f}"
)

print(
    f"Highest margin division: "
    f"{top_margin_division['Division']}"
)

print(
    f"Margin: "
    f"{top_margin_division['Gross_Margin_%']:.2f}%"
)


print("\n3. TREND ANALYSIS")
print("-" * 60)

print(
    f"Best sales month: "
    f"{best_sales_month['Year_Month']}"
)

print(
    f"Sales: "
    f"${best_sales_month['Total_Sales']:,.2f}"
)

print(
    f"Best profit month: "
    f"{best_profit_month['Year_Month']}"
)

print(
    f"Profit: "
    f"${best_profit_month['Total_Profit']:,.2f}"
)

print(
    f"Best margin month: "
    f"{best_margin_month['Year_Month']}"
)

print(
    f"Margin: "
    f"{best_margin_month['Gross_Margin_%']:.2f}%"
)

print(
    f"Lowest margin month: "
    f"{lowest_margin_month['Year_Month']}"
)

print(
    f"Margin: "
    f"{lowest_margin_month['Gross_Margin_%']:.2f}%"
)


print("\n4. FACTORY PERFORMANCE")
print("-" * 60)

print(
    f"Highest profit factory: "
    f"{top_factory_profit['Factory']}"
)

print(
    f"Profit: "
    f"${top_factory_profit['Total_Profit']:,.2f}"
)

print(
    f"Highest margin factory: "
    f"{top_factory_margin['Factory']}"
)

print(
    f"Margin: "
    f"{top_factory_margin['Gross_Margin_%']:.2f}%"
)

print(
    f"Lowest margin factory: "
    f"{lowest_factory_margin['Factory']}"
)

print(
    f"Margin: "
    f"{lowest_factory_margin['Gross_Margin_%']:.2f}%"
)


print("\n5. MARGIN RISK")
print("-" * 60)

print(
    "High Sales / Low Margin products:",
    len(high_sales_low_margin)
)

if len(high_sales_low_margin) > 0:

    print("\nProducts requiring pricing/cost review:")

    for product_name in high_sales_low_margin[
        "Product Name"
    ]:
        print("-", product_name)


print(
    "\nLow Sales / Low Margin products:",
    len(low_sales_low_margin)
)


# ==========================================
# 8. PARETO RESULT
# ==========================================

print("\n6. PARETO ANALYSIS")
print("-" * 60)

total_products = len(pareto)

pareto_80 = pareto[
    pareto["Cumulative_Profit_%"] <= 80
]

print(
    "Total products analyzed:",
    total_products
)

print(
    "Products contributing to first 80%:",
    len(pareto_80)
)


# ==========================================
# 9. RECOMMENDATIONS
# ==========================================

print("\n7. BUSINESS RECOMMENDATIONS")
print("-" * 60)

print(
    "1. Protect and prioritize high-profit products."
)

print(
    "2. Review pricing and manufacturing costs "
    "for high-sales / low-margin products."
)

print(
    "3. Investigate low-sales / low-margin products "
    "for repositioning or discontinuation."
)

print(
    "4. Focus inventory and marketing on products "
    "that contribute strongly to total profit."
)

print(
    "5. Investigate periods where gross margin "
    "declines despite strong sales."
)

print(
    "6. Compare factory-level costs and margins "
    "to identify operational inefficiencies."
)

print(
    "7. Use Pareto results to focus management "
    "attention on the products driving most profit."
)


print("\n")
print("=" * 60)
print("       BUSINESS INSIGHT ANALYSIS COMPLETE")
print("=" * 60)