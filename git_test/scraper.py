import scrapy
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime
import psycopg2
from psycopg2 import sql

class AutoRiaCrawlerSpider(scrapy.Spider):
    name = 'autoriaspider'
    allowed_domains = ['auto.ria.com']
    start_urls = ['https://auto.ria.com/car/used/']
    visited_links = set()  # Set to store visited links

    def __init__(self, *args, **kwargs):
        super(AutoRiaCrawlerSpider, self).__init__(*args, **kwargs)
        # Initialize database connection
        self.conn = psycopg2.connect(
            user="dmytrolebid",
            password="1234",
            host="localhost",
            port="5431",
            database="mydatabase"
        )
        self.cur = self.conn.cursor()

    def closed(self, reason):
        # Close database connection when the spider is closed
        self.cur.close()
        self.conn.close()

    def parse(self, response):
        # Extracting the links to the detailed pages
        detail_links = response.css('div.head-ticket a.address::attr(href)').getall()

        # Follow the links to the detailed pages
        for link in detail_links:
            if link not in self.visited_links:  # Check if the link has not been visited
                self.visited_links.add(link)
                yield scrapy.Request(link, callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        url = response.url
        title = response.css('h1.head::text').get()
        price_usd = response.css('strong::text').get()

        # Extracting odometer and appending "000" to it
        odometer_raw = response.css('span.size18::text').get()
        odometer = f"{odometer_raw}000" if odometer_raw else None

        # Extracting username using two possible selectors
        username = response.css('div.seller_info_name.bold::text, h4.seller_info_name a::text').get()
        image_url = response.css('img.outline::attr(src)').get()
        images_count_text = response.css('a.show-all.link-dotted::text').get()
        images_count = int(images_count_text.split()[-2]) if images_count_text else 0

        # Extracting car number
        car_number_raw = response.css(
            'span.state-num.ua::text').get()  # Extracting car number from span with class 'state-num ua'
        if not car_number_raw:
            car_number_raw = response.css(
                'span.state-num::text').get()  # If 'state-num ua' is not present, try extracting from 'state-num'
        car_number = car_number_raw.strip() if car_number_raw else None

        # Extracting VIN code using Beautiful Soup
        vin_raw = self.extract_vin_with_beautifulsoup(response)

        # Extracting phone numbers using the provided function
        phone_numbers = self.extract_phone_numbers(response)

        # Adding datetime_found field with the current date and time
        datetime_found = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Insert data into the database
        self.insert_data_into_database(url, title, price_usd, odometer, username, phone_numbers, image_url, images_count, car_number, vin_raw, datetime_found)

    def extract_vin_with_beautifulsoup(self, response):
        # Extracting VIN code using Beautiful Soup
        soup = BeautifulSoup(response.text, 'html.parser')
        vin_raw = soup.find('span', class_='label-vin')
        vin = vin_raw.text.strip() if vin_raw else None
        return vin

    def extract_phone_numbers(self, response):
        # Extracting phone numbers using the provided function
        url_parts = response.url.split('_')
        car_id = url_parts[-1].split('.')[0]
        url1 = f"https://auto.ria.com/demo/bu/mainPage/rotator/item/{car_id}?type=bu&langId=4"
        url2 = f"https://auto.ria.com/users/phones/{car_id}?hash={{userSecureHash}}"

        data = requests.get(url1).json()
        userSecureHash = data["userSecure"]["hash"]

        try:
            phone = requests.get(url2.format(userSecureHash=userSecureHash)).json()
        except:
            return None

        if "phones" in phone:
            return [p["phoneFormatted"] for p in phone["phones"]] if phone["phones"] else None
        return None

    def insert_data_into_database(self, url, title, price_usd, odometer, username, phone_numbers, image_url,
                                  images_count, car_number, vin_raw, datetime_found):
        # Define the SQL query for insertion
        insert_query = sql.SQL("""
            INSERT INTO auto_data (url, title, price_usd, odometer, username, phone_numbers, image_url, images_count, car_number, vin_raw, datetime_found)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """)

        try:
            # Execute the SQL query with the data
            self.cur.execute(insert_query, (
            url, title, price_usd, odometer, username, phone_numbers, image_url, images_count, car_number, vin_raw,
            datetime_found))

            # Commit the changes to the database
            self.conn.commit()

            print("Data inserted successfully.")
        except Exception as e:
            print(f"Error inserting data: {e}")
