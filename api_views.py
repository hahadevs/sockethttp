from aiohttp import web
from mysql_ import Database


db = Database()
db.connect()


async def username_available_api_view(request):
    form = await request.json()
    email = form.get("email")
    true_or_false = db.is_email_available(email=email)
    return web.json_response(
        data = {"true_or_false":true_or_false},
        content_type="application/json"
        )

async def remove_session_api_view(request):
    form = await request.json()
    sessionid = form.get("sessionid")
    db.delete_session(sessionid=sessionid)
