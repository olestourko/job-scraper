import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
from scrapy.utils.serialize import ScrapyJSONEncoder
from urllib.parse import urljoin
import json
import hashlib
from src.utils import get_inner_text
from src import storage
import logging

class JobPost(scrapy.Item):
    url = scrapy.Field(output_processor=TakeFirst())
    job_title = scrapy.Field(output_processor=TakeFirst())
    employer = scrapy.Field(output_processor=TakeFirst())
    technologies = scrapy.Field()
    # str.strip is unicode.strip in Python 2.x
    description = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())

    def get_mutable_hash(self):
        encoder = ScrapyJSONEncoder()
        json_encoded_instance = encoder.encode(self)
        hash_algo = hashlib.md5()
        hash_algo.update(json.dumps(json_encoded_instance).encode('utf-8'))
        return hash_algo.hexdigest()


class StackOverflowSpider(scrapy.Spider):
    name = "StackOverflow Jobs"
    start_urls = [
        'https://stackoverflow.com/jobs?med=site-ui&ref=jobs-tab&sort=p'
    ]

    def __init__(self, max_pages=None):
        self.crawled_pages = 0
        if max_pages is not None:
            self.max_pages = int(max_pages)
        else:
            self.max_pages = None

        try:
            storage.read_from_disk(file=open('./storage.pickle', 'rb'))
        except Exception as e:
            logging.info(msg='Storage file does not exist; a new one will be created.')

        super(StackOverflowSpider, self)

    def parse(self, response):
        base_url = 'https://stackoverflow.com'

        for job in response.css('.listResults .-job'):
            route = job.css('h2 a.job-link::attr("href")').extract_first()
            url = urljoin(base_url, route)
            yield scrapy.Request(url=url, callback=self.parse_job_post_page)

        # Go to the next page
        if self.max_pages is None or self.crawled_pages < self.max_pages:
            next_page_url = response.css('.pagination .test-pagination-next::attr("href")').extract_first()
            if next_page_url:
                yield response.follow(url=next_page_url, callback=self.parse)

        self.crawled_pages += 1

    def closed(self, reason):
        storage.write_to_disk(file=open('./storage.pickle', 'wb'))

    def parse_job_post_page(self, response):
        loader = ItemLoader(item=JobPost(), response=response)
        n_sections = len(response.css('#overview-items section').extract())
        # Regular Job Post
        if n_sections == 3:
            loader.add_value(field_name='url', value=response.url)
            loader.add_css(field_name='job_title', css='.job-details--header > div > h1 > a::text')
            loader.add_css(field_name='employer', css='.job-details--header > div > div:nth-child(2) > a::text')
            loader.add_css(field_name='technologies', css='#overview-items > section:nth-child(2) > div > a::text')
            loader.add_value(field_name='description',
                             value=get_inner_text(response.css('#overview-items > section:nth-child(3) > div')))
        # Job Post with extra "High Response Rate" section
        elif n_sections == 4:
            loader.add_value(field_name='url', value=response.url)
            loader.add_css(field_name='job_title', css='.job-details--header > div > h1 > a::text')
            loader.add_css(field_name='employer', css='.job-details--header > div > div:nth-child(2) > a::text')
            loader.add_css(field_name='technologies', css='#overview-items > section:nth-child(3) > div > a::text')
            loader.add_value(field_name='description',
                             value=get_inner_text(response.css('#overview-items > section:nth-child(4) > div')))

        yield loader.load_item()
