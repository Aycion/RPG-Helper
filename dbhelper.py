import sqlite3


class DBHelper:
    def __init__(self, dbname="pathfinder.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)


    def setup(self):
        tblstmt = "CREATE TABLE IF NOT EXISTS players (char_name text, player text)"
        plidx = "CREATE INDEX IF NOT EXISTS playerIndex ON players (char_name ASC)"
        self.conn.execute(tblstmt)
        self.conn.execute(plidx)
        characters = self.conn.execute("SELECT char_name FROM players")

        self.conn.commit()


    def add_char(self, char_name, player):
        stmt = "INSERT INTO players (char_name, player) VALUES (?, ?)" #add character to table of all characters

        char = self.scrub(char_name)
        charstmt = "CREATE TABLE IF NOT EXISTS {} (char_info text, item text)".format(char) #create table for the specific character with columns for info and items
        invidx = "CREATE INDEX IF NOT EXISTS itemIndex ON {} (item ASC)".format(char) #create an index on the items column

        nmstmt = "INSERT INTO {} (char_info) VALUES (?)".format(char)
        nmargs = ("Name: {}".format(char), )


        args = (char_name, player)
        self.conn.execute(stmt, args)

        self.conn.execute(charstmt)
        self.conn.execute(invidx)
        self.conn.execute(nmstmt, nmargs)

        self.conn.commit()


    def delete_char(self, char_name):
        char = self.scrub(char_name)
        stmt = "DROP TABLE IF EXISTS {}".format(char)

        try:
            self.conn.execute(stmt)
            self.conn.commit()
            return True
        except sqlite3.DatabaseError as e:
            return False





    def add_item(self, char_name, item):
        selstmt = "SELECT char_name FROM players"
        stmt = "INSERT INTO {} (item)".format(char_name)


    def get_items(self, owner):
        stmt = "SELECT description FROM items WHERE owner = (?)"
        args = (owner, )
        return [x[0] for x in self.conn.execute(stmt, args)]


    def scrub(self, name):
        return ''.join( chr for chr in name if chr.isalnum() )
