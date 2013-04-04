'''
Created on Mar 20, 2012

@author: talamoig
'''

from whale.plugins.logger.WhaleLogger import WhaleLogger
import logging

class StandardOutLogger(WhaleLogger):
    file=None
    
    def __init__(self,configfile=None):
        super(WhaleLogger,self).__init__()
        self.setupConfig(configfile)

    def log(self,message,level=logging.INFO):
        res=super.log(message,level)
        print(res)
        
