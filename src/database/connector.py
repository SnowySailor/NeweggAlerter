import psycopg2
import os
import psycopg2.extras

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(f"dbname=betterhelp user={os.getenv('PG_USER', 'postgres')} password={os.getenv('PG_PASS', '')} host=localhost port=5432")
        psycopg2.extras.register_uuid()
        self.conn.autocommit = True

    def cur(self):
        return self.conn.cursor()
