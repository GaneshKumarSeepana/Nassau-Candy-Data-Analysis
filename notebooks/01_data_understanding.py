import pandas as pd

# ==========================================
# 1. LOAD ORIGINAL DATASET
# ==========================================

file_path = "data/Nassau Candy Distributor.csv"

df = pd.read_csv(file_path)

print("Original dataset shape:", df.shape)


# ==========================================
# 2. REMOVE COMPLETELY DUPLICATE ROWS
# ==========================================

duplicate_count = df.duplicated().sum()

print("Duplicate rows found:", duplicate_count)

df = df.drop_duplicates()

print("Shape after removing duplicates:", df.shape)


# ==========================================
# 3. CONVERT DATE COLUMNS
# ==========================================

df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    errors="coerce"
)

df["Ship Date"] = pd.to_datetime(
    df["Ship Date"],
    errors="coerce"
)


# ==========================================
# 4. CHECK IMPORTANT NUMERIC COLUMNS
# ==========================================

numeric_columns = [
    "Sales",
    "Units",
    "Gross Profit",
    "Cost"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# ==========================================
# 5. REMOVE RECORDS WITH MISSING
#    CRITICAL ANALYTICAL VALUES
# ==========================================

before = len(df)

df = df.dropna(
    subset=[
        "Sales",
        "Units",
        "Gross Profit",
        "Cost",
        "Order Date",
        "Product Name",
        "Division"
    ]
)

after = len(df)

print("Rows removed because of missing critical values:", before - after)


# ==========================================
# 6. REMOVE INVALID SALES / UNITS
# ==========================================

before = len(df)

df = df[
    (df["Sales"] > 0) &
    (df["Units"] > 0)
]

after = len(df)

print("Rows removed because Sales/Units were invalid:", before - after)


# ==========================================
# 7. STANDARDIZE TEXT COLUMNS
# ==========================================

text_columns = [
    "Division",
    "Region",
    "Product Name",
    "Product ID"
]

for column in text_columns:
    df[column] = df[column].astype(str).str.strip()


# ==========================================
# 8. RE-CALCULATE GROSS PROFIT
# ==========================================

df["Calculated Gross Profit"] = (
    df["Sales"] - df["Cost"]
)


# ==========================================
# 9. CHECK DIFFERENCE BETWEEN
#    PROVIDED AND CALCULATED PROFIT
# ==========================================

df["Profit Difference"] = (
    df["Gross Profit"] -
    df["Calculated Gross Profit"]
)

print(
    "Maximum difference between provided and calculated profit:",
    df["Profit Difference"].abs().max()
)


# ==========================================
# 10. CREATE CLEANED DATASET
# ==========================================

output_file = (
    "data/Nassau Candy Distributor_Cleaned.csv"
)

df.to_csv(
    output_file,
    index=False
)

print("\nCleaned dataset saved successfully!")
print("Final dataset shape:", df.shape)
print("Saved to:", output_file)