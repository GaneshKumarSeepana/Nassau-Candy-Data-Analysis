import pandas as pd


# ==========================================
# 1. LOAD PRODUCT PROFITABILITY DATA
# ==========================================

file_path = "outputs/product_profitability_analysis.csv"

df = pd.read_csv(file_path)


# ==========================================
# 2. PRODUCT → FACTORY MAPPING
# ==========================================

product_factory = {
    "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows": "Lot's O' Nuts",
    "Wonka Bar - Scrumdiddlyumptious": "Lot's O' Nuts",

    "Wonka Bar - Milk Chocolate": "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel": "Wicked Choccy's",

    "Laffy Taffy": "Sugar Shack",
    "SweetTARTS": "Sugar Shack",
    "Nerds": "Sugar Shack",
    "Fun Dip": "Sugar Shack",

    "Fizzy Lifting Drinks": "Sugar Shack",

    "Everlasting Gobstopper": "Secret Factory",
    "Lickable Wallpaper": "Secret Factory",
    "Wonka Gum": "Secret Factory",

    "Hair Toffee": "The Other Factory",
    "Kazookles": "The Other Factory"
}


# ==========================================
# 3. ADD FACTORY COLUMN
# ==========================================

df["Factory"] = df["Product Name"].map(
    product_factory
)


# ==========================================
# 4. CHECK FOR UNMAPPED PRODUCTS
# ==========================================

unmapped = df[
    df["Factory"].isna()
]

if len(unmapped) > 0:

    print("\n========== WARNING ==========")

    print("Products without factory mapping:")

    print(
        unmapped["Product Name"]
        .to_string(index=False)
    )

else:

    print(
        "\nAll products successfully mapped to factories."
    )


# ==========================================
# 5. FACTORY-LEVEL SUMMARY
# ==========================================

factory_summary = (
    df.groupby("Factory", as_index=False)
    .agg(
        Total_Sales=("Total_Sales", "sum"),
        Total_Cost=("Total_Cost", "sum"),
        Total_Profit=("Gross_Profit", "sum"),
        Total_Units=("Total_Units", "sum"),
        Product_Count=("Product Name", "nunique")
    )
)


# ==========================================
# 6. GROSS MARGIN %
# ==========================================

factory_summary["Gross_Margin_%"] = (
    factory_summary["Total_Profit"]
    / factory_summary["Total_Sales"]
    * 100
)


# ==========================================
# 7. PROFIT PER UNIT
# ==========================================

factory_summary["Profit_Per_Unit"] = (
    factory_summary["Total_Profit"]
    / factory_summary["Total_Units"]
)


# ==========================================
# 8. REVENUE CONTRIBUTION %
# ==========================================

total_sales = factory_summary["Total_Sales"].sum()

factory_summary["Revenue_Contribution_%"] = (
    factory_summary["Total_Sales"]
    / total_sales
    * 100
)


# ==========================================
# 9. PROFIT CONTRIBUTION %
# ==========================================

total_profit = factory_summary["Total_Profit"].sum()

factory_summary["Profit_Contribution_%"] = (
    factory_summary["Total_Profit"]
    / total_profit
    * 100
)


# ==========================================
# 10. SORT BY PROFIT
# ==========================================

factory_summary = factory_summary.sort_values(
    by="Total_Profit",
    ascending=False
)


# ==========================================
# 11. DISPLAY FACTORY SUMMARY
# ==========================================

print("\n========== FACTORY PERFORMANCE ==========")

print(
    factory_summary.to_string(index=False)
)


# ==========================================
# 12. BEST FACTORY BY SALES
# ==========================================

best_sales = factory_summary.loc[
    factory_summary["Total_Sales"].idxmax()
]

print("\n========== HIGHEST SALES FACTORY ==========")

print(
    "Factory:",
    best_sales["Factory"]
)

print(
    f"Sales: ₹{best_sales['Total_Sales']:,.2f}"
)


# ==========================================
# 13. BEST FACTORY BY PROFIT
# ==========================================

best_profit = factory_summary.loc[
    factory_summary["Total_Profit"].idxmax()
]

print("\n========== HIGHEST PROFIT FACTORY ==========")

print(
    "Factory:",
    best_profit["Factory"]
)

print(
    f"Profit: ₹{best_profit['Total_Profit']:,.2f}"
)


# ==========================================
# 14. BEST FACTORY BY MARGIN
# ==========================================

best_margin = factory_summary.loc[
    factory_summary["Gross_Margin_%"].idxmax()
]

print("\n========== HIGHEST MARGIN FACTORY ==========")

print(
    "Factory:",
    best_margin["Factory"]
)

print(
    f"Margin: {best_margin['Gross_Margin_%']:.2f}%"
)


# ==========================================
# 15. LOWEST MARGIN FACTORY
# ==========================================

lowest_margin = factory_summary.loc[
    factory_summary["Gross_Margin_%"].idxmin()
]

print("\n========== LOWEST MARGIN FACTORY ==========")

print(
    "Factory:",
    lowest_margin["Factory"]
)

print(
    f"Margin: {lowest_margin['Gross_Margin_%']:.2f}%"
)


# ==========================================
# 16. SAVE FACTORY ANALYSIS
# ==========================================

output_file = (
    "outputs/factory_profitability_analysis.csv"
)

factory_summary.to_csv(
    output_file,
    index=False
)


# ==========================================
# 17. SAVE PRODUCT-FACTORY DATA
# ==========================================

mapping_output = (
    "outputs/product_factory_mapping.csv"
)

df.to_csv(
    mapping_output,
    index=False
)


# ==========================================
# 18. COMPLETION
# ==========================================

print("\n========== OUTPUT ==========")

print(
    "Factory analysis saved to:"
)

print(output_file)

print(
    "Product-factory mapping saved to:"
)

print(mapping_output)

print(
    "\nFactory analysis completed successfully."
)