from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# File locations
data_file = Path("data/cleaned_books.csv")
output_folder = Path("output")
chart_folder = output_folder / "charts"

chart_folder.mkdir(parents=True, exist_ok=True)


def run_analysis():

    # Read the cleaned data
    data = pd.read_csv(data_file)

    # Basic statistics of price and rating
    statistics = data[["price_gbp", "rating"]].describe().round(2)
    statistics.to_csv(output_folder / "summary_statistics.csv")

    # Get the top 10 rated books
    top_books = data.sort_values(
        by=["rating", "price_gbp"],
        ascending=[False, True]
    ).head(10)

    top_books.to_csv(
        output_folder / "top_rated_books.csv",
        index=False
    )

    # Get the 10 most expensive books
    expensive_books = data.sort_values(
        by="price_gbp",
        ascending=False
    ).head(10)

    expensive_books.to_csv(
        output_folder / "most_expensive_books.csv",
        index=False
    )

    # Price distribution
    plt.figure(figsize=(9, 5))
    plt.hist(data["price_gbp"], bins=15)
    plt.title("Distribution of Book Prices")
    plt.xlabel("Price (£)")
    plt.ylabel("Number of Books")
    plt.tight_layout()
    plt.savefig(
        chart_folder / "price_distribution.png",
        dpi=200
    )
    plt.close()

    # Number of books for each rating
    rating_count = data["rating"].value_counts().sort_index()

    plt.figure(figsize=(8, 5))
    plt.bar(
        rating_count.index.astype(str),
        rating_count.values
    )
    plt.title("Number of Books by Rating")
    plt.xlabel("Rating")
    plt.ylabel("Number of Books")
    plt.tight_layout()
    plt.savefig(
        chart_folder / "rating_distribution.png",
        dpi=200
    )
    plt.close()

    # Check the relation between price and rating
    plt.figure(figsize=(9, 5))
    plt.scatter(
        data["rating"],
        data["price_gbp"],
        alpha=0.65
    )
    plt.title("Price vs Rating")
    plt.xlabel("Rating")
    plt.ylabel("Price (£)")
    plt.tight_layout()
    plt.savefig(
        chart_folder / "price_vs_rating.png",
        dpi=200
    )
    plt.close()

    # Find average price for each rating
    average_price = (
        data.groupby("rating")["price_gbp"]
        .mean()
        .reset_index()
    )

    plt.figure(figsize=(8, 5))
    plt.bar(
        average_price["rating"].astype(str),
        average_price["price_gbp"]
    )
    plt.title("Average Price by Rating")
    plt.xlabel("Rating")
    plt.ylabel("Average Price (£)")
    plt.tight_layout()
    plt.savefig(
        chart_folder / "average_price_by_rating.png",
        dpi=200
    )
    plt.close()

    # Calculate correlation between price and rating
    correlation = data[["price_gbp", "rating"]].corr().round(3)

    correlation.to_csv(
        output_folder / "correlation_matrix.csv"
    )

    # Save all important results in one Excel file
    excel_file = output_folder / "books_scraping_report.xlsx"

    with pd.ExcelWriter(
        excel_file,
        engine="openpyxl"
    ) as writer:

        data.to_excel(
            writer,
            sheet_name="Cleaned Data",
            index=False
        )

        statistics.to_excel(
            writer,
            sheet_name="Summary Statistics"
        )

        top_books.to_excel(
            writer,
            sheet_name="Top Rated",
            index=False
        )

        expensive_books.to_excel(
            writer,
            sheet_name="Most Expensive",
            index=False
        )

        correlation.to_excel(
            writer,
            sheet_name="Correlation"
        )

    # Display the results
    print("\n===== EDA RESULTS =====")
    print("Number of books:", len(data))

    print(
        f"Average price: £{data['price_gbp'].mean():.2f}"
    )

    print(
        f"Median price: £{data['price_gbp'].median():.2f}"
    )

    print(
        f"Average rating: {data['rating'].mean():.2f}/5"
    )

    print(
        f"Highest rating: {data['rating'].max():.0f}/5"
    )

    print("\nCorrelation between price and rating:")
    print(correlation)

    print("\nTop 10 rated books:")
    print(
        top_books[
            ["title", "price_gbp", "rating"]
        ].to_string(index=False)
    )

    print(
        f"\nExcel report saved to: {excel_file}"
    )


if __name__ == "__main__":
    run_analysis()
