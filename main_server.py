import socketio
from aiohttp import web
from helpers import *
from httpviews import *
from sockethandler import *

sio = socketio.AsyncServer()

app = web.Application()

sio.attach(app=app)

# Handle Sockets 
# sockethandler.py
sio.register_namespace(MyCustomNamespace('/'))

# Http view 
# httpviews.py

# ---------  GET REQUESTS   ------------------
app.router.add_get("/signup",handler=signup_view)
app.router.add_get("/signup/",handler=signup_view)

app.router.add_get("/login",handler=login_view)
app.router.add_get("/login/",handler=login_view)

app.router.add_get("/",handler=home_view)

#----------  POST REQUESTS --------------------
app.router.add_post("/signup",handler=signup_view)
app.router.add_post("/signup/",handler=signup_view)

app.router.add_post("/login",handler=login_view)
app.router.add_post("/login/",handler=login_view)


if __name__ == "__main__":
    web.run_app(app=app,host="127.0.0.1",port=8000)