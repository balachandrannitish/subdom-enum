
# utils.py 
#
# Some general-purpose utilities that we might need to use on certain occassions
#

import socket
import json

def is_port_open(Host,port):
	'''
	Checks if a port on a remote host is open or not
	'''
	ConnectionSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # Open Stream Socket
	ConnectionResult = ConnectionSocket.connect_ex((Host,port)) # Make TCP Connection with connect_ex()
	ConnectionSocket.close()
	if ConnectionResult == 0:
		return True
	else:
		return False


def pretty_print(display_text,number_of_hyphens):
	print display_text + '\n' + '-'*number_of_hyphens + "\n"


def write_to_output_file(DomainList,output_file_name):
	with open(output_file_name,"w") as output_file:
		for i in DomainList:
			output_file.write(str(i)+"\n")

def get_config():
	with open("config/config.json","r") as config_file:
		config_dict = json.load(config_file)
		return config_dict