import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = "best_movies"
    allowed_domains = ["imdb.com"]
    start_urls = ["https://www.imdb.com/search/title/?groups=top_250&sort=user_rating"]

    rules = (
        Rule(
            LinkExtractor(restrict_xpaths="//h3[@class='lister-item-header']/a"),
            callback="parse_item",
            follow=True,
        ),
    )

    def parse_item(self, response):

        yield {
            'title': response.xpath("//h1/text()").get(),
            'year' : response.xpath("//span[@class='sc-8c396aa2-2 jwaBvf']/text()").get(),
                                                                                        
        }
