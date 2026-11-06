from bs4 import BeautifulSoup
from selenium import webdriver
import requests, time, glob


        
def makeDriver():
	profile = webdriver.FirefoxProfile('path/to/firefox/profile') # open the firefox profile for adblock
	driver = webdriver.Firefox(profile) # open firefox with the profile retrieved
	print(1) #debug
	driver.set_window_size(1296, 546) # resize the window automatically
	print(2) #debug
	return driver
	
if __name__ == "__main__":
	
	d = makeDriver()
	
	all_files = glob.glob("./site_copy/*.html")
	baseUrl = "https://podcast.example/"
	
	d.get(baseUrl)
	compUrl="https://payments.example/donate"
	
	for f in all_files:
		webpage = f.split("\\")[1]
		d.get(baseUrl + webpage)
		
		betton = d.find_element_by_xpath("//a[@id='donate-btn']")
		if betton.get_attribute("href") != compUrl:
			print("error in page: " + webpage)
	
	