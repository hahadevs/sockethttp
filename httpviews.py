from aiohttp import web
from helpers import *
from uuid import uuid4
from http.cookies import SimpleCookie


async def home_view(request):
    return web.Response(text=template("index.html"),content_type="text/html")
async def login_view(request):
    print("login view : ",request.method)
    return web.Response(text=template("login.html"),content_type="text/html")
async def signup_view(request):
    if request.method == "POST":
        user_details = await request.post()
        cookies = {
            "sessionid":str(uuid4())
        }
        headers = {}
        cookie_obj = SimpleCookie()
        for cookie_name , cookie_value in cookies.items():
            cookie_obj[cookie_name] = cookie_value
        for morsel in cookie_obj.values():
            morsel['path'] = '/'
            headers['Set-Cookie'] = morsel.OutputString()
        return web.HTTPFound("/login/",headers=headers)
    return web.Response(text=template("signup.html"),content_type="text/html")

