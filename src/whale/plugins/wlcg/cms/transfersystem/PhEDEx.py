'''
Created on Feb 27, 2012

@author: talamoig
'''

## https://cmsweb.cern.ch/phedex/datasvc/doc

from whale.utils.JsonUtils import JSonUtils
import urllib
import time

class PhEDEx(object):
    '''
    classdocs
    '''

    baseUrl="http://cmsweb.cern.ch/phedex/datasvc/json/"

    def basicQuery(self,call,options={}):
        url="%s%s/%s?%s"%(self.baseUrl,self.db,call,"&".join(["=".join([x,urllib.quote(y)]) for (x,y) in options.iteritems()]))
        return self.querier.dataFromUrl(url)['phedex']

    def setDB(self,db):
        self.db=db
        
##    def PhedexNode2PhedexAgent(self):
##        pass
    
    def Lfn2Pfn(self,lfn,PhedexNode,protocol):
        return self.basicQuery("LFN2PFN",{"lfn":lfn,"node":PhedexNode,"protocol":protocol})['mapping'][0]['pfn']
    
    ##def PhedexNode2StorageKind(self):
    ##    return self.basicQuery("")
    
    def __lfnData(self,lfn):
        return self.basicQuery("data",{"file": lfn})

    def _2PhedexNode(self):
        nodes=self.basicQuery('nodes')        
        return [n['name'] for n in nodes['node']]
        

    def __getChecksum(self,lfn):
        try:
            return self.__lfnData(lfn)['dbs'][0]['dataset'][0]['block'][0]['file'][0]['checksum']
        except Exception:
            None
    
    def Lfn2Checksum(self,lfn):
        try:
            return self.__getChecksum(lfn).split(",")[1].split(":")[1]
        except Exception:
            None


    def Lfn2Adler(self,lfn):
        try:
            return self.__getChecksum(lfn).split(",")[0].split(":")[1]
        except Exception:
            None
    
    def Lfn2Datablock(self,lfn):
        try:
            return self.__lfnData(lfn)['dbs'][0]['dataset'][0]['block'][0]['name']
        except Exception:
            None
        
    
    def Lfn2Dataset(self,lfn):
        try:
            return self.__lfnData(lfn)['dbs'][0]['dataset'][0]['name']
        except Exception:
            None
    
    def Lfn2Size(self,lfn):
        try:
            return self.__lfnData(lfn)['dbs'][0]['dataset'][0]['block'][0]['file'][0]['size']
        except Exception:
            None
    

    def Dataset2Size(self,dataset):
        try:
            return sum([int(self.Datablock2Size(block)) for block in self.Dataset2Datablock(dataset)])
        except Exception:
            None
    

    def Datablock2Size(self,datablock):
        res=self.basicQuery("data",{"block":datablock})
        try:
            return res['dbs'][0]['dataset'][0]['block'][0]['bytes']
        except Exception:
            None    

    def Datablock2Dataset(self,datablock):
        res=self.basicQuery("data",{"block":datablock})
        try:
            return res['dbs'][0]['dataset'][0]['name']
        except Exception:
            None
            
    def Dataset2Datablock(self,dataset):
        res=self.basicQuery("data",{"dataset":dataset})
        try: 
            return [block['name'] for block in res['dbs'][0]['dataset'][0]['block']]
        except Exception:
            None    
   
    def Lfn2PhedexNode(self,lfn):
        try:
            return [replica['node'] for replica in self.basicQuery("FileReplicas",{"lfn":lfn})['block'][0]['file'][0]['replica']]
        except Exception:
            None    
     
     
    def PhedexNode2TransferRequest(self,PhedexNode):
        requests=self.basicQuery("requestlist",{"node":PhedexNode})['request']
        return [r["id"] for r in requests]
##        return ["https://cmsweb.cern.ch/phedex/%s/Request::View?request=%s"%(self.db,r["id"]) for r in requests]

    def Dataset2TransferRequest(self,dataset,PhedexNode=None):
        res=self.basicQuery("requestlist",{"dataset":dataset})
        res=filter(lambda x:x['type']=='xfer',[x for x in res['request']])
        if PhedexNode:
            ret=[]
            for x in res:
                for y in x['node']:
                    if y['name']==PhedexNode:
                        ret.append(x['id'])
            return ret
            return None
        return [x['id'] for x in res]
        
    def TransferRequest2Dataset(self,transferid):
        res=self.basicQuery("transferrequests",{"request":transferid})
        try:
            return [dataset['name'] for dataset in res['request'][0]['data']['dbs']['dataset']]
        except Exception:
            return []

    def TransferRequestInfo(self,requestid):
        res=self.basicQuery("requestlist",{"request":requestid})
        requestor=res['request'][0]['requested_by']
        requestdate=res['request'][0]['time_create']
        type=res['request'][0]['type']
        dataset="\n".join(self.TransferRequest2Dataset(requestid))
        approves=[]
        ret="%s %s requested by %s on %s"%(dataset,type,requestor,time.strftime("%d %b %Y", time.localtime(float(requestdate))))
        for n in res['request'][0]['node']:
            site=n['name']
            by=n['decided_by']
            action=n['decision']
            ret+="\n@%s[%s by %s]"%(site,action,by)
        return ret                
    
    def PhedexNode2StorageElement(self,PhedexNode):
        return self.basicQuery("nodes",{"node":PhedexNode})['node'][0]['se']
        
    def Dataset2Lfn(self,dataset):
        lfns=[]
        res=self.basicQuery("data",{"dataset":dataset})
        for block in res['dbs'][0]['dataset'][0]['block']:
            for lfn in block['file']:
                lfns.append(lfn['lfn'])
        return lfns

    def Dataset2PhysicGroup(self,dataset):
        res=self.basicQuery("filereplicas",{"complete": "y","dataset":dataset})
        try:
            return res['block'][0]['file'][0]['replica'][0]['group']
        except Exception:
            None
    
    def Dataset2PhedexNode(self,dataset):
        nodes=set()
        res=self.basicQuery("filereplicas",{"complete": "y","dataset":dataset})
        for block in res['block']:
            for file in block['file'][0]['replica']:
                nodes.add(file['node'])
        return list(nodes) 

    def PhedexNode2CMSSite(self,PhedexNode):
        return PhedexNode

    def CMSSite2PhedexNode(self,CMSSite):
        return CMSSite
    
    def PhedexNode2Dataset(self,PhedexNode):
        return [dataset['name'] for dataset in self.basicQuery("subscriptions",{"dataset":"/*/*/*", "node": PhedexNode})['dataset']]    
    
    def __init__(self):
        '''
        Constructor
        '''
        self.querier=JSonUtils()
        self.db="any"
        
        
