from whale.plugins.wlcg.cms.transfersystem.PhEDEx import PhEDEx
from whale.plugins.wlcg.cms.datacatalogue.DAS import DAS
from whale.plugins.wlcg.cms.dashboard.Dashboard import Dashboard
from whale.plugins.wlcg.GridMapDir import GridMapDir
from whale.plugins.storagesystem.dcache.DCache import DCache
from whale.plugins.batchsystem.lsf.LSF import LSF
from whale.plugins.monitor.nagios.Nagios import Nagios
from whale.plugins.assets.glpi.GLPIInterface import GLPIInterface
from whale.plugins.Meta import Meta
from whale.plugins.tier2.Tier2 import Tier2
from whale.plugins.logger.WhaleLogger import WhaleLogger
from whale.plugins.system.System import System
from whale.plugins.wlcg.srm.SRMUtils import SRMUtils

phedex=PhEDEx()
phedex.setDB("prod")
dcache=DCache(config)
das=DAS(config)
lsf=LSF(config)
sys=System()
glpi=GLPIInterface(config)
t2=Tier2()
gridmapdir=GridMapDir(config)
nagiosT2=Nagios(config,"T2")
nagiosT2.setDescription("nagiosT2")
nagiosInfn=Nagios(config,"INFN")
nagiosInfn.setDescription("nagiosInfn")
nagiosCMS=Nagios(config,"NagiosCMS")
nagiosCMS.setDescription("nagiosCMS")
srm=SRMUtils(config)
dashboard=Dashboard(config)
whale=Meta()
whaleLogger=WhaleLogger(config)
whale.addLogger(whaleLogger)

whale.setDefault("PhedexNode","T2_IT_Rome")
whale.setDefault("CMSSite","T2_IT_Rome")
whale.addPlugin(phedex)
whale.addPlugin(t2)
whale.addPlugin(sys)
whale.addPlugin(dcache)
whale.addPlugin(das)
whale.addPlugin(dashboard)
whale.addPlugin(lsf)
whale.addPlugin(gridmapdir)
whale.addPlugin(nagiosT2)
whale.addPlugin(nagiosInfn)
whale.addPlugin(nagiosCMS)
whale.addPlugin(glpi)
w=whale
wns=t2._2Host("cmsrm-wn*")
ces=t2._2Host("cmsrm-cream*")
st=t2._2Host("cmsrm-st*")

def reinstallHost(host,workernode=False):
    None
#     if workernode:
#         w.convert("Host","NodeClose",host)
#         jobs=lsf.RunningNode2JobId(host.split(".")[0])
#         if len(jobs)>0:
#             print "Still %d jobs running on %s. Delaying reboot"%(len(jobs),host)
#         else:
#             print "0 jobs running. Rebooting node. Check kickstart configuration and puppet profile"            
#             w.convert("Host","OSInstall",host)
#     else:
#         w.convert("Host","OSInstall",host)

def getDHCPHost(host):
    mac=w.convert("Host","MacAddress",host)
    ipaddr=w.convert("Host","IPAddress",host)
    dhcp="host %s {\n\thardware ethernet %s;\n\tfixed-address %s;\n}\n"%(host,mac[0],ipaddr[0])
    return dhcp
    
