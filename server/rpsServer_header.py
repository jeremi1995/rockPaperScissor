#############################################################################
# Program:
#    Lab PythonRPS_Server, Computer Networking
#    Brother Jones, CSE 354
# Author:
#    Your Name
# Summary:
#    Program description ... [fill in]
#
#
# *****************************************************************************
#
# RPS (rock/paper/scissors) Protocol Description
# ----------------------------------------------
#
#
##############################################################################
# Note: Take-2 header goes here

#
# This is just a slightly modified version of the TCPServer.py code from
# section 2.7 of the book that was used in class.
#

import sys
import json
import threading
from socket import *

DEFAULT_VALUE = 6789
serverPort = int(sys.argv[1]) if len(sys.argv) == 2 else DEFAULT_VALUE

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('The Server is ready to receive')

threads = []
games = []


# def createGame(request):
#     if game


def handle_request(clientRequestDict, connectionSocket):
    '''This function handles all kinds of requests, not just 
        the initial connection request.
    '''
    print("Received from client: ", clientRequestDict)
    print("connectionSocket: ", connectionSocket)
    connectionSocket.send(json.dumps(clientRequestDict).encode('ascii'))
    connectionSocket.close()


try:
    while 1:
        # Wait for request from a client
        connectionSocket, addr = serverSocket.accept()

        # Once the request is received, get the json version of it
        clientRequestJson = connectionSocket.recv(1024).decode('ascii')
        clientRequestDict = json.loads(clientRequestJson)

        # Create a thread and start it
        thread = threading.Thread(target=handle_request, args=[
            clientRequestDict, connectionSocket])
        threads.append(thread)
        thread.start()


except KeyboardInterrupt:
    print("\nClosing Server")
    for thread in threads:
        thread.join()
    serverSocket.close()
