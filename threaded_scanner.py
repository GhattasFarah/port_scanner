#!/bin/python

import sys
import socket
from datetime import datetime
import threading
import time
from queue import Queue

#This is to prevent duplication of shared variables.
lock = threading.Lock()

#Creates the queue object
q = Queue()

#This function aims at testing if the port is open and returning a result
def port_test(target, port):

    #setting up the socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(0.6) #setting time out to 1 sec

    #Trys to scan if sockers are open from range
    try:
        con = s.connect((target,port))
        with lock:
            print('{} port is open'.format(port))
        #closing the connection
        con.close()

    #Coding the program exists by keyboard interupt.
    except KeyboardInterrupt:
        print("\n Exiting port scanner.")
        sys.exit(0)
    
    #Any other exception doesn't matter therefore pass
    except:
        pass


#Function to set up concurrent threads to scan ports
def p_scanner_thread(target):
    while True:
        p_to_scan = q.get()
        port_test(target, p_to_scan) #Passes target and port to scan
        q.task_done() #empties queue


def main():
    #gathering the variables needed by user input.
    target = input("Enter Host Ip you wish to scan: ")
    host = socket.gethostbyname(target)

    #gets the port range from the user
    s_port = int(input("Enter the starting port: "))
    max_port = int(input("Enter the ending port: "))

    #starts the timer
    starttime = time.time()

    #Number of threads
    threads = 200

    #Printing banner.
    print("-" * 40)
    print("Scanning victim "+ target)
    print("Time started: "+ str(datetime.now()))
    print("-" * 40)

    for i in range(threads):
        t = threading.Thread(target=p_scanner_thread, args=(host,))
        t.daemon = True #sets these threads as children of parent thread therefore if parent thread dies should all children threads
        t.start()
    
    #loops through all ports within supplied range and puts them in the Queue
    for worker in range(s_port, max_port):
        q.put(worker)

    q.join()

    #Prints final run time.
    final_run = float('%0.2f' %( time.time() - starttime))
    print("Total run time is {}".format(final_run))

#Handles the calling of the main function.
if __name__ == "__main__":
    main()