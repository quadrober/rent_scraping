# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import psycopg2

CURRENCY_RATES = {
    '$': 40,
    '€': 42,
    'грн': 1
}  #add https://api.exchangerate.host/latest


def clean_price(price):
    try:
        # clean and convert the price string '25 000 грн/міс'
        price = price.replace('/міс', '').replace(' ', '')
        
        for currency, rate in CURRENCY_RATES.items():
            if currency in price:
                return float(price.replace(currency, '')) * rate
        
        return float(price)
    except (ValueError, AttributeError):
        return None


class RentScrapingPipeline:
    def open_spider(self, spider):
        self.conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='postgres',
            host='localhost',
            port='5432',

        )
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        # data cleaning
        item['rooms'] = int(item['rooms'][0])
        item['price'] = clean_price(item['price'])
        floors = [floor for floor in item['floor'].split() if floor.isnumeric()]
        item['actual_floor'] = floors[0]
        item['last_floor'] = floors[1]
        # save to db
        query = """
        INSERT into flats_rent 
        (city, district, price, rooms, planing, square, actual_floor, last_floor, building, children, pets, link) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cur.execute(query, (
            item['city'],
            item['district'],
            item['price'],
            item['rooms'],
            item['planing'],
            item['square'],
            item['actual_floor'],
            item['last_floor'],
            item['building'],
            item['children'],
            item['pets'],
            item['link']
            ))
        self.conn.commit()

        return item
