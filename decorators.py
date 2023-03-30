from functools import wraps
from Player import Player

def login_required(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        sid = args[0]
        player = Player.get(sid)
        if player == None:
            return 401, 'authentication required'
        args = (*args, player)
        return await f(*args, **kwargs)
    return wrapper

def anon_required(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        sid = args[0]
        player = Player.get(sid)
        if player != None:
            return 401, 'anonymity required'
        return await f(*args, **kwargs)
    return wrapper