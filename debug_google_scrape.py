def debug_Google_Scrape(ParentDomain):
	'''
	Aids debugging the Google Scraper by launching it in Firefox instead of PhantomJS
	'''

	GoogleSearchQuery = r'allinurl: -www site:' + ParentDomain
	driver = launch_firefox()
	driver.get("http://www.google.com/search?q=allinurl:+-www+site:" + ParentDomain)                     # Make the browser send a GET request to the specified URL
	print "\nBEGIN\n"
	j = 1
	googlescrape_result_set = set()
	
	while(1):
		
		try:
			NextButton = driver.find_element(By.LINK_TEXT,'Next')                                      # Find the "Next" buton on the page       # NOTE: We cant use: NextButton = driver.find_element(By.ID,'pnnext'), since it fails when PhantomJS executes it. Funnily, it works perfectly with Firefox
		except NoSuchElementException:
			print "The CAPTCHA Page was most likely encountered. Exiting now. Bye Bye"
			break
		
		ListofLinks = driver.find_elements(By.XPATH, XPATH_FOR_GOOGLE_SEARCH_ELEMENTS)                      # Finds all of the Google Search Result Links on the Page
		print "--- Page: " + str(j) + " ---"
		
		for i in ListofLinks:
			Link = i.get_attribute("href")
			Domain = Link[Link.find("//")+len("//"):Link.find(ParentDomain)+len(ParentDomain)]
			print Domain
			googlescrape_result_set.add(Domain)
		
		print "--- END OF PAGE ---\n"
		NextButton.click()                     # Clicks the next button
		j = j+ 1 
		RandomTimeDelay = random.choice(range(9,15))            # Randomize the time delay to any value between 9 and 15 seconds. This is to be as polite as possible while scraping!
		time.sleep(RandomTimeDelay)  

	print "Closing Browser. Bye\n\n"
	close_browser(driver)
	return googlescrape_result_set