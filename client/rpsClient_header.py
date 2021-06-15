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
serverName = 'localhost'
serverPort = 6789
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

sentence = input('Input lowercase sentence: ')

clientSocket.send(sentence.encode('ascii'))
print("Sentence sent to change to upper case: ", sentence)

modifiedSentence = clientSocket.recv(1024).decode('ascii')
print("From Server: ", modifiedSentence)

clientSocket.close()





