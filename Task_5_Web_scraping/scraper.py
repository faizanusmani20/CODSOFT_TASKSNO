import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup


base_url = "https://books.toscrape.com/"
output_file = Path("data/raw_books.csv")

# Number of pages to scrape
max_pages = 10

headers = {
    "User-Agent": "Mozilla/5.0"
}


def get_rating(rating):

    ratings = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    return ratings.get(rating, None)


def scrape_books():

    books = []
    url = base_url
    page_number = 0

    while url and page_number < max_pages:

        page_number += 1

        print(
            f"Scraping page {page_number}: {url}"
        )

        response = requests.get(
            url,
            headers=headers,
            timeout=20
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Find all books on the page
        book_list = soup.select(
            "article.product_pod"
        )

        for book in book_list:

            title_tag = book.select_one(
                "h3 a"
            )

            price_tag = book.select_one(
                ".price_color"
            )

            rating_tag = book.select_one(
                "p.star-rating"
            )

            # Get title
            if title_tag:
                title = title_tag.get(
                    "title",
                    ""
                ).strip()
            else:
                title = ""

            # Get price
            if price_tag:
                price = price_tag.get_text(
                    strip=True
                )
            else:
                price = ""

            # Get rating
            rating = None

            if rating_tag:

                rating_classes = rating_tag.get(
                    "class",
                    []
                )

                for item in rating_classes:

                    if item in [
                        "One",
                        "Two",
                        "Three",
                        "Four",
                        "Five"
                    ]:

                        rating = get_rating(item)
                        break

            # Get availability
            availability_tag = book.select_one(
                ".availability"
            )

            if availability_tag:
                availability = availability_tag.get_text(
                    " ",
                    strip=True
                )
            else:
                availability = ""

            # Get product link
            if title_tag and title_tag.get("href"):

                product_url = urljoin(
                    url,
                    title_tag.get("href")
                )

            else:
                product_url = ""

            books.append({
                "title": title,
                "price_gbp": price.replace(
                    "£",
                    ""
                ).strip(),
                "rating": rating,
                "availability": availability,
                "product_url": product_url,
                "scraped_at": datetime.now().isoformat(
                    timespec="seconds"
                )
            })

        # Find the next page
        next_page = soup.select_one(
            "li.next a"
        )

        if next_page:

            next_link = next_page.get(
                "href"
            )

            if next_link:
                url = urljoin(
                    url,
                    next_link
                )
            else:
                url = None

        else:
            url = None

        # Small delay between requests
        time.sleep(0.5)

    # Convert data into a DataFrame
    data = pd.DataFrame(books)

    # Create data folder if it does not exist
    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Save the scraped data
    data.to_csv(
        output_file,
        index=False
    )

    print(
        f"\nSaved {len(data)} records to {output_file}"
    )

    return data


if __name__ == "__main__":
    scrape_books()
