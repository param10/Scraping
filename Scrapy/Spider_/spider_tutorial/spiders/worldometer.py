import scrapy


class WorldometerSpider(scrapy.Spider):
    name = "worldometer"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/world-population/population-by-country/"]

    def parse(self, response):
        # Extracting "a" elements for each country
        countries = response.xpath('//td/a')

        # Looping through the countries list
        for country in countries:
            country_name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()

            # absolute_url = f'https://www.worldometers.info/{link}'
            #absolute_url = response.urljoin(link)

            #yield scrapy.Request(url=absolute_url)
            yield response.follow(url=link, callback = self.parse_country, meta={'country': country_name})
    
    def parse_country(self, response):
        country = response.request.meta['country']
        rows = response.xpath("(//table[contains(@class,'table')])[1]/tbody/tr")
        for row in rows: 
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()

            yield{
                'country': country,
                'year': year,
                'population':population,
            }
            
