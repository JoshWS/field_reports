# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst


class ReportItem(scrapy.Item):
    created = scrapy.Field(output_processor=TakeFirst())
    slug = scrapy.Field(output_processor=TakeFirst())
    sapphire_url = scrapy.Field(output_processor=TakeFirst())
    description = scrapy.Field()
    article_date = scrapy.Field(output_processor=TakeFirst())
    source_url = scrapy.Field(output_processor=TakeFirst())
    author = scrapy.Field(output_processor=TakeFirst())
    posted_by = scrapy.Field(output_processor=TakeFirst())
    attachment = scrapy.Field()
    countries = scrapy.Field(output_processor=TakeFirst())
    images = scrapy.Field()
