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
