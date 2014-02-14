'''
Created on Mar 20, 2012

@author: talamoig
'''

import glob
import os
import re
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
        ## a dn in the gridmap dir has special characters quoted
        ## the : is a special case:
        ## it is quoted everywhere except when appears at the end of the dn for adding the pool information, eg.
        ## %2fdc%3dorg%2fdc%3ddoegrids%2fou%3dservices%2fcn%3duscmspilot50%2fglidein%2d1%2et2%2eucsd%2eedu:prdcms
        ## %2fc%3dit%2fo%3dinfn%2fou%3dpersonal%20certificate%2fl%3dcnaf%2fcn%3dgiuseppe%20misurelli:dteam
        str=self.getItem("gridmapdir")+quote(userOrDn,":").lower().replace(".","%2e").replace("-","%2d").replace("_","%5f")
        pattobj=re.compile("(.*)(:[^:]*)")
        match=pattobj.match(str)
        if (match):
            str=match.group(1).replace(":","%3a")+match.group(2)
        return str
    
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

    def _2User(self,filter=None):
        return self.__ToSomething(self.userglob,filter)

    def _2DN(self,filter=None):
        return self.__ToSomething(self.dnglob,filter)

    def byinode(self,inode):
        command="/usr/bin/find %s -inum %s 2> /dev/null"%(self.getItem("gridmapdir"),inode)
        ex=Exec()
        res=ex.osExec(command)[:-1]
        if len(res)!=2:
            return None
        return res

    def getCompanion(self,one):
        try:
            all=self.byinode(self.getInode(self._toFilename(one)))
            return unquote(basename(all[all.index(self._toFilename(one))-1]))
        except Exception:
            return None
        
    def DN2User(self,Dn):
        return self.getCompanion(Dn)
        
    def User2DN(self,User):
        return self.getCompanion(User)
