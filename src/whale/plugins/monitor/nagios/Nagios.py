'''
Created on Mar 28, 2012

@author: talamoig
'''

from whale.plugins.Plugin import Plugin
from whale.utils.HTTPSClientAuthHandler import HTTPSClientAuthHandler
from copy import deepcopy
import urllib
import urllib2
import re
import time

class Nagios(Plugin):
    '''
    This class is used to interact with a nagios server
    '''

    hostLastCeckIndex=16
    hostStatusIndex=69
    hostStatusPattern="<TR><TD CLASS='dataVar'>Host Status:</td><td CLASS='dataVal'><DIV CLASS='.*'>&nbsp;&nbsp;(.*)&nbsp;&nbsp;</DIV>&nbsp;\((.*)\)</td></tr>\n"
    serviceStatusIndex=74
    serviceStatusPattern="<TR><TD CLASS='dataVar'>Current Status:</TD><TD CLASS='dataVal'><DIV CLASS='.*'>&nbsp;&nbsp;(.*)&nbsp;&nbsp;</DIV>&nbsp;\((.*)\)</TD></TR>"
    serviceAtHostPattern="<TD ALIGN=LEFT valign=center CLASS='.*'><A HREF='.*'>(.*)</A></TD></TR>"
    hostInHostGroupPattern="<TD CLASS='.*'><A HREF='status.cgi\?host=.*&style=detail' title='.*'>(.*)</A></TD>"


    def __init__(self,configfile,section=None):
        self.config(configfile,section)
        '''
        Constructor
        '''
        self.allinfo=None
        self.cachetime=time.time()-int(self.getItem("cachetime"))
    
    def __urlContentHTTPBasicAuth(self,url):
        auth_handler = urllib2.HTTPBasicAuthHandler()
        auth_handler.add_password(realm=self.getItem("realm"),uri=self.getItem("server"),user=self.getItem("username"),passwd=self.getItem("password"))
        opener = urllib2.build_opener(auth_handler)
        urllib2.install_opener(opener)
        return urllib2.urlopen(url)

    def __urlContentCertAuth(self,url):
        opener = urllib2.build_opener(HTTPSClientAuthHandler(self.getItem("userkey"),self.getItem("usercert")))
        return opener.open(url)

    def urlContent(self,path):
        url="%s%s/%s"%(self.getItem("server"),self.getItem("path"),urllib.quote(path,"?/&="))
        if self.getItem("auth")=="basic":
            return self.__urlContentHTTPBasicAuth(url)
        if self.getItem("auth")=="cert":
            return self.__urlContentCertAuth(url)
        return None

    hostLinePattern="<TD align=left valign=center CLASS='.*'><A HREF='extinfo.cgi\?type=1&host=(.*)' title='.*'>.*</A></TD>"
    serviceLinePattern="<TD ALIGN=LEFT valign=center CLASS='.*'><A HREF='extinfo.cgi\?type=2&host=.*&service=.*'>(.*)</A></TD></TR>"
    serviceStatusLinePattern="^<TD CLASS='.*'.*>(.*)</TD>$"
    
    def getAllInfo(self):
        if time.time()-self.cachetime<int(self.getItem("cachetime")):
            return self.allinfo
        self.cachetime=time.time()
        self.allinfo={}
        lines=self.urlContent("status.cgi?host=all")
        hostPatt=re.compile(self.hostLinePattern)
        servicePatt=re.compile(self.serviceLinePattern)
        serviceStatusPatt=re.compile(self.serviceStatusLinePattern)
        host=None
        service=None
        status=None
        for l in lines:
            m=hostPatt.match(l)
            if m:
                host=m.group(1)
                self.allinfo[host]={}
            m=servicePatt.match(l)
            if host and m:
                service=m.group(1)
                status=[]
            m=serviceStatusPatt.match(l)
            if service and m:
                statusinfo=m.group(1)
                self.allinfo[host][service]=statusinfo
                status=None
                service=None
        if self.getItem("hostfilter"):
            filter=self.getItem("hostfilter")
            for k in self.allinfo.keys():
                if k.find(filter)==-1:
                    del(self.allinfo[k])
        return self.allinfo

    def NagiosService2NagiosStatus(self,NagiosService,Host):
        try:            
            return self.getAllInfo()[Host][NagiosService]
        except Exception:
            return None
        

    def NagiosQueryToHost(self,queryArgs={}):
        host=None
        service=None
        inStatus=None
        outStatus=None
        if "host" in queryArgs:
            host=queryArgs["host"]
        if "service" in queryArgs:
            service=queryArgs["service"]
        if "inStatus" in queryArgs:
            inStatus=queryArgs["inStatus"]
        if "outStatus" in queryArgs:
            outStatus=queryArgs["outStatus"]                
        return self.query(host,service,inStatus,outStatus).keys()
        

    def query(self,host=None,service=None,inStatus=None,outStatus=None):
        res=deepcopy(self.getAllInfo())
        if host:
            res=dict((k,v) for k,v in res.items() if k.find(host)!=-1)
        if service:
            for host,services in res.items():
                subserv={}
                for s in services.keys():
                    if s==service:
                        subserv[s]=services[s]
                res[host]=subserv
        if inStatus:
            if not type(inStatus) is list:
                inStatus=[inStatus]
            for host,services in res.items():
                subserv={}
                for s in services.keys():
                    if services[s] in inStatus:
                        subserv[s]=services[s]
                res[host]=subserv
        if outStatus:
            if not type(outStatus) is list:
                outStatus=[outStatus]
            for host,services in res.items():
                subserv={}
                for s in services.keys():
                    if not services[s] in outStatus:
                        subserv[s]=services[s]
                res[host]=subserv
        res=dict((k,v) for k,v in res.items() if len(v)>0)
        return res

    def Hostgroup2Host(self,Hostgroup):
        lines=self.urlContent("status.cgi?hostgroup=%s&style=overview"%(Hostgroup)).read().split("\n")
        hosts=[]
        pattern=re.compile(self.hostInHostGroupPattern)
        for l in lines:
            match=pattern.match(l)
            if match:
                hosts.append(match.group(1))
        return hosts
            

    def infoFromUrl(self,path,linenum,pattern,index):
        lines=self.urlContent(path).read().split("\n")        
        patt=re.compile(pattern)
        match=patt.match(lines[linenum])
        return match.group(index)

    def _2Host(self,host=None,service=None,inStatus=None,outStatus=None):
        return self.query(host,service,inStatus,outStatus).keys()

    def _2NagiosService(self,host=None,service=None,inStatus=None,outStatus=None):
        res=self.query(host,service,inStatus,outStatus)
        return list(set([k for s in res.values() for k in s.keys()]))
    
##        return list(set(["%s@%s"%(k,s) for s in res.keys() for k in res[s].keys()]))      
##        return list(set([k for s in self.getAllInfo().values() for k in s.keys()]))
        
    def hostStatus(self,host):
        return self.infoFromUrl("type=1&host=%s"%host,self.hostStatusIndex,self.hostStatusPattern,1)

    def serviceStatus(self,host,service):
        return self.infoFromUrl("extinfo.cgi?type=2&host=%s&service=%s"%(host,service),self.serviceStatusIndex,self.serviceStatusPattern,1)

    def NagiosService2Host(self,service):
        return [host for host,services in self.getAllInfo().items() if service in services]

    def Host2NagiosService(self,host):
        return self.getAllInfo()[host].keys()
