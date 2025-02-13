# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class RentScrapingItem(Item):
    link = Field()
    price = Field()
    city = Field()
    district = Field()
    rooms = Field()
    square = Field()
    floor = Field()
    actual_floor = Field()
    last_floor = Field()
    building = Field()
    planing = Field()
    condition = Field()
    children = Field()
    pets = Field()
