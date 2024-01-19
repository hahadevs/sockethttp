from socketio import AsyncNamespace


class MyCustomNamespace(AsyncNamespace):
    def on_connect(self, sid, environ):
        pass

    def on_disconnect(self, sid):
        pass

    def on_my_event(self, sid, data):
        self.emit('my_response', data)
