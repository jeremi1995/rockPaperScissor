#############################################################################
# Program:
#    Lab PythonRPS_Server, Computer Networking
#    Brother Jones, CSE 354
# Author:
#    Jeremy Duong
# Summary:
#    This is my implementation of the server of RPS
#    It works like a web service that can handle different requests
#
# *****************************************************************************
#
# RPS (rock/paper/scissors) Protocol Description
# ----------------------------------------------
# Server protocol:
# For every request:
# 	Check to see what type of request it is
# (5 types: Create Game, token placement, Get Game, WaitResponse or TerminateGame):
# If(Create Game)
# 		If Game() object for the 2 players specified in the request already exists
# 			Return “Welcome back to game with {the other player}” AND GameId
# 		Else If Game() object for the 2 players specified in the request does NOT exists
# Create a Game() object with if game does not already exist
# Append the Game() object to the games list
# Return “New game with players {the other player…}” AND GameId

# Else if (Token placement)
#    Check the status of the Game object associated with the 2 players specified:
#    If Game() object doesn’t exist for the 2 players specified:
#   	Return “Invalid game”
#    If Game exists:
# 		Place player’s Token
# 		Return “RPS placed” Game() object

# Else if (Get Game):
#    If Game() exists:
# 			Return Game()
# 	 Else:
# 			Return “Game doesn’t exist”

# Else if (TerminateGame):
# 	 If Game() exists:
# 			Set Game.terminate_{player} = True
# 			If Game.terminate1 && Game.terminate2:
# 				Delete Game, pop from the list
# 				Return “Game is terminated.”
# 			Return “Terminate Request placed”
# 	 Else:
# 			Return “Game doesn’t exist”

# Else if (ResetGame):
# 		Reset token1 and token2 to "" so the client can start the next loop
#
##############################################################################

# Note: Take-2 Modification:
#
# Added:
#    - resetGame() request handler which resets the game when 2 players
#      have placed their request to play again
#    - removed waitResponse() function. Moved this waiting responsibility
#      to the client.
#
#
# This is just a slightly modified version of the TCPServer.py code from
# section 2.7 of the book that was used in class.
#

import sys
import json
import threading
import time
from socket import *

DEFAULT_VALUE = 6789
serverPort = int(sys.argv[1]) if len(sys.argv) == 2 else DEFAULT_VALUE

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('The Server is ready to receive')

threads = []
games = []

# See if the game exists
def gameExists(id1, id2):
    gameId = 0
    for game in games:
        if (game["id1"] == id1 and game["id2"] == id2) or (game["id1"] == id2 and game["id2"] == id1):
            return gameId
        gameId += 1
    return -1

# See if the game exists using gameId
def gameExistsById(gameId):
    if (gameId < len(games)):
        return gameId
    return -1

# Create a new game per request from client
def createGame(requestDict):
    id1 = requestDict["id1"]
    id2 = requestDict["id2"]
    gameId = gameExists(id1, id2)
    if gameId != -1:
        return {"message": f"Welcome back to RPS with player_{id2}!", "gameId": gameId}
    else:
        games.append({"id1": id1, "id2": id2, "token1": "",
                     "token2": "", "terminate1": False, "terminate2": False,
                      "reset1": 0, "reset2": 0})
        newGameId = len(games) - 1
        return {"message": f"Starting new game with player_{id2}", "gameId": newGameId}

# place a token per request from client
def placeToken(requestDict):
    playerId = requestDict["playerId"]
    gameId = requestDict["gameId"]
    token = requestDict["token"]

    if (gameExistsById(gameId) != -1):
        if (games[gameId]["id1"] == playerId):
            games[gameId]["token1"] = token
            return {"message": "Token placed!", "gameId": gameId}
        elif (games[gameId]["id2"] == playerId):
            games[gameId]["token2"] = token
            return {"message": "Token placed!", "gameId": gameId}

    return {"message": "Cannot place token for this game!", "gameId": gameId}

# Get send the game object back to the client
def getGame(requestDict):
    gameId = requestDict["gameId"]
    if (gameExistsById(gameId) != -1):
        return {"message": "Game found!", "game": games[gameId], "exists": 1}
    else:
        return {"message": "Game does not exist!", "game": {}, "exists": 0}

# reset a game
def reset(gameId):
    games[gameId]["token1"] = ""
    games[gameId]["token2"] = ""

# handle resetGame request
def resetGame(requestDict):
    playerId = requestDict["playerId"]
    gameId = requestDict["gameId"]

    if (gameExistsById(gameId) != -1):
        if games[gameId]["id1"] == playerId:
            games[gameId]["reset1"] = (games[gameId]["reset1"] + 1) % 2
            if (games[gameId]["reset1"] == games[gameId]["reset2"]):
                reset(gameId)
            return {"message": "Termination request placed!", "gameId": gameId}
        elif games[gameId]["id2"] == playerId:
            games[gameId]["reset2"] = (games[gameId]["reset2"] + 1) % 2
            if (games[gameId]["reset1"] == games[gameId]["reset2"]):
                reset(gameId)
            return {"message": "Reset request placed!", "gameId": gameId}
    return {"message": "Cannot reset this game!", "gameId": gameId}

# handle terminateGame request
def terminateGame(requestDict):
    playerId = requestDict["playerId"]
    gameId = requestDict["gameId"]

    if (gameExistsById(gameId) != -1):
        if games[gameId]["id1"] == playerId:
            games[gameId]["terminate1"] = True
            if (games[gameId]["terminate1"] and games[gameId]["terminate2"]):
                games.pop(gameId)
            return {"message": "Termination request placed!", "gameId": gameId}
        elif games[gameId]["id2"] == playerId:
            games[gameId]["terminate2"] = True
            if (games[gameId]["terminate1"] and games[gameId]["terminate2"]):
                games.pop(gameId)
            return {"message": "Termination request placed!", "gameId": gameId}
    return {"message": "Cannot terminate this game!", "gameId": gameId}

# handle all requests
def handle_request(clientRequestDict, connectionSocket):
    '''This function handles all kinds of requests, not just 
        the initial connection request.
    '''
    requestType = clientRequestDict["Type"]
    responseDict = {}

    if (requestType == "CreateGame"):
        responseDict = createGame(clientRequestDict)
    elif (requestType == "PlaceToken"):
        responseDict = placeToken(clientRequestDict)
    elif (requestType == "GetGame"):
        responseDict = getGame(clientRequestDict)
    elif (requestType == "ResetGame"):
        responseDict = resetGame(clientRequestDict)
    elif (requestType == "TerminateGame"):
        responseDict = terminateGame(clientRequestDict)
    else:
        responseDict = {"message": "Invalid request!"}

    connectionSocket.send(json.dumps(responseDict).encode('ascii'))
    connectionSocket.close()


#############################################################################
# This is where the server starts running
#############################################################################
try:
    while 1:
        # Wait for request from a client
        connectionSocket, addr = serverSocket.accept()

        # Once the request is received, get the json version of it
        clientRequestJson = connectionSocket.recv(1024).decode('ascii')
        clientRequestDict = json.loads(clientRequestJson)

        print(clientRequestJson)

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
