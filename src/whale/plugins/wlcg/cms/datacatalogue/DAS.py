'''
Created on Jan 30, 2012

@author: talamoig
'''

import re
import time
import json
import urllib
import urllib2
from whale.plugins.Plugin import Plugin

class DAS(Plugin):
    '''
    classdocs
    '''
    
    maps={}

    def __init__(self,configFile):
        self.config(configFile)

    def rawData(self,s):
        return self.__rawData(s)

    def __Lfn2Block2Dataset(self,filename):
        try:
            blockname=self.__rawData("file=%s"%filename)['data'][0]['file'][1]['block_name']
            return self.__rawData("block=%s"%blockname)['data'][0]['block'][1]['dataset']
        except:
            return []
                   
    def __LfnData(self,filename,data):
        raw=self.__rawData("file=%s | unique | grep file.%s"%(filename,data))
        try:
            return raw['data'][0]['file'][0][data]
        except Exception:
            return None
    

    def getmap(cls,direction,site,protocol):
        try:
            return DAS.maps[DAS.keyname(direction,site,protocol)]
        except Exception:
            return None
    getmap=classmethod(getmap)
    
    def setmap(cls,direction,site,protocol,newmap):
        DAS.maps[DAS.keyname(direction,site,protocol)]=newmap
    setmap=classmethod(setmap)

    def keyname(cls,direction,site,protocol):
        return "%s-%s-%s"%(direction,site,protocol)
    keyname=classmethod(keyname)

    def __FnToFn(self,site,protocol,filename,direction):
        mymap=DAS.getmap(direction,site,protocol)
        if mymap==None:
            mymap=self.__getStorageMapping(site,direction,protocol)
            DAS.setmap(direction,site,protocol,mymap)
        return self.__FilenameMapConvert(filename,mymap)

    def Pfn2Lfn(self,pfn,CMSSite,protocol):
        return self.__FnToFn(CMSSite,protocol,pfn,"pfn-to-lfn")

    def __FilenameMapConvert(self,filename,maps):
        for m in maps:
            pattobj=re.compile(m['path-match'])
            matchobj=pattobj.match(filename)
            if (matchobj):
                filepart=matchobj.group(1)
                basepath=m['result']
                return basepath.replace("$1",filepart)
        return None    
                
    def __getStorageMapping(self,site,direction,protocol="srmv2"):
        """
        Return all available mappings for a given site/protocol
        """
        data=self.__rawData("site=%s"%site)
        maps=[]
        for info in data['data'][0]['site']:
            if info.has_key("storage-mapping"):
                for mapping in info["storage-mapping"][direction]:
                    if mapping['protocol']==protocol:
                        maps.append(mapping)
                return maps
        return None        
    
        
    def __rawData(self, query):
        """Contact DAS server and retrieve data for given DAS query"""
        params  = {'input':query, 'limit':0}
        path    = '/das/cache'
        host=self.getItem("DASHost")
        url = host + path
        headers = {"Accept": "application/json"}
        encoded_data = urllib.urlencode(params, doseq=True)
        url += '?%s' % encoded_data
        req  = urllib2.Request(url=url, headers=headers)
        opener = urllib2.build_opener()
        fdesc = opener.open(req)
        data = fdesc.read()
        fdesc.close()

        pat = re.compile(r'^[a-z0-9]{32}')
        if  data and isinstance(data, str) and pat.match(data) and len(data) == 32:
            pid = data
        else:
            pid = None
        count = 5  # initial waiting time in seconds
        timeout = 30 # final waiting time in seconds
        while pid:
            params.update({'pid':data})
            encoded_data = urllib.urlencode(params, doseq=True)
            url  = host + path + '?%s' % encoded_data
            req  = urllib2.Request(url=url, headers=headers)
            try:
                fdesc = opener.open(req)
                data = fdesc.read()
                fdesc.close()
            except urllib2.HTTPError:
                print "Error"
                return None
            if  data and isinstance(data, str) and pat.match(data) and len(data) == 32:
                pid = data
            else:
                pid = None
            time.sleep(count)
            if  count < timeout:
                count *= 2
            else:
                count = timeout
        return json.loads(data)
