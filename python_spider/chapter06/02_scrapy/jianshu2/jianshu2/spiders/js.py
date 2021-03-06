import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jianshu2.items import ArticleItem


class JsSpider(CrawlSpider):
    name = 'js'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/']

    rules = (
        # https://www.jianshu.com/p/907c9f3d8f5b
        Rule(LinkExtractor(allow=r'.*/p/[1-9a-z]{12}.*'), callback='parse_detail', follow=True),
    )

    def parse_detail(self, response):
        # title = response.xpath("//h1[@class='_1RuRku']/text()").get()
        # avatar = response.xpath("//a[@class='_1qp91i _1OhGeD']/img/@src").get()
        # author = response.xpath("//span[@class='FxYr8x']/a/text()").get()
        # pub_time = response.xpath("//div[@class='s-dsoj']/time/text()").get()

        # print(response.body.decode("utf8"))
        # print(response.xpath("//section[1]/div[1]").get())
        # title avatar author 这三个属性，是后来script 加载的
        title = response.xpath("//h1[@class='_1RuRku']/text()").get()
        avatar = response.xpath("//a[@class='_1qp91i _1OhGeD']/img/@src").get()
        author = response.xpath("//section[1]/div/div/div/div/span/a/text()").get()
        pub_time = response.xpath("//div[@class='s-dsoj']/time/text()").get()
        url = response.url
        url1 = url.split("?")[0]
        article_id = url1.split("/")[-1]
        content = response.xpath("//article[@class='_2rhmJa']").get()

        item = ArticleItem(
            title = title,
            avatar = avatar,
            author = author,
            pub_time = pub_time,
            origin_url = url,
            article_id = article_id,
            content = content
        )
        print(item)
        yield item


    # def parse_item(self, response):
    #     item = {}
    #     #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
    #     #item['name'] = response.xpath('//div[@id="name"]').get()
    #     #item['description'] = response.xpath('//div[@id="description"]').get()
    #     return item

# import scrapy
#
#
# class JsSpider(scrapy.Spider):
#     name = 'js'
#     allowed_domains = ['jianshu.com']
#     start_urls = ['http://jianshu.com/']
#
#     def parse(self, response):
#         pass
