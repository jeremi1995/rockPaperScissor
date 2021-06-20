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
import time

#############################################################################
# Return the result of the match given the player's token and the token of
# the opponent
#############################################################################


def resultString(mToken, oToken):
    if mToken == oToken:
        return "It's a DRAW!"
    elif mToken == 'r':
        return "You WON!" if oToken == 's' else "You LOST!"
    elif mToken == 'p':
        return "You WON!" if oToken == 'r' else "You LOST!"
    else:
        return "You WON!" if oToken == 'p' else "You LOST!"

#############################################################################
# Make a request to the server:
# The request can be any of the following type:
#    - CreateGame
#    - GetGame
#    - PlaceToken
#    - ResetGame
#    - TerminateGame
#############################################################################


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

#############################################################################
# Shows the result of the game once the 2 players have placed their tokens
# If one player has left the game based on the "terminate1" or "terminate2"
# attributes of the game object, then indicate so
#############################################################################


def showResult(gameObj, mNum, oNum):
    if gameObj[f"terminate{oNum}"] and gameObj[f"token{oNum}"] == "":
        oId = gameObj[f"id{oNum}"]
        print(f"Player {oId} has left the game...")

    else:
        mToken = gameObj[f"token{mNum}"]
        oToken = gameObj[f"token{oNum}"]

        print(f"Your token: {mToken}")
        print(f"Opponent token: {oToken}")
        print(resultString(mToken, oToken))


#############################################################################
# This is where the program starts
#############################################################################
serverName = ""
serverPort = 0

if (len(sys.argv) < 3):
    print("Usage: python rpsClient.py hostname port")
    sys.exit(1)
else:
    serverName = sys.argv[1]
    serverPort = int(sys.argv[2])

acceptableInputs = ['r', 'p', 's', 'q']

# Initial information about the player and the opponent
id1 = int(input('Input your playerId: '))
id2 = int(input('Input your opponent id: '))

# Create a game based on the 2 id's
gameId = makeRequest({"Type": "CreateGame", "id1": id1, "id2": id2})[
    "gameId"]

# Main game loop:
keepPlaying = True
while keepPlaying:

    # Create Game Request:
    gameObj = makeRequest({"Type": "GetGame", "gameId": gameId})["game"]

    # Which player am I?
    mNum = 1 if gameObj["id1"] == id1 else 2
    oNum = 1 if gameObj["id1"] == id2 else 2

    # Get user's input:
    userInput = ""
    while userInput not in acceptableInputs:
        userInput = input("Enter a token (r, p, s) or 'q' to quit? ")
        if userInput not in acceptableInputs:
            print("Invalid input!")

    # if 'q': terminate the game
    # if not 'q': continue the game as normal
    if userInput == "q":
        makeRequest({"Type": "TerminateGame",
                     "playerId": id1, "gameId": gameId})
        keepPlaying = False
    else:
        token = gameObj[f"token{mNum}"]
        if token == "":
            makeRequest({"Type": "PlaceToken", "playerId": id1,
                        "gameId": gameId, "token": userInput})
        else:
            print(
                f"Cannot change token already placed! Last token placed is '{token}'")

        # Wait until the reponse of the getGame request contains a token2
        # that is not an empty string
        print(f"Waiting for player {id2} to give his token...")
        keepWaiting = True
        while keepWaiting:
            gameObj = makeRequest(
                {"Type": "GetGame", "gameId": gameId})["game"]
            # If the token of the other player is not empty, or
            # the game object no longer exists, exit the loop
            if (gameObj[f"token{oNum}"] != "" or gameObj[f"terminate{oNum}"]):
                keepWaiting = False

            # If the other player happens to quit the game mid way, stop playing
            if gameObj[f"terminate{oNum}"]:
                keepPlaying = False

        # Once the result is received from the other player, show it:
        showResult(gameObj, mNum, oNum)

        if (keepPlaying):  # If the other person still wants to keep playing
            # Finally, reset game:
            makeRequest({"Type": "ResetGame",
                        "playerId": id1, "gameId": gameId})

            # Only start the next iteration once the other player is done
            # with the current iteration
            waitingForOpponentToReset = True
            while waitingForOpponentToReset:
                gameObj = makeRequest(
                    {"Type": "GetGame", "gameId": gameId})["game"]
                if gameObj["reset1"] == gameObj["reset2"]:
                    waitingForOpponentToReset = False

# finally, make sure to place in the vote to let server knows the game
# is ready to be deleted
makeRequest({"Type": "TerminateGame",
             "playerId": id1, "gameId": gameId})

# Be nice.
print("Thank you for playing!")
