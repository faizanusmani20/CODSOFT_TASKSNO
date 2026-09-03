import pandas as pd


# ---------------- LOAD DATA ----------------

df = pd.read_csv("synthetic_customer_dirty_data.csv")


# ---------------- BEFORE CLEANING ----------------

print("DATA BEFORE CLEANING")
print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())


# ---------------- REMOVE DUPLICATES ----------------

df = df.drop_duplicates()


# ---------------- HANDLE MISSING NUMERICAL VALUES ----------------

df["Engagement Score"] = df["Engagement Score"].fillna(
    df["Engagement Score"].median()
)

df["Satisfaction Level"] = df["Satisfaction Level"].fillna(
    df["Satisfaction Level"].median()
)


# ---------------- HANDLE MISSING CATEGORICAL VALUES ----------------

df["Role within Service"] = df["Role within Service"].fillna(
    df["Role within Service"].mode()[0]
)

df["Has Bought"] = df["Has Bought"].fillna(
    df["Has Bought"].mode()[0]
)


# ---------------- CLEAN DATE COLUMN ----------------

df["Date"] = df["Date"].str.replace(
    ",", "-", regex=False
)

df["Date"] = pd.to_datetime(
    df["Date"],
    dayfirst=True,
    errors="coerce"
)


# ---------------- CLEAN TEXT COLUMNS ----------------

for column in df.columns:
    if df[column].dtype == "object":
        df[column] = df[column].apply(
            lambda x: x.strip() if isinstance(x, str) else x
        )


# ---------------- AFTER CLEANING ----------------

print("\n\nDATA AFTER CLEANING")

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nData Types:")
print(df.dtypes)


# ---------------- SAVE CLEANED DATA ----------------

df.to_csv("cleaned_customer_data.csv", index=False)

print("\nData cleaned successfully!")