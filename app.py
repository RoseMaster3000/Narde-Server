import socketio
from decorators import login_required, anon_required
from utility import debug as print
from Player import Player


Player.startTable()
sio = socketio.AsyncServer(async_mode = 'asgi')
app = socketio.ASGIApp(
    sio,
    static_files = {
        '/': {'content_type': 'text/html', 'filename': 'index.html'}
    }
)



# verify dictionary contains specified keys (returns True if all keys exist)
def verifyDict(dictionary, *args):
    if type(dictionary)!=dict: return False
    return not any([(arg not in dictionary) for arg in args])


@sio.event
async def connect(sid, environ):
    print('connect   ', sid)

@sio.event
async def disconnect(sid):
    player = Player.get(sid)
    if player is not None: player.sid = None
    print('disconnect', sid)


@sio.event
@anon_required
async def login(sid, data):
    print(f"{type(data)}  :  {data}")
    # bad request
    if not verifyDict(data, "username", "password"):
        return {"status":422, "reason":"[login] event requires [username] and [password] fields"}
    # login error
    player = Player.fetch(data["username"], data["password"])
    if type(player)!=Player:
        return {"status":401, "reason":player}
    # login success
    player.sid = sid
    return {"status":200, "reason":"Login Successful"}


@sio.event
@login_required
async def logout(sid, data, player):
    player.sid = None


@sio.event
@login_required
async def whoami(sid, data, player):
    await sio.emit(
        event = 'name',
        to = sid,
        data = {'username': player.username},
        callback = nameConfirm
    )
    

def nameConfirm(*args):
    print("[name] event acknowledged by client:", args)



@sio.event
async def message(sid, data):
    print('message:', data)

@sio.on('*')
async def catchAll(event, sid, data):
    print("[?]", f"({event})", data)



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