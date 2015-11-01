import time
import googlescrape
import bruteforce
import SAN_names
import utils
import argparse


def parse_options():
	'''
	Parse command line arguments

	Notes:
	1. The domain name is mandatory
	2. All flags are optional
	3. -s cannot be used in isolation
	4. When no flag is specified (i.e. the default case), all subdom enumeration mechanisms are executed
	'''
	parser = argparse.ArgumentParser(description="Subdom-Enum enumerates subdomain names for a given domain. This is a best-effort tool and might not be able to get you ALL subdomains in all cases. Generally speaking, there isn't a straightforward solution to this problem")

	parser.add_argument("-b","--bruteforce", help="Brute Force Forward DNS Lookups for some of the most common subdomain names", action="store_true" , default=False,dest="brute_force")
	parser.add_argument("-g","--googlescrape", help="Scrape Google Search results to idenitfy subdomains using the search query 'allinurl: -www site:<Domain>'", action="store_true" , default=False, dest="google_scrape")
	parser.add_argument("-s","--san-names",help="Fetch Subject Alternative Names from the SSL Certificates of the subdomain names identified by bruteforcing and/or google scraping. This switch can't be used by itself; you need to specify either -b or -g as well",action="store_true", default=False, dest="san_names")
	parser.add_argument("-v","--verbose",help="Turn on verbose output. Off by default",action="store_true", default=False, dest="verbose")
	parser.add_argument("-o","--output-file", help="Dump results to an output file", default="no_value",dest="output_file")
	parser.add_argument("Domain",help="The domain name whose subdomains you want to extract")

	results = parser.parse_args()

	ParentDomain = results.Domain

	brute_force_list = []
	google_scrape_list = []
	san_names_list = []

	verbose = results.verbose

	if not results.brute_force and not results.google_scrape and not results.san_names:   # Default: If no flags are specified => Run all switches
		
		print "Please wait. Enumerating subdoamins of " + ParentDomain 
		brute_force_list = bruteforce.BruteForce(ParentDomain,verbose)
		google_scrape_list = googlescrape.GoogleScrape(ParentDomain,verbose)
		temp = list(set(brute_force_list + google_scrape_list))  # Join the two lists and uniqify
		san_names_list = SAN_names.get_pruned_SANs_list(temp, ParentDomain, verbose)
		Result = list(set(brute_force_list + google_scrape_list + san_names_list))  # Join all three lists and uniqify to get the final result list
	
	else:
		
		if results.brute_force:
			print "Please Wait. Enumerating Subdoamins of " + ParentDomain 
			brute_force_list = bruteforce.BruteForce(ParentDomain,verbose)
		if results.google_scrape:
			print "Please Wait. Enumerating Subdoamins of " + ParentDomain 
			google_scrape_list = googlescrape.GoogleScrape(ParentDomain,verbose)
		if results.san_names:
			
			if not results.brute_force and not results.google_scrape:
				print "Error. You can't use the SAN names switch by itself. Please specify either -b or -g and try again"
			else:
				temp = list(set(brute_force_list + google_scrape_list))  # Join the two lists and uniqify
				san_names_list = SAN_names.get_pruned_SANs_list(temp, ParentDomain)


	if results.output_file != "no_value":
		utils.write_to_output_file(Result,results.output_file)


if __name__ == "__main__":
    parse_options()


    
 