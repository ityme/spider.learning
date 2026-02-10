import scrapy
from scrapy.http import HtmlResponse


class QingTingFMSpider(scrapy.Spider):
    name = "QingTingFM"
    # allowed_domains = ["m.QingTing.fm"]
    start_urls = ["https://m.QingTing.fm/rank/"]

    def parse(self, response: HtmlResponse):
        print(dir(response))
        for i in response.xpath("//div").extract():
            yield i


def main():
    from scrapy import cmdline

    cmdline.execute(list("scrapy crawl QingTingFM --nolog".split()))


if __name__ == "__main__":
    main()
