import scrapy
from ..items import DaGroup7Item
from scrapy.loader import ItemLoader


class TilesSpider(scrapy.Spider):
    name = 'tiles'
    allowed_domains = ['magnatiles.com']
    start_urls = ['http://magnatiles.com/products/page/1/']


    def parse(self, response):
        for p in response.css('ul.products li'):
            il = ItemLoader(item=DaGroup7Item(), selector=p)
            il.add_css('imageURL', 'img.attachment-woocommerce_thumbnail::attr(data-lazy-src)')
            il.add_css('sku', 'a.button::attr(data-product_sku)')
            il.add_css('name', 'h2')
            il.add_css('price', 'span.price bdi')
            yield il.load_item()

        next_page = response.css('ul.page-numbers a.next::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


# Importing appropriate libraries
import requests
import unittest


class TestingHeader(unittest.TestCase):
    headers = {'User-Agent': 'Mobile'}
    url2 = 'http://httpbin.org/headers'
    rh = requests.get(url2, headers=headers)
    print(rh.text)

    def test_headers(self):
        self.assertTrue(TestingHeader.headers, 'Mobile')


if __name__ == '__main__':
    unittest.main()