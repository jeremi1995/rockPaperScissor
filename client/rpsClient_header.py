#############################################################################
# Program:
#    Lab PythonRPS_Client, Computer Networking
#    Brother Jones, CSE 354
# Author:
#    Jeremy Duong
# Summary:
#    This is my implementation of the Client RPS protocol
#
##############################################################################
# Note: Take-2 header goes here

#
# This is just a slightly modified version of the TCPClient.py code from
# section 2.7 of the book that was used in class.
#

from socket import *
import json
import sys

serverName = ""
serverPort = 0
if (len(sys.argv) < 3):
    print("Usage: python rpsClient.py hostname port")
    sys.exit(1)
else:
    serverName = sys.argv[1]
    serverPort = int(sys.argv[2])

# clientSocket = socket(AF_INET, SOCK_STREAM)
# clientSocket.connect((serverName, serverPort))

rspOptions = ['r', 'p', 's']


def resultString(mToken, oToken):
    if mToken == oToken:
        return "It's a DRAW!"
    elif mToken == 'r':
        return "You WON!" if oToken == 's' else "You LOST!"
    elif mToken == 'p':
        return "You WON!" if oToken == 'r' else "You LOST!"
    else:
        return "You WON!" if oToken == 'p' else "You LOST!"


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


def showResult(gameObj, mNum, oNum):
    token1 = gameObj["token1"]
    token2 = gameObj["token2"]
    player1 = gameObj["id1"]
    player2 = gameObj["id2"]
    mToken = gameObj[f"token{mNum}"]
    oToken = gameObj[f"token{oNum}"]

    print(f"Player {player1} result: {token1}")
    print(f"Player {player2} result: {token2}")
    print(resultString(mToken, oToken))


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
    print(f"Waiting for player {id2} to give his token...")
    gameObj = makeRequest(waitResponseRequest)["game"]

    showResult(gameObj, mNum, oNum)

    # Immediately terminate game:
    terminateGameRequest = {"Type": "TerminateGame",
                            "playerId": id1, "gameId": gameId}
    response_n = makeRequest(terminateGameRequest)

    keepPlaying = False if input("Keep playing (y/n)? ") == 'n' else True
