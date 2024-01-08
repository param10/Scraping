import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class TranscriptsSpider(CrawlSpider):
    name = 'transcrpits'
    allowed_domains = ['subslikescript.com']
    start_urls = ['https://subslikescript.com/movies_letter-P']  

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//ul[@class='scripts-list']/a"), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths="//a[@rel='next']"), follow=True),
    )

    def parse_item(self, response):
        article = response.xpath("//article[@class='main-article']")

        yield {
            'title': article.xpath("./h1/text()").get(),
            'plot': article.xpath("./p/text()").get(),
            'url': response.url,
        }

