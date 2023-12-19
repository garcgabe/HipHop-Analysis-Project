import psycopg2 as pg
#from utils.env import host, database, user, password, port

class Postgres():
    # holds two attributes:
    #   connection to the database
    #   cursor, which is used to execute queries and close itself
    def __init__(self, host, database, user, password, port):
        self.conn = pg.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        self.cursor = self.conn.cursor()
    
    def execute_query(self, query, params=None):
        self.cursor.execute(query, params)
        self.conn.commit()

    def fetch_data(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()