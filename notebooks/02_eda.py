import pandas as pd

# ==========================================
# 1. LOAD CLEANED DATA
# ==========================================

file_path = "data/Nassau Candy Distributor_Cleaned.csv"

df = pd.read_csv(file_path)

# Convert dates
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])


# ==========================================
# 2. BASIC DATASET INFORMATION
# ==========================================

print("\n========== DATASET OVERVIEW ==========")

print("Rows:", df.shape[0])
print("Columns:", df.shape[1])


# ==========================================
# 3. DATE RANGE
# ==========================================

print("\n========== DATE RANGE ==========")

print("Minimum Order Date:", df["Order Date"].min())
print("Maximum Order Date:", df["Order Date"].max())


# ==========================================
# 4. UNIQUE COUNTS
# ==========================================

print("\n========== UNIQUE COUNTS ==========")

print("Unique Orders:", df["Order ID"].nunique())
print("Unique Customers:", df["Customer ID"].nunique())
print("Unique Products:", df["Product ID"].nunique())
print("Unique Product Names:", df["Product Name"].nunique())
print("Unique Divisions:", df["Division"].nunique())
print("Unique Regions:", df["Region"].nunique())


# ==========================================
# 5. DIVISIONS
# ==========================================

print("\n========== DIVISIONS ==========")

print(df["Division"].value_counts())


# ==========================================
# 6. REGIONS
# ==========================================

print("\n========== REGIONS ==========")

print(df["Region"].value_counts())


# ==========================================
# 7. KEY BUSINESS METRICS
# ==========================================

total_sales = df["Sales"].sum()

total_cost = df["Cost"].sum()

total_profit = df["Gross Profit"].sum()

total_units = df["Units"].sum()

overall_margin = (
    total_profit / total_sales * 100
)


print("\n========== KEY BUSINESS METRICS ==========")

print(f"Total Sales: ₹{total_sales:,.2f}")

print(f"Total Cost: ₹{total_cost:,.2f}")

print(f"Total Gross Profit: ₹{total_profit:,.2f}")

print(f"Total Units Sold: {total_units:,.0f}")

print(f"Overall Gross Margin: {overall_margin:.2f}%")


# ==========================================
# 8. AVERAGE VALUES
# ==========================================

print("\n========== AVERAGES ==========")

print(
    f"Average Sales per Record: ₹{df['Sales'].mean():,.2f}"
)

print(
    f"Average Profit per Record: ₹{df['Gross Profit'].mean():,.2f}"
)

print(
    f"Average Units per Record: {df['Units'].mean():.2f}"
)


# ==========================================
# 9. TOP 10 PRODUCTS BY SALES
# ==========================================

top_sales = (
    df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n========== TOP 10 PRODUCTS BY SALES ==========")

print(top_sales)


# ==========================================
# 10. TOP 10 PRODUCTS BY PROFIT
# ==========================================

top_profit = (
    df.groupby("Product Name")["Gross Profit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n========== TOP 10 PRODUCTS BY PROFIT ==========")

print(top_profit)