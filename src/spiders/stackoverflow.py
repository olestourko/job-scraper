import scrapy
from urllib.parse import urljoin
from src.utils import get_inner_text

class StackOverflowSpider(scrapy.Spider):
    name = "StackOverflow Jobs"
    start_urls = [
        'https://stackoverflow.com/jobs?med=site-ui&ref=jobs-tab&sort=p'
    ]

    def parse(self, response):
        for job in response.css('.list.jobs .-job'):
            route = job.css('.-job-summary a::attr("href")').extract_first()
            url = urljoin('https://stackoverflow.com', route)
            yield scrapy.Request(url=url, callback=self.parse_job_post_page)


    def parse_job_post_page(self, response):
        yield {
            'job_title': response.css('#job-detail .-title .title::text').extract_first(),
            'employer': response.css('#job-detail .-name .employer::text').extract_first(),
            'description': get_inner_text(response.css('#job-detail .-job-description .description *::text')),
        }
