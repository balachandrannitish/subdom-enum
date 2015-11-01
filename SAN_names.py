import socket
import utils
import ssl


def get_SANs_from_cert(Domain):
	'''
	Returns the full list of Subject Alternative Names from an SSL cert. If the server isn't listening on port 443, return None
	'''
	SANs = []

	if utils.is_port_open(Domain,443) == False:
		return None

	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # Create a regular TCP Stream Socket
	sslsock = ssl.wrap_socket(s, cert_reqs=ssl.CERT_REQUIRED, ssl_version=ssl.PROTOCOL_SSLv23, ca_certs='data/ca-bundle.crt')  # Wrap the TCP socket in an SSL Context
	
	try:
		sslsock.connect((Domain,443))  		# This is the regular socket connect() method but it also does the SSL handshake in this case
	except socket.error as e:
		print e
		return None

	try:
		cert = sslsock.getpeercert()
	except ValueError as ve:
		print "No Cert"
		cert = None

	if cert is not None:
		try:
			SAN_Tuples = cert['subjectAltName']
		except KeyError:
			if verbose:
				print "No SAN"
			return None

		for x,y in SAN_Tuples:
			SANs.append(y)

		return SANs

	elif cert is None:
		return None


def get_pruned_SANs_list(subdomain_list,ParentDomain,verbose):
	''' This function does two things:
	1. Eliminates those items in the SANs list that
		a. Do not contain the parent domain
		b. Have an asterisk wildcard in them
	2. After filtering the subdomains based on the criteria above,
	   returns a list of sanitized subdomains '''
	
	result_list = []

	for k in subdomain_list:

		
		
		SANs_list = get_SANs_from_cert(k)
		if verbose:
			utils.pretty_print("Getting SANs for " + str(k), len("Getting SANs for " + str(k)))
			print "SANs: ",
			print SANs_list
		if SANs_list is not None:
			for i in SANs_list:
 				if i != ParentDomain and ParentDomain in i and '*' not in i: # Get only those SANs that are non-wildcard/asterisk containing subdomains
 					result_list.append(i)
 					print i,
					print " [SAN Name]"
		if verbose:
			print "\n"
	return result_list