import scrapy

from ..items import RentScrapingItem

FOLLOW_URL = ['https://rieltor.ua', 'flats-rent/']

BUILDING_TYPES = ['Бетонно монолітний', 'Українська панель', 'Типова панель',
                  'Стара панель', 'Українська цегла', 'Газоблок', 'Стара цегла', 'Дореволюційний']
PLANNING_TYPES = ['Роздільне', 'Суміжно-роздільна', 'Суміжна',
                  'Кухня-вітальня', 'Студія', 'Пентхаус']
CONDITION_TYPES = ['Дизайнерський ремонт', 'Перша здача', 'Євроремонт', 'Хороший стан',
                   'Чудовий стан', 'Потрібен капітальний ремонт', 'Задовільний стан']

CATEGORIES = {
    "building": BUILDING_TYPES,
    "planing": PLANNING_TYPES,
    "condition": CONDITION_TYPES,
}


class FlatsRentSpider(scrapy.Spider):
    name = "flats_rent"
    allowed_domains = ["rieltor.ua"]
    start_urls = ["https://rieltor.ua"]

    def parse(self, response):
        # parse main page to get cities names
        cities = response.css('div.nav_item_option_geo_city')
        for city in cities:
            data_index_url = city.attrib.get('data-index-url')
            yield response.follow(
                url=FOLLOW_URL[0] + data_index_url + FOLLOW_URL[1], callback=self.parse_list
                )

    def parse_list(self, response):
        # parse listing of posters to get url to detail page
        for catalog_card in response.css('div.catalog-card'):
            url = catalog_card.css('a::attr(href)').get()
            yield response.follow(url, self.parse_detail_page)

        next_page = (
            response.css("ul.pagination_custom > li.active + li > a::attr(href)").get()
        )
        if next_page:
            yield response.follow(next_page, callback=self.parse_list)

    def parse_detail_page(self, response):
        item = RentScrapingItem()
        # parse main block
        item["link"] = response.url
        item["price"] = response.xpath(
            '/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/div/text()'
            ).get()
        item["city"] = response.xpath(
            '/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div[5]/a[1]/text()'
            ).get()
        item["district"] = response.xpath(
            '/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div[5]/a[2]/text()'
            ).get()
        # parsee first column
        item["rooms"] = response.xpath(
            '/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div[7]/div[1]/div[1]/span/a/text()'
            ).get()
        item["square"] = response.xpath(
            '/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div[7]/div[1]/div[2]/span/text()'
            ).get()
        item["floor"] = response.xpath(
            '/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div[7]/div[1]/div[3]/span/text()'
            ).get()
        item['actual_floor'] = None        # fill during
        item['last_floor'] = None          # data clining
        # parse second column
        item['building'] = None
        item['planing'] = None
        item['condition'] = None
        detail_column = response.css(
            'div.offer-view-details-column + div.offer-view-details-column'
            )
        for span in detail_column.css('span'):
            text = span.css('::text').get()
            if not text:
                continue
            for key, value in CATEGORIES.items():
                if text in value:
                    item[key] = text
                    break
        # parse block with aditional info
        children_labels = response.css(
            'div.offer-view-labels a[data-analytics-event="card-click-allow_children_chip"]::text'
            ).getall()
        pets_labels = response.css(
            'div.offer-view-labels a[data-analytics-event="card-click-allow_pets_chip"]::text'
            ).getall()
        item["children"] = children_labels[1].strip() if len(children_labels) == 2 else None
        item["pets"] = pets_labels[1].strip() if len(pets_labels) == 2 else None

        return item
