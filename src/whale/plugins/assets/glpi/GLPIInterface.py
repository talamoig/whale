'''
Created on Jan 30, 2012

@author: talamoig
'''
from whale.plugins.Plugin import Plugin
from GLPI import GLPIClient

class GLPIInterface(Plugin):

    def Host2PuppetClass(self,Host):
        return self.glpi.get_puppetclass(Host)

    def Host2ProductionStatus(self,Host):
        return None
    
    def _2Host(self):
        return [x['name'].encode('ascii', 'ignore') for x in self.glpi.list_computers(count=[0,10000])]

    def Host2ComputerModel(self,Host):
        hosts=self.glpi.list_computers(count=[0,10000])
        res=filter(lambda x:x['name']==Host,hosts)
        if res==[]:
            return None
        try:
            id=res[0]['id']
            model_id=str(self.glpi.get_computer(res[0]['id'])['computermodels_id'])
            model=str(self.glpi.get_object(itemtype="ComputerModel",_id=model_id)['name'])
            return model
        except Exception:
            return None


    def Host2MacAddress(self,Host):
        hosts=self.glpi.list_computers(count=[0,10000])
        res=filter(lambda x:x['name']==Host,hosts)
        if res==[]:
            return None
        try:
            return str(self.glpi.get_network_ports(res[0]['id'],itemtype='computer').values()[0]['mac'])
        except Exception:
            return None
    
    
        
    def __init__(self,configfile):
        self.config(configfile)
        self.url=self.getItem("url")
        self.username=self.getItem("username")
        self.password=self.getItem("password")        
        self.glpi=GLPIClient.RESTClient()
        self.glpi.BASEURL= ''
        self.glpi.SCHEME = 'http://'
        self.glpi.connect(self.url,self.username,self.password)
