#!/bin/python

import sys
import socket
from datetime import datetime

#Defining that victim target
if len(sys.argv) == 2:
	#gets the hostname as IPv4
	target = socket.gethostbyname(sys.argv[1])
else:
	print("Invalid input. Use 'python3 scanner.py <ip>'")
	
#Printing banner.
print("-" * 40)
print("Scanning victim "+target)
print("Time started: "+str(datetime.now()))
print("-" * 40)


#Trys to scan if sockers are open from range
try:
	#Scans the ports within port range
	for port in range(50, 85):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socket.setdefaulttimeout(1) #setting time out to 1 sec
		
		outcome = s.connect_ex((target,port)) #catches the error
		
		#if the port is open a 0 is returned otherwise an error is thrown and a 1 is returned
		if outcome == 0:
			print("Port {} is open".format(port))
		s.close() #closes the socket.

#Coding the program exists
except KeyboardInterrupt:
	print("\n Exiting port scanner.")
	sys.exit()
	
except socket.gaierror:
	print("Hostname is not resolveable.")
	sys.exit()

except socket.error:
	print("Couldn't connect to server.")
	sys.exit =()