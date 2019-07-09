import json

class DatabaseAccess:

    def __init__(self):
        host = "host=claudioserv.ddns.net"
        port = "port=5432"
        database = "dbname=visites_db"
        user = "user=visites"
        password = "password=Blok9tSFvisit"
        self.conn_string = host + " " + port + " " + database + " "
        self.conn_string += user + " " + password

    def get_user(self, pseudo, password):
        req = """SELECT * FROM employee
        WHERE pseudoemployee = %s
        AND passwordemployee = %s"""
        db = connect(self.conn_string)
        cur = db.cursor()
        cur.execute(req, (pseudo, password))
        user = cur.fetchone()
        cur.close()
        db.close()
        return user

    def add_to_db(self, table, empData):
        strKeys, listValues, listTemp = "", [], []
        strValues = ""
        for key, value in empData.items():
            strKeys += key + ", "
            strValues += "%s, "
            listValues.append(value)
        for item in listValues:
            listTemp.append(item[0])
        strKeys = (strKeys[:-1])[:-1]
        strValues = (strValues[:-1])[:-1]
        req = "INSERT INTO " + table +  "(" + strKeys + ") VALUES(" + strValues + ")"
        db = connect(self.conn_string)
        db.cursor().execute(req, tuple(listTemp))
        db.commit()
        db.close()
        return None

    def get_users(self):
        req = """SELECT * FROM employee
        WHERE admin is Null"""
        db = connect(self.conn_string)
        cur = db.cursor()
        cur.execute(req)
        users = cur.fetchall()
        cur.close()
        db.close()
        return users
