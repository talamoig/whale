'''
Created on Mar 20, 2012

@author: talamoig
'''

from whale.plugins.Plugin import Plugin
import logging

class WhaleLogger(Plugin):
    
    def __init__(self,configfile=None):
        self.levels={}
        self.levels["DEBUG"]=logging.DEBUG
        self.levels["INFO"]=logging.INFO
        self.levels["WARNING"]=logging.WARNING
        self.levels["ERROR"]=logging.ERROR
        self.levels["CRITICAL"]=logging.CRITICAL

        self.config(configfile)
        logging.basicConfig(format=self.getItem("format"),filename=self.getItem("file"))
        self.logger=logging.getLogger()
        self.logger.setLevel(self.levels[self.getItem("loglevel")])

    def log(self,message,level=logging.WARNING):
        return self.logger.log(level,message)
        
