import func.overlord.client as fc
import simplejson as json
from whale.plugins.Plugin import Plugin

'''
Created on Apr 29, 2012

@author: talamoig
'''

class Func(Plugin):

    def __init__(self):
        '''
        Wrapper class to func https://fedorahosted.org/func/
        It provides generic whale-like methods and func-specific methods.
        '''
        None
        
    def _2Host(self,hostexp="*"):
        return self.funcclientsname(hostexp)
    
    def funcclientsname(self,hostexp="*"):
        return self.funcclients("*%s*"%hostexp).list_minions()
    
    def funcclients(self,hostexp):
        return fc.Client(hostexp)

    def Host2Commandrun(self,Host,Command):
        return funcclients(Host).command.run(Command)
    
    def runcommand(self,hostexp,command):
        return self.funcclients(hostexp).command.run(command)

