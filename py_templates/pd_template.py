import pandas as pd     

"""
Use import pandas as pd, and pd.read_json('customers.json') if the file is flat. 
If it’s nested, consider pd.json_normalize().
"""
# flat json
example_df = pd.read_json("example.json")
# nested json 
example_df = pd.json_normalize("example.json")

# +-------------------------
# |         DF VIEW        |
# +-------------------------
df_name = "example_df"
print(f"\033[94m{'='*(len(df_name)+8)}\n=== {df_name} ===\n{'='*(len(df_name)+8)}\033[0m")
print("\033[94m--- HEAD (first 5 rows) ---\033[0m")
print(example_df.head())
print("\033[94m--- TAIL (last 5 rows) ---\033[0m")
print(example_df.tail())
print("\033[94m--- SHAPE (rows, columns) ---\033[0m")
print(example_df.shape)
print("\033[94m--- COLUMNS ---\033[0m")
print(example_df.columns)
print("\033[94m--- DATA TYPES ---\033[0m")
print(example_df.dtypes)

import pandas as pd
import numpy as np


# ===================================================
# DUPLICATES: FIND + REMOVE
# ===================================================

# FIND DUPLICATE ROWS (entire row the same)

# duplicates_mask_all a Series of booleans
# - length = number of rows in example_df
# - True means: "this row is a duplicate of a previous row"
duplicates_mask_all = example_df.duplicated()

# example_df[duplicates_mask_all] uses the boolean Series to filter rows
# -> returns a **DataFrame** containing only the duplicate rows
duplicates_rows_all = example_df[duplicates_mask_all]

print("\n=== DUPLICATE ROWS (ALL COLUMNS) ===")
print(duplicates_rows_all)   

# FIND DUPLICATES BY COLUMN (e.g. 'country')

# u can add as many cols to check
col_name = "country"
duplicates_mask_id = example_df.duplicated(subset=[col_name])
duplicates_rows_id = example_df[duplicates_mask_id]

print("\n=== DUPLICATE ROWS BY country ===")
print(duplicates_rows_id)    # prints a DataFrame

# 1.3 REMOVE DUPLICATES (KEEP FIRST)
example_df_no_dups = example_df.drop_duplicates()   # removes exact duplicate rows, keeps first
print("\n=== DF WITHOUT DUPLICATE ROWS (ALL COLS) ===")
print(example_df_no_dups)

# 1.4 REMOVE DUPLICATES BY COLUMN (e.g. 'id'), KEEP FIRST
df_unique_by_id = df.drop_duplicates(subset=["id"], keep="first")
print("\n=== DF UNIQUE BY id (KEEP FIRST) ===")
print(df_unique_by_id)

# 1.5 REMOVE DUPLICATES BY COLUMN, KEEP LAST
df_unique_by_id_last = df.drop_duplicates(subset=["id"], keep="last")
print("\n=== DF UNIQUE BY id (KEEP LAST) ===")
print(df_unique_by_id_last)

# (OPTIONAL) IN-PLACE REMOVE (modifies df directly)
# df.drop_duplicates(subset=["id"], keep="first", inplace=True)

# ===================================================
# 2. NULLS (NaN): FIND + CLEAN / SET / REMOVE
# ===================================================

# 2.1 FIND NULLS (NaN)

# boolean mask of where values are NaN (same shape as df)
na_mask = df.isna()
print("\n=== BOOLEAN MASK OF NaN VALUES ===")
print(na_mask)

# count nulls per column
null_counts = df.isna().sum()
print("\n=== COUNT OF NaN PER COLUMN ===")
print(null_counts)

# rows where 'age' is null
age_null_rows = df[df["age"].isna()]
print("\n=== ROWS WHERE age IS NaN ===")
print(age_null_rows)

# rows where 'age' is NOT null
age_not_null_rows = df[df["age"].notna()]
print("\n=== ROWS WHERE age IS NOT NaN ===")
print(age_not_null_rows)

# 2.2 REMOVE (DROP) NULLS

# drop rows that have ANY NaN
df_dropna_rows_any = df.dropna()
print("\n=== DROP ROWS WITH ANY NaN (ANY COLUMN) ===")
print(df_dropna_rows_any)

# drop rows where 'age' is NaN (only that column matters)
df_dropna_age = df[df["age"].notna()]
print("\n=== DROP ROWS WHERE age IS NaN (ONLY AGE) ===")
print(df_dropna_age)

# drop columns that contain ANY NaN
df_dropna_cols_any = df.dropna(axis=1)
print("\n=== DROP COLUMNS THAT HAVE ANY NaN ===")
print(df_dropna_cols_any)

# 2.3 FILL / SET NULLS (CLEAN)

# copy so we don't mess up original
df_clean = df.copy()

# fill ALL NaNs in the whole df with a single value (e.g. 0)
df_fill_all_zero = df_clean.fillna(0)
print("\n=== FILL ALL NaN WITH 0 (WHOLE DF) ===")
print(df_fill_all_zero)

# FILL NULLS PER COLUMN (more realistic)

df_clean = df.copy()

# fill age nulls with a fixed value (e.g. 99)
df_clean["age_fill_99"] = df_clean["age"].fillna(99)

# OR fill age nulls with mean / median of that column
age_mean = df_clean["age"].mean()
age_median = df_clean["age"].median()

df_clean["age_fill_mean"] = df_clean["age"].fillna(age_mean)
df_clean["age_fill_median"] = df_clean["age"].fillna(age_median)

print("\n=== FILL age NaN WITH 99 / MEAN / MEDIAN ===")
print(df_clean[["id", "name", "age", "age_fill_99", "age_fill_mean", "age_fill_median"]])

# 2.4 FORWARD FILL / BACKWARD FILL (time-series style)

# example: sort by id and fill missing age with previous/next value
df_ffill = df.sort_values("id").copy()
df_ffill["age_ffill"] = df_ffill["age"].ffill()   # forward fill
df_ffill["age_bfill"] = df_ffill["age"].bfill()   # backward fill

print("\n=== FORWARD/BACKWARD FILL FOR age ===")
print(df_ffill)

# 2.5 SET VALUES TO NULL (make some values NaN on purpose)

df_set_null = df.copy()

# example: set age to NaN where age < 30
df_set_null.loc[df_set_null["age"] < 30, "age"] = np.nan

print("\n=== SET age TO NaN WHERE age < 30 ===")
print(df_set_null)