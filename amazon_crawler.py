import json
import argparse
import requests
import bs4


def get_args():
    parser = argparse.ArgumentParser(
        description='Amazon Product Crawler by search term link',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        usage='python amazon_crawler.py --link "https://www.amazon.com/s?k=dellalienware&ref=nb_sb_noss_1"',
    )
    parser.add_argument('-l', '--link', type=str, help='Link to the search term', required=True)
    parser.add_argument('-p', '--max-pages', type=int, default=10, help='Number of pages to crawl')
    args = parser.parse_args()
    return args


def parse_product_links(soup):
    product_links = soup.findAll('a', attrs={
        "class": "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"
    })
    products = []
    for product in product_links:
        products.append("https://www.amazon.com" + product.get('href'))
    return products


def parse_product_title(soup):
    title = soup.find("span", attrs={"id": "productTitle"})
    title = title.text.strip() if len(title) > 0 else ""
    return title


def parse_product_image(soup):
    image_link = soup.find("img", attrs={"id": "landingImage"})
    image = image_link.get("src") if image_link is not None else ""
    return image


def parse_product_price(soup):
    price = soup.find("span", attrs={"class": "a-offscreen"})
    price=price.text.strip() if "$" in price.text.strip() else ''
    return price


def parse_product_rating(soup):
    rating = soup.select("div#averageCustomerReviews")
    rating = rating[0].text.strip() if len(rating) > 0 else ""
    return rating


def parse_product_description(soup):
    description = soup.select("div#featurebullets_feature_div")
    description = description[0].text.strip() if len(description) > 0 else ""
    return description


args = get_args()

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "referers":"https://www.google.com"
}

print("\033[1;32;40m [+] \033[1;32;40m Starting the crawler...")


resp = requests.get(args.link, headers=headers)
soup = bs4.BeautifulSoup(resp.text, "html.parser")

print("\033[1;32;40m [+] \033[1;32;40m Parsing the product links...")
products = parse_product_links(soup)
print("\033[1;32;40m [+] \033[1;32;40m Found {} products".format(len(products)))

data = []
print("\033[1;32;40m [+] \033[1;32;40m Parsing the products...")
for product in products:
    print("\033[1;32;40m [+] \033[1;32;40m Parsing product {} of {}"
          .format(products.index(product) + 1, len(products)))
    resp = requests.get(product, headers=headers)
    soup = bs4.BeautifulSoup(resp.text, "html.parser")
    title = parse_product_title(soup)
    image = parse_product_image(soup)
    price = parse_product_price(soup)
    rating = parse_product_rating(soup)
    description = parse_product_description(soup)
    data.append({
        "title": title,
        "image": image,
        "price": price,
        "rating": rating,
        "description": description
    })
    if len(data) == args.max_pages:
        break

print("\033[1;32;40m [+] \033[1;32;40m Saving the data...")
with open("data.json", "w") as f:
    json.dump(data, f, indent=4)
print("\033[1;32;40m [+] \033[1;32;40m Done!")

