'''
Created on Mar 19, 2012

@author: talamoig
'''

from whale.plugins.Plugin import Plugin
from whale.utils.Exec import Exec
import os

class SRMUtils(Plugin):
    '''
    classdocs
    '''

## common used ports:
## dCache = 8443
## StoRM = 8444
## DPM = 8446
    
    srmCommands=["copy","bringOnline","stage","mv","ls","rm",
                 "mkdir","rmdir","getPermissions","checkPermissions",
                 "setPermissions","extendFileLietime","advisoryDelete",
                 "abortRequest","abortFiles","releaseFiles","getRequestStatus",
                 "getRequestSummary","getGetRequestTokens","getFileMetaData",
                 "getSpaceTokens","getStorageElementInfo","reserveSpace",
                 "releaseSpace","getSpaceMetaData","ping"]
    
    ports=[8443,8444,8446]
    
    srmTimeout=5 ## number of seconds to wait for srm command to finish
    
    def srmCommandRun(self,srmCommand,options,storageElement,port=None,timeout=10):
        if not srmCommand in self.srmCommands:
            raise Exception, "SRM command %s unknown"%srmCommand
        command="%s -%s %s srm://%s:%d"%(self.getItem("srmcommand"),
                                            srmCommand,
                                            " ".join(options),
                                            storageElement,
                                            port)
        executer=Exec()
        return executer.osExec(command,timeout)
        

    def srmCp(self,SURL,destination=None):
        if not destination:
            destination="file:///%s"%os.getcwd()        
        command="%s '%s' '%s'"%(self.getItem("srmcp"),SURL,destination)
        print command
        executer=Exec()
        return executer.osExec(command)
    
    def backendType(self,storageElement):
        for port in self.ports:
            res=self.srmCommandRun("ping",["-2"],storageElement,port,self.srmTimeout)
            if res!=[]:
                try:
                    return res[1].split(":")[1]
                except Exception:
                    None
        return "Unknown"
        
    def __init__(self,configfile):
        '''
        Constructor
        '''
        self.config(configfile)
        
