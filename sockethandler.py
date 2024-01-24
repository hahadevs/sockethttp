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
                    db.delivered_chat(email=user)
                    await self.emit("connected-user",user)
                    return
        await self.emit("status","unauthorize access.",to=sid)

    async def on_disconnect(self, sid):
        email = db.remove_socket(sid=str(sid))
        if email is not None:
            await self.emit("disconnected-user",email)

    async def on_message(self, sid, data):
        if data.get("type") == "message-seen":
            db.update_message_status_seen(data)
            senders = db.is_user_online(data['sender'])
            if senders:
                await self.emit("message-seen",data={"msid":data['msid']},to=senders)
            return
        #insert messsage in db
        db.inset_message_users_chat(data)

        # sending received response to user
        await self.emit(
            'message-received',
            data = {'msid':data['msid']},
            to = sid
        )
        # if receiver online send it to user
        users_online_with_receiver_id = db.is_user_online(data['receiver'])
        if users_online_with_receiver_id:
            db.update_message_status_delivered(data)
            await self.emit(
                'new-message',
                data = data,
                to = users_online_with_receiver_id
                )
            await self.emit(
                'message-delivered',
                data = {"msid":data['msid']},
                to = sid
            )

        