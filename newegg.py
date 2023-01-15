from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

def search(search_key):
    url = f'https://www.newegg.com/p/pl?d={search_key}&N=4131'
    page = requests.get(url).text
    doc = BeautifulSoup(page, 'html.parser')

    pages_count = int(doc.find(class_ = "list-tool-pagination-text").strong.text.split('/')[-1])

    items_found = []
    for page in range(1, pages_count + 1):
        url = f'https://www.newegg.com/p/pl?d={search_key}&N=4131&page={page}'
        page = requests.get(url).text
        doc = BeautifulSoup(page, 'html.parser')

        div = doc.find(class_ = "item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")
        items = div.find_all(text=re.compile(search_key))

        for item in items:
            parent = item.parent
            if parent.name != 'a':
                continue
            link = parent['href']

            #Price
            try:
                next_parent = item.find_parent(class_ = 'item-container')
                price = next_parent.find(class_ = 'price-current').strong.text
            except:
                price = None
            #Brand name
            try:
                branding = next_parent.find(class_ = 'item-branding')
                brand = branding.find(class_ = 'item-brand').img['alt']
            except:
                brand = None

            #Reviews count 
            try:
                review_count = next_parent.find(class_ = 'item-rating-num').text
            except:
                review_count = None

            #Rating
            try:
                rating = next_parent.find(class_ = 'rating rating-4-5')['aria-label'].split(' ')[1]
            except:
                rating = None

            try:
                store = next_parent.find(class_ ="d2c-section-title").text
                store_link = next_parent.find(class_ ="d2c-section-title").a['href']
            except:
                store = None
                store_link = None

            items_found.append([item, int(price), link, brand, review_count, rating, store, store_link])

    # df = pd.DataFrame(items_found, columns = ['Item', 'Price', 'Link', 'Brand', 'Review Count', 'Rating', 'Store', 'Store Link'])
    return (items_found)

print(search('3050'))

