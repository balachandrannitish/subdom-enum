###Subdom-Enum 
Subdom-enum is a tool that enumerates subdomain names for a given domain. For instance, for the parent domain "google.com", subdomain names such as "mail.google.com", "drive.google.com", etc. will be discovered.

It gets as many subdomain names as possible (but usually not all) using the methods listed below, in conjunction

#####Methods used to extract subdomain names

1) Scraping Google Search Results using the query "allinurl: -www site:<Domain>.com"
2) Bruteforcing forward DNS lookups using a set of commonly used subdomain prefixes
3) If the domain suppports SSL, extract the SAN names out of the certificate to see if they contain any subdomains

