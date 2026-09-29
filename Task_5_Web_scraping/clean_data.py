from pathlib import Path
import pandas as pd
import re


raw_file = Path("data/raw_books.csv")
clean_file = Path("data/cleaned_books.csv")


def get_price(value):

    if pd.isna(value):
        return None

    value = str(value)

    # Get the number from the price
    result = re.search(r"\d+(?:\.\d+)?", value)

    if result:
        return float(result.group())

    return None


def clean_data():

    data = pd.read_csv(raw_file)

    print("Raw data loaded:", len(data), "rows")

    # Remove duplicate books
    data = data.drop_duplicates(
        subset=["title"]
    ).copy()

    # Clean price
    data["price_gbp"] = data["price_gbp"].apply(
        get_price
    )

    data["price_gbp"] = pd.to_numeric(
        data["price_gbp"],
        errors="coerce"
    )

    # Convert rating into numbers
    data["rating"] = pd.to_numeric(
        data["rating"],
        errors="coerce"
    )

    # Clean book titles
    data["title"] = (
        data["title"]
        .astype(str)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    # Check whether the book is in stock
    data["in_stock"] = data["availability"].str.contains(
        "In stock",
        case=False,
        na=False
    )

    # Fill missing prices with the median price
    if data["price_gbp"].isna().any():

        median_price = data["price_gbp"].median()

        data["price_gbp"] = data["price_gbp"].fillna(
            median_price
        )

    # Fill missing ratings with the median rating
    if data["rating"].isna().any():

        median_rating = data["rating"].median()

        data["rating"] = data["rating"].fillna(
            median_rating
        )

    # Divide books into price groups
    data["price_category"] = pd.cut(
        data["price_gbp"],
        bins=[
            -float("inf"),
            10,
            20,
            30,
            float("inf")
        ],
        labels=[
            "Under £10",
            "£10–£20",
            "£20–£30",
            "Over £30"
        ]
    )

    # Create rating labels
    data["rating_label"] = data["rating"].apply(
        lambda x: f"{x:.0f} Star"
    )

    # Sort by rating and then price
    data = data.sort_values(
        by=["rating", "price_gbp"],
        ascending=[False, True]
    )

    # Create the output folder if needed
    clean_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Save cleaned data
    data.to_csv(
        clean_file,
        index=False
    )

    # Display some information
    print("\n===== DATA CLEANING REPORT =====")

    print("Total rows:", len(data))

    print("\nMissing values:")
    print(data.isna().sum())

    print("\nPrice statistics:")
    print(data["price_gbp"].describe())

    print("\nRating statistics:")
    print(data["rating"].describe())

    print("\nFirst 5 records:")

    print(
        data[
            [
                "title",
                "price_gbp",
                "rating",
                "in_stock"
            ]
        ].head()
    )

    print(
        f"\nCleaned dataset saved to: {clean_file}"
    )

    return data


if __name__ == "__main__":
    clean_data()
