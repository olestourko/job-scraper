import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from urllib.parse import urljoin
import json
import hashlib
from src.utils import get_inner_text


class JobPost(scrapy.Item):
    url = scrapy.Field(output_processor=TakeFirst())
    job_title = scrapy.Field(output_processor=TakeFirst())
    employer = scrapy.Field(output_processor=TakeFirst())
    technologies = scrapy.Field()
    description = scrapy.Field(output_processor=TakeFirst())

    @staticmethod
    def get_mutable_hash(instance):
        hash_algo = hashlib.md5()
        hash_algo.update(json.dumps(instance.__dict__['_local_values']).encode('utf-8'))
        return hash_algo.hexdigest()


class StackOverflowSpider(scrapy.Spider):
    name = "StackOverflow Jobs"
    start_urls = [
        'https://stackoverflow.com/jobs?med=site-ui&ref=jobs-tab&sort=p'
    ]

    def __init__(self, max_pages=None):
        self.crawled_pages = 0
        self.max_pages = int(max_pages)
        super(StackOverflowSpider, self)

    def parse(self, response):
        base_url = 'https://stackoverflow.com'

        for job in response.css('.list.jobs .-job'):
            route = job.css('.-job-summary a::attr("href")').extract_first()
            url = urljoin(base_url, route)
            yield scrapy.Request(url=url, callback=self.parse_job_post_page)

        # Go to the next page
        if self.max_pages is None or self.crawled_pages < self.max_pages:
            next_page_url = response.css('.pagination .test-pagination-next::attr("href")').extract_first()
            if next_page_url:
                yield response.follow(url=next_page_url, callback=self.parse)

        self.crawled_pages += 1

    def parse_job_post_page(self, response):
        employer_css = [
            '#job-detail .-name .employer::text',
            '#job-detail .-name::text'
        ]
        for css in employer_css:
            employer = response.css(css).extract_first()
            if employer:
                break

        loader = ItemLoader(item=JobPost(), response=response)
        loader.add_value(field_name='url', value=response.url)
        loader.add_css(field_name='job_title', css='#job-detail .-title .title::text')
        loader.add_value(field_name='employer', value=employer)
        loader.add_css(field_name='technologies', css='#job-detail .-technologies .-tags a::text')
        loader.add_css(field_name='description', css='#job-detail .-job-description .description')
        yield loader.load_item()
