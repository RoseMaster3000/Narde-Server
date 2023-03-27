import socketio
from decorators import login_required

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins=["https://www.piesocket.com"])
app = socketio.ASGIApp(sio)

@sio.event
async def connect(sid, environ):
    print('connect ', sid)

@sio.event
async def disconnect(sid):
    print('disconnect ', sid)

@sio.event
async def message(sid, data):
    session = await sio.get_session(sid)
    print('message from ', session['username'])

@sio.on('*')
async def catchAll(event, sid, data):
    print("[ ? ]", event, data)


if __name__=="__main__":
    import uvicorn
    uvicorn.run(app, host='localhost', port=3000)


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
