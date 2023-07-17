import socketio
import random
from asyncio import sleep as asyncSleep
from decorators import login_required, anon_required, opponent_required
from decorators import data_required, no_data
from utility import debug as print
from Player import Player
LFG = {} # keys: <Player> | value : DesiredGameType (str:"casualbackgammon")


# Player.resetTable()
Player.startTable() 
sio = socketio.AsyncServer(async_mode = 'asgi')
app = socketio.ASGIApp(
    sio,
    static_files = {
        '/': {'content_type': 'text/html', 'filename': 'index.html'},
        '/game': {'content_type': 'text/html', 'filename': 'game.html'},
        '/Build': './Build'
    }
)

@sio.event
async def connect(sid, environ):
    print('connect   ', sid)

@sio.event
async def disconnect(sid):
    player = Player.get(sid)
    if player is not None: await quitSession(player)
    print('disconnect', sid)

###################################
#  Account Management
###################################

@sio.event
@anon_required
@data_required("username", "password")
async def login(sid, data):
    player = Player.fetch(data["username"], data["password"])
    if type(player)!=Player:
        return {"status":401, "message":player}
    if (player.sid != None):
        return {"status":401, "message": f"{player.username} is logged in somewhere else."}
    # login success
    player.sid = sid
    player.clearGame()
    return {"status":200, "message":"Login Successful", "username":player.username}

@sio.event
@no_data
async def relogin(sid):
    player = Player.get(sid)
    if player==None:
        return {"status":666, "message":"Silent Error", "username":""}
    else:
        return {"status":200, "message":"Login Successful", "username":player.username}


@sio.event
@anon_required
@data_required("username", "password")
async def register(sid, data):
    if len(data["password"]) < 8:
        return {"status":400, "message":"Password must be 8 characters or longer."}
    player = Player.create(data["username"], data["password"])
    if type(player)!=Player:
        return {"status":409, "message":player}
    # register success
    return {"status":200, "message":"Registration Successful", "username":player.username}


@sio.event
@login_required
@no_data
async def logout(sid, player):
    await quitSession(player)
    return {"message":"Logged out"}


# Testing Client acknowledgments
@sio.event
@login_required
async def whoami(sid, player):
    print("whoami recieved...")
    await sio.emit(
        event = 'name',
        to = sid,
        data = {'name':player.username},
        callback = nameConfirm
    )
    return "whoami ack..."
def nameConfirm(*args):
    print("[name] event acknowledged by client:", args)


# Generic messages
@sio.event
async def message(sid, data):
    print('message:', data)
@sio.on('*')
async def catchAll(event, sid, data):
    print("[?]", f"({event})", data)


###################################
#  Matchmaking / Looking For Game (LFG)
###################################


@sio.event
@login_required
@data_required("mode", "format")
async def matchmakeStart(sid, data, player):
    global LFG
    # Validate matchmaking eligibility
    if player.opponent!=None:
        return {"status": 400, "message":"You are already in a game!"}
    if player in LFG:
        return {"status": 400, "message":"You are already looking for a game!"}
    # Validate matchmaking request paramters
    if data["format"] not in ["casual", "competetive", "casino"]:
        return {"status": 400, "message":"Unknown Game Format"}
    if data["mode"] not in ["longgammon", "mini", "backgammon", "debug"]:
        return {"status": 400, "message":"Unknown Game Mode"}
    if player in LFG:
        return {"status": 400, "message":"You are already looking for an opponent"}
    
    gametype = data['format'] + data['mode']

    # look for opponent
    opponent = None
    for queuePlayer in LFG:
        if LFG[queuePlayer] == gametype:
            opponent = queuePlayer
    # if opponent available, immediatly matchmake
    if opponent != None:
        await pairPlayers(opponent, player, data['format'], data['mode'])
    # if not available, this player enters queue (LFG)
    else:
        LFG[player] = gametype
        return {"status":200, "message":f"{player.username} looking for opponent..."}


@sio.event
@login_required
@no_data
async def matchmakeStop(sid, player):
    LFG.pop(player, None)
    return {"status":200, "message":"Stopped looking for opponent."}


async def pairPlayers(playerA, playerB, gameFormat, gameMode):
    LFG.pop(playerA, None)
    LFG.pop(playerB, None)
    dice = [1,2,3,4,5,6]
    random.shuffle(dice)
    dice = dice[:2]
    if dice[0] > dice[1]: playerA.active=True
    else: playerB.active=True
    nextDice = [random.randint(1,6), random.randint(1,6)]
    await startGame(playerA, playerB, "white", dice, nextDice, gameFormat, gameMode)
    await startGame(playerB, playerA, "black", dice, nextDice, gameFormat, gameMode)


async def startGame(player, opponent, color, firstDice, nextDice, gameFormat, gameMode):
    player.opponent = opponent
    player.gameFormat = gameFormat
    player.gameMode = gameMode
    print("gameStart", firstDice, "|", nextDice, "|", player)
    await sio.emit(
        event = 'startGame',
        to = player.sid,
        data = {
            'gameMode': gameMode,
            'gameFormat': gameFormat,
            'you': player.username,
            'opponent': opponent.username,
            'color': color,
            'firstDice': firstDice,
            'nextDice': nextDice
        }
    )

###################################
#  Game Terminations
###################################

@sio.event
@login_required
@opponent_required
@no_data
async def abandon(sid, player, opponent):
    await player.abandon(sio)
    return {"message": "you abandoned your opponent..."}

@sio.event
@login_required
@opponent_required
@no_data
async def loseGame(sid, player, opponent):
    player.clearGame()
    return {"message": "You Lost!"}


@sio.event
@login_required
@opponent_required
async def winGame(sid, player, opponent):
    player.beatOpponent()
    player.clearGame()
    return {"message": "You Win!"}


async def quitSession(player):
    player.sid = None         # clear socket id
    LFG.pop(player, None)     # if queued for game, leave LFG
    await player.abandon(sio) # if in game, abandon / notify opponent


###################################
#  Relay Game Actions
###################################


@sio.event
@login_required
@opponent_required
async def relayAction(sid, data, player, opponent):
    # TODO: validate data (makey sure 2D list that uses dice values...)
    print("ACTION", player, data)

    # reject action from non-active
    if not player.active:
        return {"status": 400, "message":"It is not your turn"}

    nextDice = [random.randint(1,6), random.randint(1,6)]

    # show player the dice for next turn (opponent's turn)
    await sio.emit(
        event = 'nextDice',
        to = player.sid,
        data = nextDice
    )

    # give opponent this players actions [AND] dice for next turn
    await sio.emit(
        event = 'opponentAction',
        to = opponent.sid,
        data = {
            "actions": data,
            "nextDice": nextDice
        }
    )

    # swap active player
    player.active = False
    opponent.active = True

    return {"status": 200, "message":"Your actions have been transmitted"}


# https://www.youtube.com/watch?v=tHQvTOcx_Ys
# https://python-socketio.readthedocs.io/en/latest/api.html#socketio.Server.emit
# https://python-socketio.readthedocs.io/en/latest/server.html#event-callbacks
# https://python-socketio.readthedocs.io/en/latest/server.html#user-sessions


# @sio.event
# def roomTest(sid, data):
#     sio.enter_room(sid, 'cool_room')
#     sio.emit(
#         'my event',
#         {'dice': 2,'chip': 11},
#         room='cool_room'
#     )
#     sio.leave_room(sid, 'cool_room')