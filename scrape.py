import requests
from bs4 import BeautifulSoup
import re
import csv
from Helper import Clean

# Create Initial File
with open("data/books.csv", "w+", encoding="utf-8") as file:
    csv_row = csv.writer(file)
    # Header
    header = ["Title", "Product Type", "Category", "Price Include Tax(£)", "Price Exclude Tax(£)", "Tax(£)",
              "Availability",
              "Rating", "Reviews", "UPC"]
    csv_row.writerow(header)

books_count = 1

# Get WebPage data
for page in range(1, 51):
    root_url = "http://books.toscrape.com/catalogue/"
    url = "http://books.toscrape.com/catalogue/page-{}.html".format(page)
    response = requests.get(url)

    # Make Soup
    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.find_all("article", class_="product_pod")

    # Get Data
    for product in products:
        # Get Hyper Link
        base_url = product.h3.a["href"].strip()
        url = root_url + base_url

        # Get Single Page Data
        single_response = requests.get(url)
        single_soup = BeautifulSoup(single_response.text, "html.parser")
        single_product = single_soup.find("article", class_="product_page")

        # Product Main Data
        product_main = single_product.find("div", class_="product_main")

        # Scraping Data
        title = product_main.h1.get_text().strip()
        availability_text = product_main.find("p", class_="availability").get_text().strip()
        rating = product_main.find("p", "star-rating")["class"][1].strip()
        category = single_soup.find("ul", class_="breadcrumb").find_all("li")[2].a.get_text()

        # Product Data
        product_info = single_product.find("table", class_="table")
        single_info = product_info.find_all("tr")

        # Scraping Data
        upc = single_info[0].td.get_text().strip()
        product_type = single_info[1].td.get_text().strip()
        price_ex_tax_text = single_info[2].td.get_text().strip()
        price_in_tax_text = single_info[3].td.get_text().strip()
        tax_text = single_info[4].td.get_text().strip()
        reviews = single_info[6].td.get_text().strip()

        # Clean Data
        # Get Only Integer From String
        availability = re.findall("\d+", availability_text)[0]
        price_in_tax = re.findall("[\d.\d]+", price_in_tax_text)[0]
        price_ex_tax = re.findall("[\d.\d]+", price_ex_tax_text)[0]
        tax = re.findall("[\d.\d]+", tax_text)[0]
        reviews = int(reviews)

        # Make Ratting String To Integer
        rating = Clean.str_to_int(rating)

        # Save All Data To CSV Format
        with open("data/books.csv", "a", encoding="utf-8") as file:
            csv_row = csv.writer(file)

            # Data
            data = [title, product_type, category, price_in_tax, price_ex_tax, tax, availability, rating, reviews, upc]
            csv_row.writerow(data)
            print("No: {} - {} Book Has Been Added".format(books_count, title))
            books_count += 1
