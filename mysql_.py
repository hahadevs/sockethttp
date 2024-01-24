import mysql.connector
from datetime import datetime
from time import sleep

class Database:
    def _connector(method,*args,**kwargs):
        def wrapper(self,*args,**kwargs):
            self.connect()
            output = method(self,*args,**kwargs)
            self.close_conn()
            return output
        return wrapper
    def __init__(self) -> None:
        self.host = 'localhost'
        self.user = 'root'
        self.__password = '' 
        self.database = 'sockethttp_db'
        self.__conn = False
        self.__cursor = False
    def connect(self):
        try:
            self.__conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.__password,
                database=self.database,
            )
            self.conn = self.__conn
            self.__cursor = self.__conn.cursor()
        except Exception as e :
            raise ConnectionRefusedError(str(e))
    @_connector
    def create_user(self,users_details:dict=None) -> None:
        email = users_details.get("email")
        password = users_details.get("password")
        firstname = users_details.get("firstname")
        lastname = users_details.get("lastname")
        command_for_users_auth = f"""insert into users_auth (email,password) values ('{email}','{password}');"""
        command_for_users_data = f"""insert into users_data (email,firstname,lastname) values ('{email}','{firstname}','{lastname}');"""
        try:
            self.__cursor.execute(command_for_users_auth)
            self.__conn.commit()
            self.__cursor.execute(command_for_users_data)
            self.__conn.commit()
            return True
        except Exception as e:
            print("create_user : ",e)
            return False
    @_connector
    def create_session(self,sessionid:str,email:str):
        command = f"""insert into session_auth (email,sessionid) values ('{email}','{sessionid}');"""
        try:
            self.__cursor.execute(command)
            self.__conn.commit()
            return True
        except Exception as e :
            return False
    @_connector
    def inset_message_users_chat(self,message_dict:dict):
        try:
            sender = message_dict['sender']
            receiver = message_dict['receiver']
            message_datetime = datetime.now()
            message = message_dict['message']
            msid = message_dict['msid']
            status = "not-delivered"
            command = f"""insert into users_chat(`sender`,`receiver`,`datetime`,`message`,`msid`,`status`) values ('{sender}','{receiver}','{message_datetime}','{message}','{msid}','{status}');"""
            self.__cursor.execute(command)
            self.__conn.commit()
            # command = f"""select * from users_chat where id = LAST_INSERT_ID();"""
            # self.__cursor.execute(command)
            return True
        except Exception as e:
            print("inset_message_message : ",e)
    @_connector
    def add_socket(self,sid,email):
        command = f"""insert into sockets_meta (sid,email) values ('{sid}','{email}');"""
        try:
            self.__cursor.execute(command)
            self.__conn.commit()
        except Exception as e :
            print("add_socket : ",e)
    @_connector
    def update_message_status_delivered(self,data):
        msid = data['msid']
        command = f"""update users_chat set status = 'delivered' where msid = '{msid}';"""
        try:
            self.__cursor.execute(command)
            self.__conn.commit()
        except Exception as e :
            print("update_message_status_delivered : ",e)
    @_connector
    def update_message_status_seen(self,data):
        msid = data['msid']
        command = f"""update users_chat set status = 'seen' where msid = '{msid}';"""
        try:
            self.__cursor.execute(command)
            self.__conn.commit()
        except Exception as e :
            print("update_message_status_seen : ",e)
    @_connector
    def delivered_chat(self,email):
        command = f"update users_chat set status = 'delivered' where receiver = '{email}' and status = 'not-delivered';"
        try:
            self.__cursor.execute(command)
            self.__conn.commit()
        except Exception as e:
            print("delivered_chat : ",e)
    @_connector
    def delete_session(self,sessionid):
        command = f"""delete from session_auth where sessionid = '{sessionid}';"""
        try:
            self.__cursor.execute(command)
            self.__conn.commit()
        except Exception as e :
            print("delete_session : ",e)
    @_connector
    def remove_socket(self,sid):
        command = f"""select email from sockets_meta where sid = '{sid}';"""
        self.__cursor.execute(command)
        rows = self.__cursor.fetchall()
        email = None
        if len(rows) > 0 :
            email = rows[0][0]
        command = f"""delete from sockets_meta where sid = '{sid}';"""
        try:
            self.__cursor.execute(command)
            self.__conn.commit()
            if email:
                command = f"select * from sockets_meta where email = '{email}';"
                self.__cursor.execute(command)
                if len(self.__cursor.fetchall()) == 0:
                    return email
            return None
        except Exception as e:
            print("remove_socket : ",e)
    @_connector
    def clear_sockets_meta(self):
        command = """delete from sockets_meta ;"""
        self.__cursor.execute(command)
        self.__conn.commit()  
    @_connector
    def get_sockets_meta(self)->dict:
        command = """select email from sockets_meta ;""" 
        self.__cursor.execute(command)
        rows = self.__cursor.fetchall()
        return rows
    @_connector
    def get_users_data(self)->list:
        command = """select * from users_data;"""
        try:
            self.__cursor.execute(command)
            rows = self.__cursor.fetchall()
            return rows
        except Exception as e:
            print("get_users_data : ",e)
    @_connector
    def get_user_chat(self,email:str)->list:
        try:
            command = f"""select * from users_chat where sender = '{email}' or receiver = '{email}' ;"""
            self.__cursor.execute(command)
            chat = self.__cursor.fetchall()
            return chat
        except Exception as e:
            print("get_user_chat : ",e)
    @_connector
    def is_credentials_valid(self,email,password):
        try:
            command = f"""select email,password from users_auth where email='{email}';"""
            self.__cursor.execute(command)
            row = self.__cursor.fetchall()
            if  len(row) == 1 and row[0][1] == password :
                return True
            else:
                return False
        except Exception as e :
            print("is_credentials_valid : ",e)
            return False
    @_connector
    def is_email_available(self,email):
        command = f"""select email from users_auth where email = '{email}';"""
        self.__cursor.execute(command)
        rows = self.__cursor.fetchall()
        if len(rows) == 0 : return True
        else : return False
    @_connector
    def is_session_authenticated(self,sessionid):
        command = f"""select email from session_auth where sessionid = '{sessionid}' ;"""
        try:
            self.__cursor.execute(command)
            rows = self.__cursor.fetchall()
            if len(rows) == 1 :
                return rows[0][0]
            else:
                return False
        except Exception as e:
            print("is_session_authenticated : ",e)
            return False
    @_connector
    def is_user_online(self,user)->list:
        command = f"select sid from sockets_meta where email = '{user}'"
        try:
            self.__cursor.execute(command)
            rows = self.__cursor.fetchall()
            return [row[0] for row in rows]
        except Exception as e :
            print("is_user_online : ",e)
    def close_conn(self):
        if self.__conn:
            self.__conn.close()
if __name__ == "__main__":
    db = Database()
    db.connect()