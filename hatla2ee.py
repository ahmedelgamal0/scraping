from bs4 import BeautifulSoup
import requests
import csv


def search_used_cars(car):  # sourcery skip: inline-immediately-returned-variable
    url = f'https://eg.hatla2ee.com/en/car/{car}'

    with requests.Session() as session:
        page = session.get(url).text
        soup = BeautifulSoup(page, 'html.parser')

        pages_count = int(soup.find(class_ ="pagination pagination-right").ul.li.find_next_siblings()[-2].text)
        cars = []
        for page in range(1, pages_count + 1):
            url = f'https://eg.hatla2ee.com/en/car/{car}/page/{page}'
            page = session.get(url).text
            soup = BeautifulSoup(page, 'html.parser')

            car_list = soup.find_all(class_ = 'newCarListUnit_data_wrap')

            for item in car_list:
                title = item.find(class_ = 'newCarListUnit_header').text.strip()
                tags = item.find(class_ = 'newCarListUnit_metaTags').contents
                specs = [tag.text.strip() for tag in tags if tag.text!='\n']
                post_date = item.find(class_ = 'otherData_Date').span.text.strip()
                price = item.find(class_ = 'main_price').text.strip()

                try:
                    check_installment = item.find(class_ = 'newCarListUnit_subMetaTags').span.a
                    installment = 'Yes'
                except Exception:
                    installment = 'No'

                cars.append([title, specs, post_date, price, installment])
                
    return cars

def save_to_csv(filename, car):

    # run the function to get the data
    cars = search_used_cars(car)

    # open the file for writing and create a CSV writer object
    with open(filename, 'a', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=',', lineterminator='\n')

        # write the header row
        writer.writerow(['Title', 'Specs', 'Post Date', 'Options', 'Price', 'Installment'])

        # write the data rows
        for car in cars:
            writer.writerow(car)
        







