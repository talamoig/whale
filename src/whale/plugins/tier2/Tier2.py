import subprocess
import os
from whale.plugins.Func import Func
from whale.plugins.Plugin import Plugin

'''
Created on Apr 29, 2012

@author: talamoig
'''

class Tier2(Plugin):

    def __init__(self):
        '''
        Constructor
        '''
        self.func=Func()

    def _2Host(self,match=""):
        return self.func.funcclientsname("*%s*"%match)

    def Host2Shutdown(self,Host):
        hosts=self.func.funcclientsname(Host)
        for host in hosts:
            result=whaleutil.runcommand(host,'/sbin/shutdown -h now')[host][0]
            whaleutil.addEvent("management","shutdown of %s: %s"%(host,comment),result)
            
    def Host2Reboot(self,Host,comment=None):    
        hosts=self.func.funcclientsname(Host)
        for host in hosts:
            self.func.funcclients(host).reboot.reboot()[host]

    def Host2Exec(self,Host,Command):
        host=self.func.funcclientsname(Host)
        if len(host)!=1:
            return None
        res=self.func.runcommand(Host,Command).values()[0]
        if res[0]==0:
            return res[1].split("\n")[:-1]
        else:
            return res[1]

    def Host2RemoveFromFuncAndPuppet(self,Host):
        hosts=self.func.funcclientsname(Host)
        for host in hosts:
            self.Host2RemoveFromPuppet(host)
            self.Host2RemoveFromFunc(host)
    
    def Host2RemoveFromPuppet(self,Host):
        command=["/usr/sbin/puppetca","--clean", "%s"%Host]
        subprocess.call(command)

    def Host2RemoveFromFunc(self,Host):
        command=["/usr/bin/certmaster-ca","--clean", "%s"%Host]
        subprocess.call(command)

    def Host2File(self,Host,File,Destination=None):
        hosts=self.func.funcclients(Host)        
        if Destination==None:
            Destination=os.getcwd()
        try:
            hosts.local.getfile.get(File,Destination)
        except Exception:
            None
        
    def Host2OSInstall(self,Host):
        hosts=self.func.funcclientsname(Host)
        for host in hosts:
            self.Host2Reboot(host)
            self.Host2RemoveFromFuncAndPuppet(host)
            
    def Host2YaimReconfig(self,Host):
        return self.Host2Exec(Host,"rm -f /opt/glite/yaim/reconfig.log")
            
