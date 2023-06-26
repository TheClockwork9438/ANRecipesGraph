#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Necessary library importation
import re
import time
import pprint
import pandas as pd
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# In[16]:


class AmazonPriceScraper(object):
	"""docstring for AmazonProductScraper"""
	def __init__(self):
		super(AmazonPriceScraper, self).__init__()
		self.link_XPATH = './/a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]'
		self.name_XPATH = './/span[@class="a-size-base-plus a-color-base a-text-normal"]'
		self.loging = False
		
		self.cooking_measures = ['teaspoon', 'tablespoon', 'cup', 'ounce', 
		'pint', 'quart', 'gallon', 'milliliter', 'liter', 'gram', 
		'kilogram', 'ounce', "oz" ,'pound', "lb", "lt"]

		self.patron = re.compile(r"(\d+(\.\d+)?)\s*(" + "|".join(self.cooking_measures) + r")\b", re.IGNORECASE)
		self.datos = {'NAME':[],'ASIN':[],"QUANTITY":[],"UNIT":[],'PRICE':[],'RATINGS':[],'RATINGS NUM':[],'LINK':[]}
		pass

	def scraper_engine(self, product = 'saltine crackers'):
		url = f"https://www.amazon.com/s?k={product}"

		self.options = webdriver.ChromeOptions()
		self.options.add_argument("start-maximized")
		self.options.add_argument("--lang=en")
		
		self.driver = webdriver.Chrome(options=self.options)
		self.wait = WebDriverWait(self.driver, 5)

		self.driver.get(url)

		self.wait.until(EC.element_to_be_clickable(
			(By.ID, 'nav-global-location-popover-link'))).click()

		
			
		self.wait.until(EC.element_to_be_clickable(
			(By.CSS_SELECTOR, "[data-action='GLUXPostalInputAction']"))).send_keys("33177")
		self.wait.until(EC.element_to_be_clickable(
			(By.CSS_SELECTOR, "[aria-labelledby='GLUXZipUpdate-announce']"))).click()
		self.wait.until(EC.element_to_be_clickable(
			(By.CSS_SELECTOR, ".a-popover-footer #GLUXConfirmClose"))).click()
		self.loging = True
		time.sleep(1)
		
		#wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".glow-toaster-footer input[data-action-type='DISMISS']"))).click()
		#

		items = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))

		link = ""
		product_name = []
		product_price = []
		product_ratings = []
		product_ratings_num = []
		product_asin = []
		product_link = []                       

		for item in items:
			
			# Get the link and asin
			link = item.find_element(By.XPATH, self.link_XPATH).get_attribute("href")			
			if "/dp/" not in link :continue	
			final_link = link.split("ref")[0]
			product_link.append(final_link)

			asin = link.split("/")[5].split("?")[0]
			product_asin.append(asin)			



			# Get the price
			whole_price = item.find_elements(By.XPATH, './/span[@class="a-price-whole"]')
			fraction_price = item.find_elements(By.XPATH, './/span[@class="a-price-fraction"]')

			if whole_price != [] and fraction_price != []:
				price = '.'.join([whole_price[0].text, fraction_price[0].text])
			else:
				price = 0
				pass

			product_price.append(price) 

		   # find ratings box
			ratings_box = item.find_elements(By.XPATH, './/div[@class="a-row a-size-small"]/span')

			# find ratings and ratings_num
			if ratings_box != []:
				ratings = ratings_box[0].get_attribute('aria-label')
				ratings_num = ratings_box[1].get_attribute('aria-label')
			else:
				ratings, ratings_num = 0, 0

			product_ratings.append(ratings)
			product_ratings_num.append(str(ratings_num))
			

			# Get the name of the product
			name = item.find_element(By.XPATH, self.name_XPATH)	
			product_name.append(name.text)
			print("NAME: ", name.text)			

			# Buscamos todas las coincidencias en el texto
			coincidencias = re.findall(self.patron, name.text)

			#datos = {'NAME':[],'ASIN':[],"QUANTITY":[],"UNIT":[],'PRICE':[],'RATINGS':[],'RATINGS NUM':[],'LINK':[]}

			# Iteramos sobre las coincidencias y las imprimimos
			if len(coincidencias) == 0: 
				continue
			else:
				for cantidad, _, unidad in coincidencias:
					self.datos['QUANTITY'].append(cantidad)
					self.datos['UNIT'].append(unidad)
					#print("QUANTITY: ", cantidad)
					#print("UNIT: ", unidad)					

				self.datos['ASIN'].append(asin)
				self.datos['NAME'].append(name.text)
				self.datos['PRICE'].append(price)
				self.datos['RATINGS'].append(ratings)
				self.datos['RATINGS NUM'].append(ratings_num)
				self.datos['LINK'].append(final_link)

				#print("ASIN: ", asin)
				#print("NAME: ", name.text)
				#print("PRICE: ", price)
				#print("RATINGS: ", ratings)
				#print("RATINGS NUM:", ratings_num)
				#print("LINK: ", final_link)
				#print("")

		self.driver.quit()
		amazon_df = pd.DataFrame.from_dict(self.datos)
		#pprint.pprint(amazon_df)
		#amazon_df['title'].replace('', np.nan, inplace=True)
		#amazon_df = amazon_df.dropna(subset=['title'])
		#amazon_df.to_csv("amazon_data.csv", header=True, index=False)		
		return amazon_df
		pass

	def quit(self):
		self.driver.quit()
		pass


# In[17]:


engine = AmazonPriceScraper()


# In[18]:


dataframe = engine.scraper_engine()


# In[19]:


#dataframe


# In[ ]:




