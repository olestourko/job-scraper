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
            title = job.css

            title_css_paths = [
                '.jobtitle a *::text',
                'a.jobtitle *::text',
                'a.jobTitle *::text'
            ]
            for path in title_css_paths:
                title = get_inner_text(job.css(path))
                if title:
                    title = title.strip()
                    break

            company_css_paths = [
                '.company a *::text',
                'span.company *::text'

            ]
            for path in company_css_paths:
                company = get_inner_text(job.css(path))
                if company:
                    company = company.strip()
                    break

            yield {
                'title': title,
                'company': company,
            }

        next_page = response.css('.pagination a:last-of-type::attr("href")').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
