import scrapy
from lxml import etree


class EventsCollector(scrapy.Spider):
        name = "Webber"
        start_urls = [
        "https://www.eventbrite.com/d/kenya--nairobi/events/"
        ]

        custom_settings = {
            'FEED_FORMAT': 'csv',
            'FEED_URI': 'Crawled_Data.csv'
        }

    # we have our starting url that the spider will scrape through collecting relevant data which in our case should
    # be urls or events

        def parse(self, response, **kwargs):
            for stuff in response.css('div.eds-g-cell-3-12'):
                link = stuff.css('.eds-event-card-content a::attr(href)').get()
                title = stuff.css('.eds-event-card__formatted-name--is-clamped-three::text').get()
                date = stuff.css('.eds-text-color--ui-orange::text').get()
                location = stuff.css('.card-text--truncated__one::text').get()
                

                yield {'Link': link, 'Title': title, 'Date': date, 'Location': location}

