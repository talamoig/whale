from whale.plugins.wlcg.cms.transfersystem.PhEDEx import PhEDEx
from whale.plugins.wlcg.cms.datacatalogue.DAS import DAS
from whale.plugins.wlcg.cms.CMS import CMS
from whale.plugins.wlcg.GridMapDir import GridMapDir
from whale.plugins.storagesystem.dcache.DCache import DCache
from whale.plugins.batchsystem.lsf.LSF import LSF
from whale.plugins.monitor.nagios.Nagios import Nagios
from whale.plugins.Meta import Meta
from whale.plugins.wlcg.srm.SRMUtils import SRMUtils

phedex=PhEDEx()
phedex.setDB("prod")
dcache=DCache(config)
das=DAS(config)
lsf=LSF(config)
cms=CMS(config)
gridmapdir=GridMapDir(config)
nagiosT2=Nagios(config,"T2")
nagiosT2.setDescription("nagiosT2")
nagiosInfn=Nagios(config,"INFN")
nagiosInfn.setDescription("nagiosInfn")
nagiosCMS=Nagios(config,"NagiosCMS")
nagiosCMS.setDescription("nagiosCMS")
srm=SRMUtils(config)
whale=Meta()

whale.setDefault("PhedexNode","T2_IT_Rome")
whale.setDefault("CMSSite","T2_IT_Rome")
whale.addPlugin(phedex)
whale.addPlugin(cms)
whale.addPlugin(dcache)
whale.addPlugin(das)
whale.addPlugin(lsf)
whale.addPlugin(gridmapdir)
whale.addPlugin(nagiosT2)
whale.addPlugin(nagiosInfn)
whale.addPlugin(nagiosCMS)
w=whale
