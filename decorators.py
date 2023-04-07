from functools import wraps
from Player import Player

def login_required(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        player = Player.get(args[0])
        if player == None:
            return {"status":401, "reason":'authentication required'}
        kwargs["sid"] = args[0]
        kwargs["data"] = args[1] if (len(args)>1) else {}
        kwargs["player"] = player
        return await f(**kwargs)
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

def data_required(*args):
    required = list(args)
    def decorator(f):
        @wraps(f)
        async def wrapper(*args, **kwargs):
            sid = args[0]
            data = args[1]
            fields = ", ".join(required)
            if type(data) is not dict:
                return {"status":400, "reason":f"[{f.__name__}] event expects dictionary (via JSON)"}
            if any([(key not in data) for key in required]):
                return {"status":422, "reason":f"[{f.__name__}] event expects [{fields}] fields"}
            return await f(*args, **kwargs)
        return wrapper
    return decorator