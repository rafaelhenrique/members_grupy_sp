# -*- coding: utf-8 -*-
import scrapy
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

from members_grupy_sp.items import MembersGrupySpItem


class MeetupSpider(scrapy.Spider):
    name = "meetup"
    allowed_domains = ["meetup.com"]
    start_urls = (
        'http://www.meetup.com/pt/Grupy-SP/events/225100888/',
        'http://www.meetup.com/pt/Grupy-SP/events/224816475/',
        'http://www.meetup.com/pt/Grupy-SP/events/224816288/',
        'http://www.meetup.com/pt/Grupy-SP/events/223534171/',
        'http://www.meetup.com/pt/Grupy-SP/events/222731535/',
        'http://www.meetup.com/pt/Grupy-SP/events/222170881/',
        'http://www.meetup.com/pt/Grupy-SP/events/221188662/',
        'http://www.meetup.com/pt/Grupy-SP/events/220656720/',
        'http://www.meetup.com/pt/Grupy-SP/events/219248903/',
    )

    def __init__(self):
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.rank = {}

    def spider_closed(self, spider):
        zipped_rank = zip(self.rank.values(), self.rank.keys())
        self.rank = reversed(sorted(zipped_rank))

        for position, rank in enumerate(self.rank, 1):
            print("{0}.\t{1}".format(position, rank[1]))

    def parse(self, response):
        # get event name from event-title id
        event_name = response.xpath(
            '//*[@id="event-title"]/h1/text()').extract_first().strip()

        # get rsvp_list
        rsvp_list = response.xpath('//*[@id="rsvp-list"]')
        # from rsvp_list get anchors
        rsvp_anchor = rsvp_list.xpath(
            '*[@id]/div/div[2]/h5/a')

        for a in rsvp_anchor:
            # separate url and text from anchor
            url = a.xpath('@href').extract_first()
            member = a.xpath('text()').extract_first()

            # use Item class
            item = MembersGrupySpItem()
            item["name"] = event_name
            item["member"] = member
            item["url"] = url

            if url in self.rank.keys():
                self.rank[url] += 1
            else:
                self.rank[url] = 1

            yield item
