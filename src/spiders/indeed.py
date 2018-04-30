import scrapy
from src.utils import get_inner_text

# Before running:
# 1. Set PYTHONPATH to project root
# 2. export PYTHONPATH
# scrapy runspider src/spiders/indeed.py -o output.json

class IndeedSpider(scrapy.Spider):
    name = "indeed"
    start_urls = [
        'https://www.indeed.ca/jobs?q=developer&l=London,+ON&limit=20&sort=date',
    ]

    def parse(self, response):
        for job in response.css('.row.result'):
            link_css_paths = [
                '.jobtitle > a::attr("href")',
                'a.jobtitle::attr("href")'
            ]
            for path in link_css_paths:
                link = get_inner_text(job.css(path))
                if link:
                    link = 'https://www.indeed.ca%s' % link.strip()
                    break

            # when you yield a Request in a callback method, Scrapy will schedule that request to be sent and register a
            # callback method to be executed when that request finishes.
            yield scrapy.Request(url=link, callback=self.parse_job_post_page)

        next_page = response.css('.pagination a:last-of-type::attr("href")').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_job_post_page(self, response):
        # using yield or return doesn't seem to make much of a difference here
        yield {
            'job_title': get_inner_text(response.css('div[data-tn-component="jobHeader"] .jobtitle *::text')),
            'employer': get_inner_text(response.css('div[data-tn-component="jobHeader"] .company::text')),
            'description': get_inner_text(response.css('#job_summary div *::text'))
        }

