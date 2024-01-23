import socketio
from aiohttp import web
from helpers import *
from httpviews import *
from sockethandler import *
from api_views import *


cors_allowed_origins = ['https://b009-112-196-88-154.ngrok-free.app']
sio = socketio.AsyncServer(cors_allowed_origins=cors_allowed_origins)

app = web.Application()

sio.attach(app=app)


# Handle Sockets 
# sockethandler.py
sio.register_namespace(EntryNameSpace('/'))

# Http view 
# httpviews.py

# ---------  GET REQUESTS   ------------------
app.router.add_get("/signup",handler=signup_view)
app.router.add_get("/signup/",handler=signup_view)

app.router.add_get("/login",handler=login_get_view)
app.router.add_get("/login/",handler=login_get_view)

app.router.add_get("/",handler=redirect_login)
app.router.add_get("/chatboard",handler=home_view)
app.router.add_get("/chatboard/",handler=home_view)

#----------  POST REQUESTS --------------------
app.router.add_post("/signup",handler=signup_view)
app.router.add_post("/signup/",handler=signup_view)

app.router.add_post("/login",handler=login_post_view)
app.router.add_post("/login/",handler=login_post_view)

# Api Views
# apiviews.py

app.router.add_post("/api/is-email-available",handler=username_available_api_view)
app.router.add_delete("/api/delete-session/",handler=remove_session_api_view)


if __name__ == "__main__":
    db = Database()
    db.clear_sockets_meta()
    web.run_app(app=app,host="0.0.0.0",port=8000)