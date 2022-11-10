import pymysql


class db_util:
    def __init__(self, host, port, user, psw, db, charset='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.psw = psw
        self.db = db
        self.charset = charset

    def connect(self):
        self.conn = pymysql.Connect(host=self.host, port=self.port, user=self.user, passwd=self.psw, db=self.db,
                                    charset=self.charset)
        self.cur = self.conn.cursor()

    def select_all(self, sql):
        self.cur.execute(sql)
        self.data = self.cur.fetchall()

    def close(self):
        self.cur.close()
        self.conn.close()
