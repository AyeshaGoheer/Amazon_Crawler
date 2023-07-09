# Amazon_Crawler
# Amazon Product Crawler

This script allows you to crawl Amazon product information based on a search term link. It retrieves product details such as title, image, price, rating, and description from the search results.

## Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.9
- Required packages: `argparse`, `requests`, `bs4`

## Usage

Run the script using the following command:

```
python amazon_crawler.py --link "https://www.amazon.com/s?k=dellalienware&ref=nb_sb_noss_1"

```

Optional arguments:

- `-l, --link`: Link to the search term (required)
- `-p, --max-pages`: Number of pages to crawl (default: 10)

## How It Works

1. The script starts by parsing the command-line arguments provided by the user.
2. It sends an HTTP GET request to the specified search term link, using a user-agent header and referrer.
3. The response HTML content is parsed using `BeautifulSoup`.
4. The script extracts the product links from the parsed HTML.
5. For each product link, it sends another HTTP GET request to retrieve the product details.
6. The script extracts the title, image link, price, rating, and description from the product page.
7. The extracted data is stored in a list of dictionaries.
8. The script saves the data in JSON format to a file named `data.json`.
9. Once the crawling process is complete, the script outputs a completion message.

## Output

The script saves the crawled product data to a file named `data.json` in the same directory. The file contains a list of dictionaries, where each dictionary represents a product and includes the following fields:

- `title`: The product title
- `image`: The URL of the product image
- `price`: The product price (if available)
- `rating`: The product rating (if available)
- `description`: The product description (if available)

