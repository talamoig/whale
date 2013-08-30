'''
Created on Jan 30, 2012

@author: talamoig
'''

from whale.utils.Configurable import Configurable
import collections

class PluginException(Exception):
    pass


class Plugin(object):
    '''
    Base class from which every WHALE plugin must inherit.
    It provides simple function so that every plugin can be configured through a text file.
    The config file has to be in the .ini format.
    See http://docs.python.org/2/library/configparser.html for further details.
    '''

    descr=None
    name=None
    descr=None

    def setName(self,name):
        '''
        Function to set a shortname to recall this plugin
        '''
        self.name=name

    def getName(self):
        if self.name==None:
            return self.__class__.__name__
        return self.name
    
    def setDescription(self,descr):
        '''
        Function to set a human-readable description of the plugin.
        It can be configured:
        -in the config file
        -at runtime
        The runtime takes precedence over the config file
        '''
        self.descr=descr

    def getDescription(self):
        '''
        Returns the human-readable plugin description.
        '''        
        return self.descr
        

    def getItem(self,item):
        '''
        Returns the value of the current item in the config file
        '''
        return self.configurable.getItem(item)

    def getItems(self):
        '''
        Returns the list of items/values of the specific section in form of a dictionary
        '''
        return dict(self.configurable.getItems())
        

    def config(self,configfile="/etc/whale/whale.conf",section=None):
        '''
        Setup different parameters for using a configuration file.
        configfile = the file to be used
        section = the [section] to be used. defaults to class name
        '''
        if section==None:
            section=self.__class__.__name__
        self.configurable=Configurable(configfile,section)
        if not self.configurable.hasSection(section):
            raise PluginException("No section %s found in configuration file %s"%(section, configfile))        
        descr=self.getItem("description")
        if descr!=None:
            self.setDescription(descr)
        name=self.getItem("name")
        if name!=None:
            self.setName(name)
        
#    def flatten(self,x):
#        if isinstance(x, collections.Iterable):
#            return [a for i in x for a in self.flatten(i)]
#        else:
#            return [x]
  
                
