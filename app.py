import socketio
from decorators import login_required, anon_required, data_required
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
@data_required("username", "password")
async def login(sid, data):
    # login error
    player = Player.fetch(data["username"], data["password"])
    if type(player)!=Player:
        return {"status":401, "reason":player}
    # login success
    player.sid = sid
    return {"status":200, "reason":"Login Successful"}


@sio.event
@anon_required
@data_required("username", "password")
async def register(sid, data):
    p = Player.create(data["username"], data["password"])
    if type(p)!=Player:
        return {"status":409, "reason":p}
    # register success
    return {"status":200, "reason":f"{data['username']} Registration Successful"}


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