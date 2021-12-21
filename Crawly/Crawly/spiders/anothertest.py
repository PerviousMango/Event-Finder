


try:
  import scrapy
  class EventsScraper(scrapy.Spider):
        name = "Weabermain"
  start_urls = [
  "https://www.eventbrite.com/d/kenya--nairobi/events/"
  ]

  custom_settings = {
      'FEED_FORMAT': 'csv',
      'FEED_URI': 'Crawled_Data.csv'
  }
  #setting our custom feed settings as we are dealing with a csv file
  #

  def parse(self, response, **kwargs):
      for stuff in response.css('div.eds-g-cell-3-12'):
          link = stuff.css('.eds-event-card-content a::attr(href)').get()
          title = stuff.css('.eds-event-card__formatted-name--is-clamped-three::text').get()
          date = stuff.css('.eds-text-color--ui-orange::text').get()
          location = stuff.css('.card-text--truncated__one::text').get()
          
          yield {'Link': link, 'Title': title, 'Date': date, 'Location': location}
      
      #return super().parse(response, **kwargs)


except ImportError:
  print("Import etree from lxml failed !")