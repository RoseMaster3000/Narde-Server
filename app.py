import socketio
from Decorators import login_required
sio = socketio.AsyncServer()


@sio.event
async def connect(sid, environ, auth):
    print('connect ', sid)

@sio.event
async def disconnect(sid):
    print('disconnect ', sid)


@sio.event
@login_required
async def whoAmI(sid, data):
    print(sid)
    sio.emit('youAre', {'data': sid})





@sio.event
async def roomTest(sid, data):
    sio.enter_room(sid, 'cool_room')
    sio.emit(
        'my event',
        {'dice': 2,'chip': 11},
        room='cool_room'
    )
    sio.leave_room(sid, 'cool_room')

