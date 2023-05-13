##################################################################
# Project:  CSE-5306 Vector Clock Implementation
# File:     Process 1
# Date:     Saturday 1 October 2022
# Authors:  Prithvi Bhat (pnb3598@mavs.uta.edu), 
#           Arvind Raman (axr0501@mavs.uta.edu)
##################################################################

import os
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import threading

P1_PORT     = 8001          # Port to bind socket to
P2_PORT     = 8002          # Port to bind socket to
P3_PORT     = 8003          # Port to bind socket to
HOSTNAME    = "0.0.0.0"     # Server Host address

g_vector_clock = [0, 0, 0]

def msg_recv(vector_clock, message_string):
    print("Message received: ", message_string)

    # Update internal Vector Clock with incoming vector clock's values
    vector_clock[0]     =  g_vector_clock[0]
    g_vector_clock[1]   =  vector_clock[1]
    g_vector_clock[2]   =  vector_clock[2]

    g_vector_clock[0] = vector_clock[0] + 1                         # Update receive event count
    print("Vector Clock after receive is: ", g_vector_clock)

    return True

def msg_send(vector_clock, destination, message_string):
    print("Vector Clock before send is: ", g_vector_clock)

    if destination == 1:
        thread1 = threading.Thread(target = msg_recv, args = (g_vector_clock, message_string,))
        thread1.start()                                             # Update vector clock for internal event

    elif destination == 2:
        g_vector_clock[0] = g_vector_clock[0] + 1                   # Update send event count
        p2_endpoint = 'http://{}:{}'.format(HOSTNAME, P2_PORT)      # Set an endpoint for the client to communicate to
        p2_proxy = xmlrpc.client.ServerProxy(p2_endpoint)
        thread2 = threading.Thread(target = p2_proxy.p2_msg_recv, args = (g_vector_clock, message_string,))
        thread2.start()

    elif destination == 3:
        g_vector_clock[0] = g_vector_clock[0] + 1                   # Update send event count
        p3_endpoint = 'http://{}:{}'.format(HOSTNAME, P3_PORT)      # Set an endpoint for the client to communicate to
        p3_proxy = xmlrpc.client.ServerProxy(p3_endpoint)
        thread3 = threading.Thread(target = p3_proxy.p3_msg_recv, args = (g_vector_clock, message_string,))
        thread3.start()

    print("Vector Clock after send is: ", g_vector_clock)

    return True



def Main():
    server = SimpleXMLRPCServer((HOSTNAME, P1_PORT))                    # Bind server
    print("Server online\nListening on port [" + str(P1_PORT) + "]")
    server.register_function(msg_recv, 'p1_msg_recv')                   # Register RPC
    server.register_function(msg_send, 'p1_msg_send')                   # Register RPC
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Killing Server")

if __name__ == '__main__':
    Main()