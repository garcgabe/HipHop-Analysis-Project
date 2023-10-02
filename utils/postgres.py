import psycopg2 as pg

class Postgres():
    # holds two attributes:
    #   connection to the database
    #   cursor, which is used to execute queries and close itself
    def __init__(self):
        self.conn = pg.connect(
            host="localhost",
            database="hiphop",
            user="garcgabe",
            password="password"
        )
        self.cursor = self.conn.cursor()
    
    def execute_query(self, query, params):
        self.cursor.execute(query, params)
        self.conn.commit()

    def fetch_data(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()