'''
Created on Mar 20, 2012

@author: talamoig
'''

from whale.plugins.logger.WhaleLogger import WhaleLogger
import logging

class FileLogger(WhaleLogger):
    
    def __init__(self,configfile=None):
        super(FileLogger,self).__init__(configfile)
        self.setupConfig(configfile)
        self.file=open(self.getItem("file"),'a')

    def log(self,message,level=logging.WARNING):
        res=super(FileLogger,self).log(message,level)
        print("File logger:")
        print(res)
        self.file.write(res)
        
