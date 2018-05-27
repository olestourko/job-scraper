

### Running the scraping spider
```
scrapy runspider src/spiders/stackoverflow.py -a max_pages=10 --loglevel INFO

```

Edit `scrapy.cfg` to change how long the spider waits between requests.
