'''
Created on Jan 30, 2012

@author: talamoig
'''

import ConfigParser

class Configurable(object):
    '''
    This class provides basic funcions for configurable elements.
    See http://docs.python.org/2/library/configparser.html
    '''

    def getItem(self,item,default=None):
        try:
            return self.__configParser.get(self.__section,item)
        except ConfigParser.NoOptionError:
            return default
        except ConfigParser.NoSectionError as e:
            print "No section %s found in file %s"%(self.__section,self.__configFile)
            raise e

    def getItems(self):
        return self.__configParser.items(self.__section)
        
    def getConfig(self):
        return self.__configParser.items(self.__section)

    def hasSection(self,section):
        return self.__configParser.has_section(section)

    def __init__(self,configFile,section=None):
        '''
        Constructor. 
        '''
        self.__configParser=ConfigParser.RawConfigParser()
        if not configFile:
            configFile=Configurable.defaultConfig
        if not section:
            section=self.__class__.__name__
        self.__configFile=configFile
        self.__section=section
        files=self.__configParser.read(configFile)
        if len(files)==0:
            raise ConfigParser.NoSectionError("No section %s found on file %s"%(section,configFile))
