# -*- coding: utf-8 -*-
import scrapy


class MeetupSpider(scrapy.Spider):
    name = "meetup"
    allowed_domains = ["www.meetup.com"]
    start_urls = (
        'http://www.www.meetup.com/',
    )

    def parse(self, response):
        pass
