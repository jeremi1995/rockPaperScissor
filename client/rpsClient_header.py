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

playerId = int(input('Input playerId: '))
playerRSP = input('Enter r/s/p: ')[0]

clientRequest = {"playerId": playerId, "opponentId": playerRSP}
clientRequestJson = json.dumps(clientRequest)

clientSocket.send(clientRequestJson.encode('ascii'))
print("Client Request: ", clientRequestJson)

serverResponse = clientSocket.recv(1024).decode('ascii')
print("From Server: ", serverResponse)

clientSocket.close()
