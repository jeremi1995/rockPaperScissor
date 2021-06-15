#############################################################################
# Program:
#    Lab PythonRPS_Client, Computer Networking
#    Brother Jones, CSE 354
# Author:
#    Your Name
# Summary:
#    Program description ... [fill in]
#
##############################################################################
# Note: Take-2 header goes here

#
# This is just a slightly modified version of the TCPClient.py code from
# section 2.7 of the book that was used in class.
#

from socket import *
import json
serverName = 'localhost'
serverPort = 6789
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

id1 = int(input('Input your playerId: '))
id2 = int(input('Input your opponent id: '))


keepPlaying = True
while keepPlaying:
    # Create game request
    createGameRequest = {"Type": "CreateGame", "id1": id1, "id2": id2}
    createGameReqJson = json.dumps(createGameRequest)
    clientSocket.send(createGameReqJson.encode('ascii'))
    print("Client Request: ", clientSocket)
    serverCreateResponse = clientSocket.recv(1024).decode('ascii')
    print("From Server: ", serverCreateResponse)

    # Immediately terminate game:
    terminateGameRequest = {"Type": "CreateGame", "id1": id1, "id2": id2}
    terminateGameReqJson = json.dumps(createGameRequest)
    clientSocket.send(terminateGameReqJson.encode('ascii'))
    print("Client Request: ", clientSocket)
    serverTerResponse = clientSocket.recv(1024).decode('ascii')
    print("From Server: ", serverTerResponse)

    clientSocket.close()
    keepPlaying = False if input("Keep playing (y/n)? ") == 'n' else True
