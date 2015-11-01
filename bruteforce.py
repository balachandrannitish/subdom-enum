import DNS
import utils


def BruteForce(ParentDomain,verbose=False):
	""" Brute Force Forward DNS Lookups for some of the most common subdomain names. 
		These subdomain prefixes are obtained from the file specified in the argument """
	
	BruteForcePrefixes = open(str(utils.get_config()['brute_force_prefixes_file']),'r')
	bruteforce_result_list = []   #Set of the domain names obtained by brute forcing
	
	for line in BruteForcePrefixes:
		
		CurrentName = line.replace("\n","") + "." + ParentDomain     # Append the subdoamin prefix to the parent domain name [e.g. abc + google.com = abc.google.com]
		Display = "Current Name is: " + CurrentName
		
		if verbose:
			print '-'*len(Display)
			print Display
		
		try:			
			IP = DNS.dnslookup(unicode(CurrentName,"utf-8"),qtype='A')[0]  # Do a DNS Lookup for the current host name. #The current name will be a combination of the brute force prefix and the parent domain. E.g. - Sub=abc and Parent=xyz.com. So, current=abc.xyz.com
			bruteforce_result_list.append(CurrentName)
			if verbose:
				print "SUCCESS! IP/CNAME = " + IP
				display_text="WebServerStatus = ON" if utils.is_port_open(IP,80)==True  else "WebServerStatus = OFF"     #Test whether the destination IP's WebServer is ON. If it isn't, this domain isn't of any interest to us.
				utils.pretty_print(display_text,len(Display))
			else:
				print CurrentName
				#print " [Brute Force]"
		
		except DNS.Base.ServerError as e:
			display_text="\nThe DNS Server is Refusing requests. \nPlease use 8.8.8.8 and try again." if 'REFUSED' in e.message  else "Non-Existent Domain"
			if verbose:
				utils.pretty_print(display_text,len(Display))
			continue
		
		except DNS.Base.TimeoutError:   #Handle the case where there's a DNS timeout
			if verbose:
				utils.pretty_print("Timeout",len(Display))
			continue
		
		except IndexError:    # This handles those (rare) cases where a valid DNS response is returned with no IP address (e.g. - 67.salesforce.com), because of which the variable index 0 of the array is non-existent and we thereforce cannot assign it to the variable 'IP'.
			if verbose:
				utils.pretty_print("Non-Existent Domain",len(Display))
			continue
	
	return bruteforce_result_list