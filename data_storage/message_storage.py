import sys
from pathlib import Path
sys.path.append(f"{Path(__file__).resolve().parent.parent}")

from utils import date_string, date_stamp
from data_storage.sqlite_controller import SqliteController


class MessageStorage(object):

    def __init__(self, first_msg: str):
        self.title = f"{date_string()}_{first_msg}"
        self.editor = SqliteController()

    def __str__(self):
        return f"<MessageStorage session: {self.title}>"

    __repr__ = __str__

    def write_message(self, msg: str, character: str):
        self.editor.connect_db("conversation")
        session = self.title
        name = character
        create_time = f"{date_stamp().lstrip('_')}"
        content = msg
        insert_data_query = '''INSERT INTO conversation (session, name, create_time, content)
                                      VALUES ('{}', '{}', '{}', '{}')'''.format(session, name, create_time, content)
        self.editor.write(conn="conversation", insert_data_query=insert_data_query)
