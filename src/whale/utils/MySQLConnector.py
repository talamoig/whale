'''
Created on Jan 30, 2012

@author: talamoig
'''
from whale.Stub import Stub

import MySQLdb

class MySQLConnector(Stub):
    """A WHALE connector to MySQL DB backend"""

    def dbstart(self):
        return MySQLdb.connect(self.host,self.user,self.passwd,self.db)
    

    def __init__(self,host,user,passwd,db):
        self.host=host
        self.user=user
        self.passwd=passwd
        self.db=db
        
    
    def runquery(self,query):
        conn=self.dbstart()
        res=[]
        cursor=conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()
