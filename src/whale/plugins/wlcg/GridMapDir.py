'''
Created on Mar 20, 2012

@author: talamoig
'''

import glob
import os
from os import stat
from os.path import basename
from urllib import quote,unquote
from whale.utils.Exec import Exec
from whale.plugins.Plugin import Plugin

class GridMapDir(Plugin):

    dnglob='%*'
    userglob='[!%]*'

    def __init__(self,configfile=None):
        self.config(configfile)

    def fileList(self,globString):
        return map(lambda x: basename(x),glob.glob( os.path.join(self.getItem("gridmapdir"),globString)))

    def _toFilename(self,userOrDn):
        return self.getItem("gridmapdir")+quote(userOrDn,":").lower().replace(".","%2e").replace("-","%2d").replace("_","%5f")
    
    def getInode(self,path):
        try:
            return stat(path).st_ino
        except Exception:
            return None

    def __ToSomething(self,glob,needle):
        something=map(unquote, self.fileList(glob))
        if needle:
            something=filter(lambda x:x.lower().find(needle.lower())!=-1,something)
        return something

    def _2User(self,needle=None):
        return self.__ToSomething(self.userglob,needle)

    def _2DN(self,needle=None):
        return self.__ToSomething(self.dnglob,needle)

    def byinode(self,inode):
        command="/usr/bin/find %s -inum %s 2> /dev/null"%(self.getItem("gridmapdir"),inode)
        ex=Exec()
        res=ex.osExec(command)[:-1]
        if len(res)!=2:
            return None
        return res

    def getTheCompanion(self,one):
        try:
            all=self.byinode(self.getInode(self._toFilename(one)))
            return unquote(basename(all[all.index(self._toFilename(one))-1]))
        except Exception:
            return None
        
    def DN2User(self,Dn):
        return self.getTheCompanion(Dn)
        
    def User2DN(self,User):
        return self.getTheCompanion(User)
