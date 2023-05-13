##################################################################
# Project:  CSE-5306 Vector Clock Implementation
# File:     Master
# Date:     Saturday 1 October 2022
# Authors:  Prithvi Bhat (pnb3598@mavs.uta.edu), 
#           Arvind Raman (axr0501@mavs.uta.edu)
##################################################################

import os
import xmlrpc.client
import sys
import array as A

P1_PORT     = 8001          # Port to bind socket to
P2_PORT     = 8002          # Port to bind socket to
P3_PORT     = 8003          # Port to bind socket to
HOSTNAME    = "0.0.0.0"     # Server Host address

def Main():
    vector_clock = [0, 0, 0]
    while (1):
        source = int(input("\n\nSelect source (1 | 2 | 3 ):-------: "))
        if source >= 4 or source <= 0:
            print("ERROR: Invalid Source! Try again")
            continue

        destination = int(input("Select destination (1 | 2 | 3 ):--: "))

        message_string = input("Enter the message:--: ")

        if destination >= 4 or destination <= 0:
            print("ERROR: Invalid Destination! Try again")
            continue

        elif source == 1:
            p1_endpoint = 'http://{}:{}'.format(HOSTNAME, P1_PORT)      # Set an endpoint for the client to communicate to
            p1_proxy = xmlrpc.client.ServerProxy(p1_endpoint)
            p1_proxy.p1_msg_send(vector_clock, destination, message_string)

        elif source == 2:
            p2_endpoint = 'http://{}:{}'.format(HOSTNAME, P2_PORT)      # Set an endpoint for the client to communicate to
            p2_proxy = xmlrpc.client.ServerProxy(p2_endpoint)
            p2_proxy.p2_msg_send(vector_clock, destination, message_string)

        elif source == 3:
            p3_endpoint = 'http://{}:{}'.format(HOSTNAME, P3_PORT)      # Set an endpoint for the client to communicate to
            p3_proxy = xmlrpc.client.ServerProxy(p3_endpoint)
            p3_proxy.p3_msg_send(vector_clock, destination, message_string)


if __name__ == '__main__':
    Main()