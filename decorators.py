from functools import wraps
from Player import Player

def login_required(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        sid = args[0]
        player = Player.get(sid)
        if player == None:
            return {"status":401, "reason":'authentication required'}
        kwargs["player"] = player
        return await f(*args, **kwargs)
    return wrapper

def anon_required(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        sid = args[0]
        player = Player.get(sid)
        if player != None:
            return {"status":401, "reason":'anonymity required'}
        return await f(*args, **kwargs)
    return wrapper

def opponent_required(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        player = kwargs["player"]
        if player.opponent == None:
            return {"status":401, "reason":'opponent required'}
        kwargs["opponent"] = player.opponent
        return await f(*args, **kwargs)
    return wrapper

def data_required(*args):
    required = list(args)
    def decorator(f):
        @wraps(f)
        async def wrapper(*args, **kwargs):
            data = args[1]
            if type(data) is not dict:
                return {"status":400, "reason":f"[{f.__name__}] event expects dictionary (via JSON)"}
            if any([(key not in data) for key in required]):
                fields = ", ".join(required)
                return {"status":422, "reason":f"[{f.__name__}] event expects [{fields}] fields"}
            return await f(*args, **kwargs)
        return wrapper
    return decorator


def no_data(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        return await f(*args[:1], **kwargs)
    return wrapper