from socketio import AsyncNamespace
from mysql_ import Database
from helpers import *

db = Database()


class EntryNameSpace(AsyncNamespace):
    async def on_connect(self, sid, environ):
        raw_cookies = environ.get("HTTP_COOKIE")
        if raw_cookies:
            cookies = get_cookies_dict(raw_cookies)
            if cookies.get('sessionid'):
                user = db.is_session_authenticated(cookies['sessionid'])
                if user:
                    db.add_socket(email=user,sid=str(sid))
                    await self.emit("status","handshake-successfull",to=[sid])
                    await self.emit(
                        event="users_data_sockets_meta",
                        data={
                            "users_data":db.get_users_data(),
                            "sockets_meta":db.get_sockets_meta(),
                            "user_chat":db.get_user_chat(user)
                            },
                        to=[sid]
                        )
                    await self.emit("connected-user",user)
                    return
        await self.emit("status","unauthorize access.",to=sid)

    async def on_disconnect(self, sid):
        email = db.remove_socket(sid=str(sid))
        if email is not None:
            await self.emit("disconnected-user",email)

    async def on_message(self, sid, data):
        db.inset_message_users_chat(data)
        receiver = data['receiver']
        await self.emit(
            'new-message',
            data = data,
            to = db.is_user_online(receiver)
            )
        await self.emit(
            'message-status',
            data = {data['msid']:'ok'},
            to = [sid]
            )
        