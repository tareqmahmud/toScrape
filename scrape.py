import re
from random import randint
from time import sleep, time

import pandas as pd
import requests
from IPython.core.display import clear_output
from bs4 import BeautifulSoup

from Helper import Clean

# Global Array for store data
titles = []
product_types = []
categories = []
prices_include_tax = []
prices_exclude_tax = []
taxes = []
total_availability = []
ratings = []
total_reviews = []
total_upc = []

# Incremental books and request counter
books_count = 1
request = 1

# Start the time for request count
start_time = time()

# Get WebPage data
for page in range(1, 51):
    root_url = "http://books.toscrape.com/catalogue/"
    url = "http://books.toscrape.com/catalogue/page-{}.html".format(page)
    response = requests.get(url)

    # Make Soup
    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.find_all("article", class_="product_pod")

    # Get the data
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
        availability = re.findall(r"\d+", availability_text)[0]
        price_in_tax = re.findall(r"[\d.\d]+", price_in_tax_text)[0]
        price_ex_tax = re.findall(r"[\d.\d]+", price_ex_tax_text)[0]
        tax = re.findall(r"[\d.\d]+", tax_text)[0]
        reviews = int(reviews)

        # Make Ratting String To Integer
        rating = Clean.str_to_int(rating)

        # Save all data to the global array
        titles.append(title)
        product_types.append(product_type)
        categories.append(category)
        prices_include_tax.append(price_in_tax)
        prices_exclude_tax.append(price_ex_tax)
        taxes.append(tax)
        total_availability.append(availability)
        ratings.append(rating)
        total_reviews.append(reviews)
        total_upc.append(upc)

        print("Book No: {} - {} title has been added to the global array store".format(books_count, title))

        books_count += 1

    # Calculate the total requests per second
    total_time = time() - start_time
    request_per_second = total_time / request
    print("{} Request per second.".format(request_per_second))
    request += 1

    # Sleep for some time
    print("\n-------------------------------------------------")
    random_second = randint(0, 15)
    print("-----------------Sleeping For {}sec----------------".format(random_second))
    sleep(random_second)
    print("----------------Go to the next page----------------")
    print("-------------------------------------------------\n")

    clear_output(wait=True)

# Save the data to the csv format with pandas
csv_data = pd.DataFrame({
    "Title": titles,
    "Product Type": product_types,
    "Category": categories,
    "Price(Include Tax)": prices_include_tax,
    "Price(Exclude Tax)": prices_exclude_tax,
    "Tax": taxes,
    "Total Availability": total_availability,
    "Rating": ratings,
    "Total Review": total_reviews,
    "UPC": total_upc,
})

csv_data.to_csv("data/books.csv", index=False)
print("All Books Successfully Stored To The CSV Format")
