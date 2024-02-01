import os
import sqlite3

from pathlib import Path


class SqliteController(object):
    _COUNT_ = 0

    def __init__(self):
        self.path = Path(os.path.abspath(__file__)).parent
        self.conn_c, self.conn_s = None, None
        self.init_db()

    def __str__(self):
        return f"<SqliteController connections_alive: {SqliteController._COUNT_}>"

    __repr__ = __str__

    def connect_db(self, table_name):
        if table_name == "conversation":
            self.conn_c = sqlite3.connect(f'{self.path}/{table_name}.db')
            SqliteController._COUNT_ += 1

        if table_name == "settings":
            self.conn_s = sqlite3.connect(f'{self.path}/{table_name}.db')
            SqliteController._COUNT_ += 1

    def close_connection(self, conn_name: str):
        if conn_name == "conversation":
            self.conn_c.close()
            SqliteController._COUNT_ -= 1
        if conn_name == "settings":
            self.conn_s.close()
            SqliteController._COUNT_ -= 1

    def init_db(self):
        self.connect_db("conversation")
        self.connect_db("settings")
        if None in (self.conn_c, self.conn_s):
            raise ValueError(
                "connection is None, which is unexpected. Reconnect db with statement: SSqliteController.connect_db()")
        self.conn_c.execute('CREATE TABLE IF NOT EXISTS conversation '
                            '(id INTEGER PRIMARY KEY, '
                            'session TEXT,'
                            'name TEXT, '
                            'create_time TEXT,'
                            'content TEXT)')
        self.conn_s.execute('CREATE TABLE IF NOT EXISTS settings '
                            '(id INTEGER PRIMARY KEY, '
                            'port TEXT,'
                            'transit_port TEXT, '
                            'system_prompt TEXT,'
                            'aiserver_command TEXT,'
                            'auto_prompt TEXT,'
                            'auto_copy_last TEXT,'
                            'python_executable TEXT)')

        self.conn_c.commit()
        self.conn_s.commit()

    def write(self, conn: str, insert_data_query: str):
        if conn == "settings":
            connection = self.conn_s
        elif conn == "conversation":
            connection = self.conn_c
        else:
            raise TypeError("connection error")
        connection.cursor().execute(insert_data_query)
        connection.commit()

    def read(self, conn: str, read_data_query: str):
        if conn == "settings":
            connection = self.conn_s
        elif conn == "conversation":
            connection = self.conn_c
        else:
            raise TypeError("connection error")

        result = connection.cursor().execute(read_data_query).fetchall()
        return result

    def update_settings(self, **settings):
        connection = self.conn_s
        query = "UPDATE settings SET {} WHERE id=1"
        values = str()
        for setting, value in settings.items():
            values += f"{setting} = '{value}',"
        query = query.format(values.rstrip(","))
        print(query)
        result = connection.cursor().execute(query).fetchall()
        connection.commit()
        return result

    def read_settings(self):
        read_data_query = "SELECT * FROM settings"
        result = self.conn_s.cursor().execute(read_data_query).fetchall()
        if result:
            # print(result)
            # "auto_prompt": "YES",
            # "auto_copy_last": "YES",
            ID, port, transit_port, system_prompt, aiserver_command, auto_prompt, auto_copy_last, python_executable = result[0]
            return {
                "port": port,
                "transit_port": transit_port,
                "system_prompt": system_prompt,
                "aiserver_command": aiserver_command,
                "auto_prompt": auto_prompt,
                "auto_copy_last": auto_copy_last,
                "python_executable": python_executable,
            }
        else:
            return None


if __name__ in "__main__":
    pass
    # current_path = Path.cwd()
    # print(f'{current_path}/conversation.db')
    # conn = sqlite3.connect(f'{current_path}/conversation.db')
    #
    # # Create a cursor object to interact with the database
    # c = conn.cursor()
    #
    # # Create a table
    # c.execute('CREATE TABLE IF NOT EXISTS conversation '
    #           '(id INTEGER PRIMARY KEY, '
    #           'session TEXT,'
    #           'name TEXT, '
    #           'create_time TEXT,'
    #           'content TEXT)')
    #
    # # Commit the changes and close the connection
    # conn.commit()
    # conn.close()
