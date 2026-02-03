from ast import parse
import json
import random
import re
import threading
import time

import parsel
import requests

base_url = "https://movie.douban.com/top250/"


# 请求头配置，模拟浏览器访问
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0",
    "Referer": "https://www.douban.com/",  # 设置来源页面，避免防盗链
}

d = []

session = requests.Session()

url_s = set()


def detail_parser(url: str):
    rsp = session.get(url, headers=headers).text

    selector = parsel.Selector(rsp).css("#info")

    print(rsp)
        
    
    print("\033[96m========== break-line ==========\033[0m")

    print(url)
    
    director = selector.xpath(
        ".//span[span[contains(text(), '导演')]]/span[@class='attrs']/a/text()"
    ).get("")

    return director


def parser(url) -> str:
    rsp = session.get(url, headers=headers).text

        
    selector = parsel.Selector(rsp)

    next_page_url = selector.css(".paginator > .next > a::attr(href)").get("")

    item_l = selector.css(".article ol.grid_view > li > .item")

    # content > div > div.article > ol > li:nth-child(1) > div > div.info > div.hd > a

    for i in item_l:
        picture = i.css(".pic > a > img::attr(src)").get()
        name_ch = i.css(".info > .hd > a > span.title:nth-child(1)::text").get()
        name_en = i.css(".info > hd > a > span.title:nth-child(2)::text").get(
            "\xa0/\xa0"
        )[3:]
        detail_url = i.css(".info > .hd > a::attr(href)").get("")

        director = detail_parser(detail_url)
        info = {
            "name_ch": name_ch,
            "name_en": name_en,
            "picture": picture,
            "detail_url": detail_url,
            "director": director,
        }

        d.append(info)

        time.sleep(random.randint(2, 3))

        break

    return next_page_url


def main():
    url = base_url + "?start=0&filter="
    parser(url)
    # while url := parser(url):
    # ...
    print(d[0])


if __name__ == "__main__":
    main()
