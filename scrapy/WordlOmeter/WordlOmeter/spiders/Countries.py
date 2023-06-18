import scrapy


class CountriesSpider(scrapy.Spider):
    name = "Countries"
    allowed_domains = ["www.worldometers.info"]
    start_urls = [
        "https://www.worldometers.info/world-population/population-by-country/"
    ]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0"
    }

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0], 
            callback=self.parse, 
            headers=self.headers
        )

    def parse(self, response):
        countries = response.xpath("//td/a")
        for country in countries:
            name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()

            yield response.follow(
                url=link,
                callback=self.parse_country,
                meta={"country_name": name},
                headers=self.headers,
            )

    def parse_country(self, response):
        name = response.request.meta["country_name"]
        rows = response.xpath(
            "(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr"
        )
        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()

            yield {
                "country_name": name,
                "year": year,
                "population": population,
                "User-Agent": response.request.headers["User-Agent"]
            }
