import scrapy
from scrapy.loader import ItemLoader
from olxcrawler.items import Category, SubCategory, Item, User
from pprint import pprint

class OlxSpider(scrapy.Spider):
	name = "olx"

	def start_requests(self):
		urls = [
			'https://www.olx.pt/'
		]
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		cats_nodes = response.css('.maincategories-list.clr div.li.fleft')
		sub_cats_nodes = response.css('.subcategories-list.clr ul li.fleft')

		# List of Category objects
		categories = []

		# List of SubCategory objects
		sub_cats = []

		self.logger.debug("Found {} categories".format(len(cats_nodes)))
		for cat in cats_nodes:
			c = ItemLoader(item=Category(), selector=cat)
			c.add_css('olx_id', 'div.item a::attr(data-id)')
			c.add_css('name', 'div.item a span::text')
			c.add_css('url', 'div.item a::attr(href)')

			yield c.load_item()

		self.logger.debug("Found {} SUB categories".format(len(sub_cats_nodes)))
		for sub_cat in sub_cats_nodes:
			s = ItemLoader(item=SubCategory(), selector=sub_cat)
			s.add_css('olx_cat_id', 'a::attr(data-category-id)')
			s.add_css('olx_sub_id', 'a::attr(data-id)')
			s.add_css('name', 'a span span::text')
			s.add_css('url', 'a::attr(href)')
			ss = s.load_item()
			# print(ss)
			yield response.follow(ss['url'], self.parse_items_list_page)

		# print ("LENGTH: " + str(len(sub_cats)))

	def parse_items_list_page(self, response):
		for item in response.css('table.fixed.offers tr.wrap td div table tbody td.title-cell div h3 a::attr(href)').getall():
			yield scrapy.Request(item, callback=self.parse_item_page)
		
	def parse_item_page(self, response):
		# yield self.parse_item(response)
		yield self.parse_user(response)

	def parse_item(self, selector):
		i = ItemLoader(item=Item(), selector=selector)
		# response.css('div.offer-titlebox h1::text').get()

		i.add_css('name', 'div.offer-titlebox h1::text')
		i.add_css('description', 'div#textContent::text')
		i.add_css('image_urls', 'div.tcenter.img-item img::attr(src)')
		i.add_css('publish_date', 'div.offer-titlebox__details em::text') # getall()??? how to force get all?
		i.add_css('location', 'div.offer-titlebox__details a strong::text')
		i.add_css('views_count', 'div#offerbottombar div.pdingtop10 strong::text')
		i.add_css('price', 'div.price-label strong::text') # output is 'X €' -- X being the price integer

		tt =  i.load_item()
		# self.logger.debug("----------- ITEM")
		# self.logger.debug(tt)
		return tt

	def parse_user(self, response):
		u = ItemLoader(item=User(), response=response)

		# olx_user_id is of type: https://www.olx.pt/ads/user/1Gm2h/
		# Extract 1Gm2h further in the item pipeline
		u.add_css('olx_user_id', 'div.offer-sidebar__box div.offer-user__details h4 a::attr(href)') 

		# Concatenate list and remove whitespace in item pipeline
		u.add_css('fullname', 'div.offer-sidebar__box div.offer-user__details h4 a::text')
		
		# Needs a new request for this
		# phone_number_node = response.css('ul#contact_methods li')

		# if len(phone_number_node) > 0:
			# u.add_value('phone_number')

		# u.add_css('phone_number', )

		u.add_css('registration_date', 'div.offer-sidebar__box div.offer-user__details span::text')

		# Of type "Registado desde Out 2016" -- EXTRACT Out 2016 (mm YYYY)
		u.add_css('type_of_user', 'div.clr.descriptioncontent.marginbott20 table.details.fixed table td strong a::text')

		uu = u.load_item()
		self.logger.debug(uu)
		return uu