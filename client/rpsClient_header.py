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
# clientSocket = socket(AF_INET, SOCK_STREAM)
# clientSocket.connect((serverName, serverPort))

rspOptions = ['r', 'p', 's']


def makeRequest(request):
    # Create game request
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))

    requestJson = json.dumps(request)
    clientSocket.send(requestJson.encode('ascii'))

    # print("Client Request: ", requestJson)
    serverResponse = clientSocket.recv(1024).decode('ascii')

    # print("From Server: ", serverResponse)
    serverResponseDict = json.loads(serverResponse)

    clientSocket.close()

    return serverResponseDict


def showResult(gameObj):
    token1 = gameObj["token1"]
    token2 = gameObj["token2"]
    player1 = gameObj["id1"]
    player2 = gameObj["id2"]

    print(f"Player {player1} result: {token1}")
    print(f"Player {player2} result: {token2}")


keepPlaying = True
while keepPlaying:

    id1 = int(input('Input your playerId: '))
    id2 = int(input('Input your opponent id: '))

    # Create Game Request:
    createGameRequest = {"Type": "CreateGame", "id1": id1, "id2": id2}
    response1 = makeRequest(createGameRequest)
    gameId = response1["gameId"]

    getGameRequest = {"Type": "GetGame", "gameId": gameId}
    gameObj = makeRequest(getGameRequest)["game"]

    # Which player am I?
    mNum = 0
    oNum = 0
    if (gameObj["id1"] == id1):
        mNum = 1
        oNum = 2
    elif (gameObj["id2"] == id1):
        mNum = 2
        oNum = 1

    if gameObj[f"token{mNum}"] == "":
        token = input("Enter a token (r, p, or s)? ")
        placeTokenRequest = {"Type": "PlaceToken",
                             "playerId": id1, "gameId": gameId, "token": token}
        makeRequest(placeTokenRequest)

    waitResponseRequest = {"Type": "WaitResponse",
                           "gameId": gameId, "waitForId": id2}
    gameObj = makeRequest(waitResponseRequest)["game"]

    showResult(gameObj)

    # Immediately terminate game:
    terminateGameRequest = {"Type": "TerminateGame",
                            "playerId": id1, "gameId": gameId}
    response_n = makeRequest(terminateGameRequest)

    keepPlaying = False if input("Keep playing (y/n)? ") == 'n' else True
