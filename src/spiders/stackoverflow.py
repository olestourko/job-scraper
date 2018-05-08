import scrapy
from urllib.parse import urljoin
from src.utils import get_inner_text

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
        self.crawled_pages += 1
        print(self.crawled_pages)
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


    def parse_job_post_page(self, response):
        employer_css = [
            '#job-detail .-name .employer::text',
            '#job-detail .-name::text'
        ]
        for css in employer_css:
            employer = response.css(css).extract_first()
            if employer:
                break

        yield {
            'url': response.url,
            'job_title': response.css('#job-detail .-title .title::text').extract_first(),
            'employer': employer,
            'technologies': response.css('#job-detail .-technologies .-tags a::text').extract(),
            'description': response.css('#job-detail .-job-description .description').extract()
        }
