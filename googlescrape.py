import socket
import random
import ssl
import utils
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


XPATH_FOR_GOOGLE_SEARCH_ELEMENTS = r"//h3[@class='r']/a[@href]"         # This XPath identifies the links to all of the search results on a page - 10 links per page, by deafult     # This will need to be fixed if Google's search results page ever changes.

#PATH_TO_PHATNOMJS = r'C:\Users\nitishb\Downloads\phantomjs-2.0.0-windows\phantomjs-2.0.0-windows\bin\phantomjs.exe'       #The path to the PhantomJS executable. If this changes, Google scraping will fail
#PATH_TO_PHATNOMJS = r'data\phantomjs.exe'
PATH_TO_PHATNOMJS = str(utils.get_config()['path_to_phantomjs'])

def randomize_user_agent():
	'''
	Returns a random user agent from a predefined list
	'''
	UserAgentList = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36', 
					 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36', 
					 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14', 
					 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0', 
					 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36', 
					 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0']
	UserAgent = random.choice(UserAgentList)
	return UserAgent


def launch_firefox():
	'''
	Launches a Firefox instance. 
	To run Firefox without CSS, images and Flash content, uncomment the lines below. 
	This doesn't help much vis-a-vis performance and this should, in most cases, not be done since it allows Google to easily detect that you're scraping their site
	'''
	#CustomFirefoxProfile = webdriver.FirefoxProfile()
	#CustomFirefoxProfile.set_preference('permissions.default.stylesheet', 2)                    # Disable loading of images,
	#CustomFirefoxProfile.set_preference('permissions.default.image', 2) 		                 # stylesheets
	#CustomFirefoxProfile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')   # and Adobe Flash content
	#driver = webdriver.Firefox(firefox_profile=CustomFirefoxProfile)
	driver = webdriver.Firefox()
	return driver


def launch_phantomJS():
	'''	Launches a PhatnomJS instance with a randomized user agent	'''
	dcap = dict(DesiredCapabilities.PHANTOMJS)
	dcap["phantomjs.page.settings.userAgent"] = randomize_user_agent()    #Set a random User Agent
	driver = webdriver.PhantomJS(executable_path=PATH_TO_PHATNOMJS,desired_capabilities=dcap)    #Launch PhantomJS with that random user agent. If the path to PhatnomJS is incorrect, this will fail
	driver.set_window_size(1280, 1024)  # Need this line to circumvent some open bug in PhantomJS - https://github.com/ariya/phantomjs/issues/11637
	return driver


def close_browser(driver):
	'''Closes a browser instance gracefully'''
	driver.close()


def GoogleScrape(ParentDomain,verbose=False):
	'''
	Scrapes Google Search Result pages using the PhantomJS headless browser to find subdomains of the Parent Domain
	Returns a set of domain names
	'''

	GoogleSearchQuery = r'allinurl: -www site:' + ParentDomain                            #The actual search query. E.g. - "allinurl: -www site:box.com"
	driver = launch_phantomJS()
	driver.get("http://www.google.com/search?q=allinurl:+-www+site:" + ParentDomain)                     # Make the browser send a GET request to the specified URL
	if verbose:
		print "\nBEGIN GOOGLE SCRAPING\n"
	j = 1
	googlescrape_result_list = []
	
	while(1):
		
		try:
			NextButton = driver.find_element(By.LINK_TEXT,'Next')                     # Find the "Next" buton on the page          # NOTE: We cant use: NextButton = driver.find_element(By.ID,'pnnext'), since it fails when PhantomJS executes it. Funnily, it works perfectly with Firefox
		
		except NoSuchElementException:
			print "The CAPTCHA Page was most likely encountered. Exiting..."             								    # Stop scraping when the CAPTCHA page is encountered
			break
		
		ListofLinks = driver.find_elements(By.XPATH, XPATH_FOR_GOOGLE_SEARCH_ELEMENTS)   											# Find all of the Google Search Result Links on the Page
		if verbose:
			print "--- Page: " + str(j) + " ---"
		
		for i in ListofLinks:
			Link = i.get_attribute("href")
			SanitizedLink = Link[Link.find("?q=")+len("?q="):Link.find(ParentDomain)+len(ParentDomain)]                            # Extract the App's URL from the nauseatingly large Google Search URL
			Domain = SanitizedLink[SanitizedLink.find("//")+len("//"):]    														   # Extract Domain Name from URL
			print Domain
			#print " [Google Scraping]"
			googlescrape_result_list.append(Domain)
		
		if verbose:
			print "--- END OF PAGE ---\n"
		NextButton.click()                     # Click the next button
		j = j+ 1
		time.sleep(random.choice(range(15,60)))    # Randomize the time delay to any value between 15 and 60 seconds. This is to avoid detection by Google
	
	if verbose:
		print "Closing Browser.\n\n"
	close_browser(driver)
	return googlescrape_result_list