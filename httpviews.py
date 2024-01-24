from aiohttp import web
from helpers import *
from uuid import uuid4
from http.cookies import SimpleCookie
from mysql_ import Database



db = Database()


async def home_view(request):
    raw_cookies = request.headers.get("Cookie")
    if raw_cookies is not None:
        cookies = get_cookies_dict(raw_cookies=raw_cookies)
        if cookies.get("sessionid"):
            user = db.is_session_authenticated(cookies['sessionid'])
            if user:
                context = {
                    'email':user
                }
                return web.Response(text=template("chatboard.html",context=context),content_type="text/html")
    return web.HTTPFound("/login/")


async def login_get_view(request):
    raw_cookies = request.headers.get("Cookie")
    if raw_cookies is not None:
        cookies = get_cookies_dict(raw_cookies=raw_cookies)
        if cookies.get("sessionid"):
            user = db.is_session_authenticated(cookies['sessionid'])
            if user:
                return web.HTTPFound("/chatboard/")
    return web.Response(text=template("login.html"),content_type="text/html")

async def login_post_view(request):
    if request.method == "POST":
        form = await request.post()
        email = form.get("email")
        password = form.get("password")
        if db.is_credentials_valid(email=email,password=password) == False:
            return web.Response(text=template("login.html",context={'error':"username or password not valid."}),content_type="text/html") 
        sessionid = str(uuid4())
        db.create_session(email=email,sessionid=sessionid)
        cookies = {
            "sessionid":sessionid
        }
        headers = {}
        cookie_obj = SimpleCookie()
        for cookie_name , cookie_value in cookies.items():
            cookie_obj[cookie_name] = cookie_value
        for morsel in cookie_obj.values():
            morsel['path'] = '/'
            headers['Set-Cookie'] = morsel.OutputString()
        return web.HTTPFound("/chatboard",headers=headers)    
async def signup_view(request):
    if request.method == "POST":
        user_details = await request.post()
        created_ = db.create_user(user_details)
        if created_ == False:
            return web.Response(text=template("signup.html",context={"error":"Something Went Wrong !"}),content_type="text/html")
        return web.HTTPFound("/login/")
    return web.Response(text=template("signup.html"),content_type="text/html")

async def logout_view(request):
    """
    Currently not in use
    """
    raw_cookies = request.headers.get("Cookie")
    if raw_cookies:
        cookies = get_cookies_dict(raw_cookies=raw_cookies)
        if cookies.get("sessionid"):
            db.delete_session(cookies['sessionid'])
    return web.HTTPFound("/login/")

async def redirect_login(request):
    return web.HTTPFound("/login/")

