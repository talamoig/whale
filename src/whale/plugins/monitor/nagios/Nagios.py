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
    hostStatusPattern="<TR><TD CLASS='dataVar'>Host Status:</td><td CLASS='dataVal'><DIV CLASS='.*'>&nbsp;&nbsp;(.*)&nbsp;&nbsp;</DIV>&nbsp;\((.*)\)</td></tr>"
    serviceStatusIndex=74
    serviceStatusPattern="<TR><TD CLASS='dataVar'>Current Status:</TD><TD CLASS='dataVal'><DIV CLASS='.*'>&nbsp;&nbsp;(.*)&nbsp;&nbsp;</DIV>&nbsp;\((.*)\)</TD></TR>"
    serviceAtHostPattern="<TD ALIGN=LEFT valign=center CLASS='.*'><A HREF='.*'>(.*)</A></TD></TR>"
    hostInHostGroupPattern="<TD CLASS='.*'><A HREF='status.cgi\?host=.*&style=detail' title='.*'>(.*)</A></TD>"


    def resetCache(self):
        self.cachetime=time.time()-int(self.getItem("cachetime"))
        
    def __init__(self,configfile,section=None):
        self.config(configfile,section)
        '''
        Constructor
        '''
        self.allinfo=None
        self.resetCache()
    
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
        cgipath=self.getItem("path","/nagios/cgi-bin/")
        url="%s%s/%s"%(self.getItem("server"),cgipath,urllib.quote(path,"?/&=+"))
        if self.verbose():
            print "Url:%s"%url
        if self.getItem("auth")=="basic":
            return self.__urlContentHTTPBasicAuth(url)
        if self.getItem("auth")=="cert":
            return self.__urlContentCertAuth(url)
        return None

    infoLinePattern="<td align=[']{0,1}left[']{0,1} valign=center class='(.*)'><a href='extinfo.cgi.type=2&host=(.*)&service=.*'>(.*)</a></td></tr>"
    
    allInfoPage="status.cgi?host=all&limit=0&start=0&limit=100000"

    def getAllInfo(self):
        if time.time()-self.cachetime<int(self.getItem("cachetime")):
            return self.allinfo
        self.cachetime=time.time()
        self.allinfo={}
        lines=self.urlContent(self.allInfoPage)
        infoPatt=re.compile(self.infoLinePattern,re.IGNORECASE)
        host=None
        service=None
        status=None
        for l in lines:
            m=infoPatt.match(l)
            if m:
                status=m.group(1)
                host=m.group(2)
                service=m.group(3)
                if not self.allinfo.has_key(host):
                    self.allinfo[host]={}
                self.allinfo[host][service]=status
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
        pattern=re.compile(self.hostInHostGroupPattern,re.IGNORECASE)
        for l in lines:
            match=pattern.match(l)
            if match:
                hosts.append(match.group(1))
        return hosts
            

    def infoFromUrl(self,path,linenum,pattern,index):
        lines=self.urlContent(path).read().split("\n")        
        patt=re.compile(pattern,re.IGNORECASE)
        match=patt.match(lines[linenum])
        if not match:
            return None
        return match.group(index)

    def _2Host(self,Host=None,Service=None,inStatus=None,outStatus=None):
        return self.query(Host,Service,inStatus,outStatus).keys()

    def _2Service(self,Host=None,Service=None,inStatus=None,outStatus=None):
        res=self.query(Host,Service,inStatus,outStatus)
        return list(set([k for s in res.values() for k in s.keys()]))    
        
    def Host2Status(self,Host):
        return self.infoFromUrl("/extinfo.cgi?type=1&host=%s"%Host,self.hostStatusIndex,self.hostStatusPattern,1)

    def Service2Status(self,Service,Host):
        Service.replace(" ","+")
        return self.infoFromUrl("extinfo.cgi?type=2&host=%s&service=%s"%(Host,Service),self.serviceStatusIndex,self.serviceStatusPattern,1)
    
    def Service2Host(self,Service):
        return [host for host,services in self.getAllInfo().items() if Service in services]

    def Host2Service(self,Host):
        return self.getAllInfo()[Host].keys()
