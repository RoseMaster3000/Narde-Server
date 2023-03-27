import socketio
from functools import wraps
from SQLITE import querySQL

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        print(args)
        search = querySQL("SELECT * FROM online WHERE sid = ?", args[0])
        if len(search) == 0:
            raise ConnectionRefusedError('authentication failed')
        else:
            return f(*args, **kwargs)
    return wrapper


# def admin_required(f):
#     @wraps(f)
#     def wrapper(*args, **kwargs):
#         if current_user.get("sid") and current_user.get("admin"):
#             return f(*args, **kwargs)
#         else:
#             return emit("401", {"message":"administrators only"})
#     return wrapper

# def alpha_required(f):
#     @wraps(f)
#     def wrapper(*args, **kwargs):
#         if current_user.get("sid") and current_user.get("alpha"):
#             return f(*args, **kwargs)
#         elif current_user.get("sid"):
#             return emit("401", {"message": "{} is not in closed alpha".format(current_user.get("username"))} )
#         else:
#             return emit("401", {"message": "authentication + alpha access required"} )
#     return wrapper

# def anon_required(f):
#     @wraps(f)
#     def wrapper(*args, **kwargs):
#         if not current_user.get("sid"):
#             return f(*args, **kwargs)
#         else:
#             return emit("401", {"message":"anonimity required (log out)"})
#     return wrapper