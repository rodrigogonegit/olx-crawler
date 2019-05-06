# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Join, MapCompose, TakeFirst, Compose

class Category(scrapy.Item):
	olx_id = scrapy.Field(
		output_processor=TakeFirst()
	)

	name = scrapy.Field(
		output_processor=TakeFirst()
	)

	url = scrapy.Field(
		output_processor=TakeFirst()
	)

class SubCategory(scrapy.Item):
	olx_cat_id = scrapy.Field(
		output_processor=TakeFirst()
	)

	olx_sub_id = scrapy.Field(
		output_processor=TakeFirst()
	)

	name = scrapy.Field(
		output_processor=TakeFirst()
	)

	url = scrapy.Field(
		output_processor=TakeFirst()
	)

class Item(scrapy.Item):
	name = scrapy.Field(
		output_processor=Compose(TakeFirst(), lambda x: x.strip())
	)
	description = scrapy.Field(
		output_processor=Compose(Join(), lambda x: x.strip())
	)
	image_urls = scrapy.Field(
		output_processor=MapCompose(lambda x: x.strip())
	)
	publish_date = scrapy.Field(
		output_processor=Compose(Join(), lambda x: x.strip())
	)
	location = scrapy.Field(
		output_processor=Compose(TakeFirst(), lambda x: x.strip())
	)
	views_count = scrapy.Field(
		output_processor=TakeFirst()
	) 
	price = scrapy.Field(
		output_processor= Compose(TakeFirst(), lambda x: x.replace('€', ''), lambda x: x.replace(' ', ''))
	)

class User(scrapy.Item):
	olx_user_id = scrapy.Field(
		output_processor=Compose(TakeFirst(), lambda x: x.strip())
	)
	fullname = scrapy.Field(
		output_processor=Compose(Join(), lambda x: x.strip())
	)

	phone_number = scrapy.Field()

	type_of_user = scrapy.Field(
		output_processor=Compose(TakeFirst(), lambda x: x.strip())
	)
	registration_date = scrapy.Field(
		output_processor=TakeFirst()
	)
	
