'''
Created on Jan 30, 2012

@author: talamoig
'''
from whale.plugins.Plugin import Plugin
import socket

class System(Plugin):

    def Host2IPAddress(self,Host):
        return socket.gethostbyname(Host)
    
    def __init__(self):
        None
