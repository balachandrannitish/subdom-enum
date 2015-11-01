###Subdom-Enum 
Subdom-Enum is a command-line tool for Windows that enumerates subdomain names for a given domain. For instance, for the parent domain "google.com", subdomain names such as "mail.google.com", "drive.google.com", etc. will be discovered. This is a best-effort tool and might not be able to get you ALL subdomains in all cases. Generally speaking, there isn't a straightforward solution to this problem since most pubic-facing nameservers dont respond to AXFR queries anymore.

#####Methods used to extract subdomain names
1) Scraping Google Search Results using the query "allinurl: -www site:<Domain>.com"
2) Bruteforcing forward DNS lookups using a set of commonly used subdomain prefixes
3) If the domain suppports SSL, extract the SAN names out of the certificate to see if they contain any subdomains

######Usage: 
python subdom-enum.py [-h] [-b] [-g] [-s] [-v] [-o OUTPUT_FILE] Domain

-h, --help		show this help message and exit
-b, --bruteforce	Brute Force Forward DNS lookups for common subdomain prefixes [www,mail,etc]
-g, --googlescrape	Scrape Google search results (politely)
-s, --san-names	Fetch Subject Alternative Names from SSL certificates of subdomains identified by bruteforcing and/or Google scraping. This switch cant be used by itself.
-v, --verbose	Toggle verbose output. Off by default.
-o OUTPUT_FILE, --output-file OUTPUT_FILE	Dump results to an output file