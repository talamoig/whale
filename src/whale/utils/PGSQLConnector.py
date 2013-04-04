'''
Created on Jan 30, 2012

@author: talamoig
'''

import psycopg2

class PGSQLConnector(object):
    """A WHALE connector to PostgreSQL DB backend"""

    def __init__(self,host,user,passwd,db):
        conn_string = "host='%s' dbname='%s' user='%s'"%(host,db,user)
        try:
            connection=psycopg2.connect(conn_string)
            self.cursor=connection.cursor()
        except psycopg2.Error, e:
            print e.pgerror            
    
    def runquery(self,query):
        self.cursor.execute(query)
        return self.cursor.fetchall()
