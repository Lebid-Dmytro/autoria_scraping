import subprocess
import time
from datetime import datetime

import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import psycopg2
import schedule
import scrapydo


class AutoDataItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    price_usd = scrapy.Field()
    odometer = scrapy.Field()
    username = scrapy.Field()
    car_number = scrapy.Field()
    vin = scrapy.Field()
    image_url = scrapy.Field()
    images_count = scrapy.Field()
    phone_number = scrapy.Field()
    datetime_found = scrapy.Field()


class AutoRiaSpider(scrapy.Spider):
    name = 'autoriaspider'
    allowed_domains = ['auto.ria.com']
    start_urls = ['https://auto.ria.com/car/used/?page=1']

    def save_to_database(self, item):
        try:
            connection = psycopg2.connect(
                user="dmytrolebid",
                password="1234",
                host="localhost",
                port="5431",
                database="mydatabase"
            )
            cursor = connection.cursor()
            insert_query = """INSERT INTO auto_data 
                              (url, title, price_usd, odometer, username, 
                               phone_number, image_url, images_count, 
                               car_number, vin, datetime_found) 
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

            cursor.execute(insert_query, (
                item['url'],
                item['title'],
                item['price_usd'],
                item['odometer'],
                item['username'],
                item['phone_number'],
                item['image_url'],
                item['images_count'],
                item['car_number'],
                item['vin'],
                item['datetime_found']
            ))
            connection.commit()
            print("Record inserted successfully")
        except (Exception, psycopg2.Error) as error:
            print(f"Error: {error}")
        finally:
            if connection:
                cursor.close()
                connection.close()

    def parse(self, response):
        detail_links = response.css('div.head-ticket a.address::attr(href)').getall()
        for link in detail_links:
            yield scrapy.Request(link, callback=self.parse_detail_page)

        current_page = int(response.url.split('=')[-1])
        next_page_url = f'https://auto.ria.com/car/used/?page={current_page + 1}'
        if next_page_url:
            yield

    def parse_detail_page(self, response):
        item = AutoDataItem()
        item['url'] = response.url
        item['title'] = response.css('h1.head::text').get()
        item['price_usd'] = response.css('strong::text').get()
        odometer_raw = response.css('span.size18::text').get()
        item['odometer'] = int(odometer_raw.replace(' тис.', '')) * 1000 if odometer_raw else None
        item['username'] = response.css('div.seller_info_name.bold::text, h4.seller_info_name a::text').get()
        item['car_number'] = response.css('span.state-num.ua::text').get()
        item['vin'] = self.get_vin(response)
        item['image_url'] = response.css('img.outline::attr(src)').get()
        images_count_text = response.css('a.show-all.link-dotted::text').get()
        item['images_count'] = int(images_count_text.split()[-2]) if images_count_text else 0
        item['phone_number'] = self.get_phone_number(response.url)
        item['datetime_found'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.save_to_database(item)

    def get_phone_number(self, url):
        driver = webdriver.Chrome()

        try:
            driver.get(url)
            # Wait for the "show" button to become clickable
            show_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'size14.phone_show_link.link-dotted.mhide')))

            # Use JavaScript to click the "show" button
            driver.execute_script("arguments[0].click();", show_button)

            # Wait for the displayed phone number field to become visible
            phone_element = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.popup-successful-call-desk[data-value]')))

            # Get the phone number from the displayed field
            phone_number = phone_element.get_attribute("data-value")
            return phone_number
        except Exception as e:
            return None
        finally:
            driver.quit()

    def get_vin(self, response):
        # Check VIN-code
        vin_primary = response.css('span.label-vin::text').get()
        if vin_primary:
            return vin_primary.strip()

        vin_secondary = response.css('span.label-vin + span::text').get()
        if vin_secondary:
            return vin_secondary.strip()

        vin_tertiary = response.css('span.vin-code::text').get()
        if vin_tertiary:
            return vin_tertiary.strip()

        return None


def data_recording():
    try:
        print(f"Running data recording job at {datetime.now()}")

        scrapydo.setup()

        spider_class = AutoRiaSpider
        process = scrapy.crawler.CrawlerProcess()
        process.crawl(spider_class)
        process.start(stop_after_crawl=True)
        process.stop()

        print("Data recording job completed successfully")
    except Exception as e:
        print(f"Error in data recording job: {e}")


def database_dump():
    try:
        print(f"Creating a database dump at {datetime.now()}")
        dump_filename = f"/Users/dmytrolebid/PycharmProjects/autoria_test/dumps/db_dump_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
        subprocess.run(["/opt/homebrew/bin/pg_dump", "-h", "localhost", "-U", "dmytrolebid", "-d", "mydatabase", "-f", dump_filename])

    except Exception as e:
        print(f"Error in database dump job: {e}")


# Schedule tasks to run daily at specific times
schedule.every().day.at("20:13").do(data_recording)
schedule.every().day.at("00:00").do(database_dump)

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
