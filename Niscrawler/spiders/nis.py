import scrapy
import json
from urllib.parse import quote


class NisSpider(scrapy.Spider):
    name = "nis"
    allowed_domains = ["nisanyansozluk.com"]

    def start_requests(self):
        with open("wordlist.json", "r", encoding="utf8") as f:
            words = json.load(f)
        for i in words:
            url = "https://radyal-api.vercel.app/api/nisanyan-decrypt?word=" + quote(
                i["name"]
            )
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        yield response.json()
