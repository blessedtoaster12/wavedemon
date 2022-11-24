from pathlib import Path
import sqlite3

#TODO: Add additional column for file paths to items (files for songs, folders for pretty much everything else)

class Database:
    '''
    Allows interaction between sqlite database and wavedemon

    Keyword arguments:
    Path db - path to database file, defaults to wavedemon directory

    Database: wavedemon
    Table: downloaded_item_ids
    ID | Author | Title | Type
    00000000 | "ABC"  | "Best title ever" | "Album, PLaylist, or Song"
    Maybe add mixes and radios to compatible types
    '''
    def __init__(self, db = Path("data\\wavedemon.db")):
        self.db_conn = None

        try:
            self.db_conn = sqlite3.connect(db)
        except sqlite3.Error():
            quit()

        self.cur = self.db_conn.cursor()

        self.cur.execute("CREATE TABLE if not EXISTS downloaded_item_ids(id, author, title, type")

    def __del__(self):
        self.db_conn.close()

    def insert(self, item_id, author, title, item_type):
        '''
        Insert row into db

        Keyword arguments:
        item_id - Item ID
        author - Item Author (User if playlist)
        title - Title/Name of item
        item_type - One of the types described in class docstring
        '''
        self.cur.execute(f"INSERT INTO downloaded_item_ids VALUES ({item_id}, {author}, {title}, {item_type})")
        self.db_conn.commit()

    def delete(self, item_id, author, title, item_type):
        '''
        Delete exact row from db

        Keyword arguments:
        item_id - Item ID
        author - Item Author (User if playlist)
        title - Title/Name of item
        item_type - One of the types described in class docstring
        '''
        self.cur.execute(f"DELETE FROM downloaded_item_ids WHERE ({item_id}, {author}, {title}, {item_type})")
        self.db_conn.commit()
