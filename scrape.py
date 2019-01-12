import csv
import re
from random import randint
from time import sleep, time

import requests
from IPython.core.display import clear_output

from Helper import Clean

# Create Initial Csv File
with open("data/books.csv", "w+", encoding="utf-8") as file:
    header = ["Title", "Product Type", "Category", "Price(Include Tax)", "Price(Exclude Tax)", "Tax",
              "Total Availability", "Rating", "Total Review", "UPC"]
    csv_writer = csv.writer(file)
    csv_writer.writerow(header)

# URL for scraping
root_url = "http://books.toscrape.com/catalogue/"
url = "http://books.toscrape.com/catalogue/page-1.html"
total_pages = 50

# Incremental books no, request
request = 1
book_no = 1

# Start request time
start_time = time()

# Scrape data from page 1 to total_pages
for page in range(1, total_pages + 1):

    # Send the request and get the response
    response = requests.get(url)

    # Single book section from product pod
    single_book_section = re.findall(r'<article\s+class="product_pod">(.*?)</article>', response.text,
                                     re.IGNORECASE | re.MULTILINE | re.DOTALL)

    # Go to the every books single page and collect necessary information
    for single_book in single_book_section:
        single_base_url = re.findall(r'<h3>\s*<a\s*href=[\'"](.*?)[\'"]', single_book,
                                     re.IGNORECASE | re.MULTILINE | re.DOTALL)

        if single_base_url is not None:
            # Generate single book url and get the response
            single_url = root_url + single_base_url[0]
            single_response = requests.get(single_url)

            # Find the single book section
            single_book_content = re.findall(r'<div class=".*?product_main">(.*?)<div id="product_description',
                                             single_response.text, re.IGNORECASE | re.MULTILINE | re.DOTALL)
            if single_book_content is not None:
                single_book_content = single_book_content[0]

                # Scraping Data
                title = re.findall(r'<h1>(.*?)</h1>', single_book_content,
                                   re.IGNORECASE | re.MULTILINE | re.DOTALL)[0]
                rating = re.findall(r'<p\s*class=[\'"]star-rating\s*(\w*)[\'"]>', single_book_content,
                                    re.IGNORECASE | re.MULTILINE | re.DOTALL)

                # Product type and category
                breadcrumb = re.findall(r'<ul\s*class=[\'"]breadcrumb[\'"]>(.*?)</ul>', single_response.text,
                                        re.I | re.M | re.DOTALL)[0]
                single_breadcrumb = re.findall(r'<li>.*?<a\s*href=[\'"].*?[\'"]>(.*?)</a>', breadcrumb,
                                               re.I | re.M | re.DOTALL)
                product_type = single_breadcrumb[1]
                category = single_breadcrumb[2]

                # Find the product description section from single book
                product_description = re.findall(r'<table\s*class=[\'"]table\s*table-striped[\'"]>.*?(.*?)</table>',
                                                 single_response.text, re.I | re.M | re.DOTALL)[0]

                single_product_description = re.findall(r'<td>(.*?)</td>', product_description, re.I | re.M | re.DOTALL)

                # Scraping Data -  Product Information
                upc = single_product_description[0]
                price_exclude_tax = re.findall(r'(\d+)', single_product_description[2])[0]
                price_include_tax = re.findall(r'(\d+)', single_product_description[3])[0]
                tax = re.findall(r'(\d+)', single_product_description[4])[0]
                availability = re.findall(r'(\d+)', single_product_description[5])[0]
                review = single_product_description[6]

                # Clean the scraping data
                rating = Clean.str_to_int(rating)

                # Save the data to csv file - data/books.csv
                with open("data/books.csv", "a", encoding="utf-8") as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerow(
                        [title, product_type, category, price_include_tax, price_exclude_tax, tax, availability, rating,
                         review, upc])

                # New book has been saved
                print("Book No #{}: {} has been saved to csv file".format(book_no, title))
                book_no += 1

            else:
                print("Unknown content")

        else:
            print("URL Doesn't Found")

    # Count the request
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
