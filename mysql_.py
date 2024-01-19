import mysql.connector


class Database:
    def __init__(self) -> None:
        self.host = 'localhost'
        self.user = 'root'
        self.__password = '' 
        # self.database = 'sockethttp'
        self.__conn = False
        self.__cursor = False
    def connect(self):
        try:
            self.__conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.__password,
                # database=self.database,
            )
            self.conn = self.__conn
            self.__cursor = self.__conn.cursor()
            self.cursor = self.__cursor
        except Exception as e :
            raise ConnectionRefusedError(str(e))
        
        
if __name__ == "__main__":
    db = Database()
    db.connect()