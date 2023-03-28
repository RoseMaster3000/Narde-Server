import socketio
from decorators import login_required
from utility import debug

sio = socketio.AsyncServer(async_mode='asgi')
app = socketio.ASGIApp(sio)

@sio.event
async def connect(sid, environ):
    debug('connect   ', sid)

@sio.event
async def disconnect(sid):
    debug('disconnect', sid)


@sio.event
@login_required
async def message(sid, data):
    debug('message:', data)

    # session = await sio.get_session(sid)
    # debug('message from ', session['username'])



@sio.on('*')
async def catchAll(event, sid, data):
    debug("[?]", f"({event})", data)



# @sio.event
# @login_required
# def whoAmI(sid, data):
#     print(sid)
#     sio.emit('youAre', {'data': sid})


# @sio.event
# def roomTest(sid, data):
#     sio.enter_room(sid, 'cool_room')
#     sio.emit(
#         'my event',
#         {'dice': 2,'chip': 11},
#         room='cool_room'
#     )
#     sio.leave_room(sid, 'cool_room')






# https://python-socketio.readthedocs.io/en/latest/server.html#event-callbacks

# https://python-socketio.readthedocs.io/en/latest/server.html#user-sessions
# @sio.event
# async def connect(sid, environ):
#     username = authenticate_user(environ)
#     await sio.save_session(sid, {'username': username})



# https://www.youtube.com/watch?v=tHQvTOcx_Ys