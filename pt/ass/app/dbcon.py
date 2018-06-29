from MySQLdb import escape_string, cursors
import MySQLdb


class DbConn(object):
    def __init__(self, host="localhost", user="root", password="111000", db="asstelite"):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.conn = MySQLdb.connect(host=host, user=user, passwd=password, db=db)
        self.curser = self.conn.cursor()

    # Select user, email
    def sell(self, username, email):
        cur = self.curser
        selct = cur.execute("""SELECT * FROM users WHERE username = '%s' or email = '%s' """ %
                            (escape_string(username), escape_string(email)))
        return selct

    # Insert data
    def inss(self, username, password, email):
        cur = self.curser
        insrt = cur.execute("""INSERT INTO users (username, password, email, tracking) VALUES (%s, %s, %s, %s)""", (
                escape_string(username), escape_string(password), escape_string(email), escape_string('shotatam')))
        return insrt

    def log_p(self, username):
        cur = self.curser
        log_us = cur.execute("""SELECT * FROM users WHERE username = '%s' """ %
                             (escape_string(username)))
        return log_us

    def upd(self, username, username_ses):
        cur = self.curser
        update_u = cur.execute("""UPDATE users SET username = '%s' WHERE username = '%s' """ %
                                (escape_string(username), escape_string(username_ses)))
        return update_u

    def dlte(self, username):
        cur = self.curser
        delte = cur.execute("DELETE FROM users WHERE username = '%s' " % escape_string(username))
        self.conn.commit()
        self.curser.close()
        return delte

