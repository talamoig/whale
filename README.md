#WHALE

## Quickstart installation
To install:

    git clone https://github.com/talamoig/whale
   cd whale/src
   sudo python setup.py install
   python

And then on the Python prompt:
    
    from whale.plugins.wlcg.cms.transfersystem.PhEDEx import PhEDEx
    phedex=PhEDEx()
    phedex.setDB("prod")
    phedex._2PhedexNode()
    #[u'T2_PK_NCP', u'T3_US_FIT', u'T3_US_UCD', u'T3_MX_Cinvestav', u'T3_IR_IPM', u'T3_KR_KNU', u'T2_TH_CUNSTDA', u'T1_RU_JINR_Disk', u'T3_HR_IRB', u'T3_US_NU', u'T3_US_Vanderbilt_EC2', u'T2_MY_UPM_BIRUNI', u'T3_BG_UNI_SOFIA', u'T3_IT_Firenze', u'T3_US_FSU', u'T3_US_FNALXEN', u'T2_PT_NCG_Lisbon', u'T3_KR_UOS', u'T3_US_FIU', u'T3_TW_NCU', u'T2_RU_PNPI', u'T3_FR_IPNL', u'T3_CN_PKU', u'T3_US_Cornell', u'T1_IT_CNAF_Disk', u'T3_GR_IASA_HG', u'T2_FR_GRIF_IRFU', u'T3_UVA_Buffer', u'T3_US_TTU', u'T0_CH_CERN_Export', u'T0_CH_CERN_MSS', u'T1_IT_CNAF_Buffer', u'T1_IT_CNAF_MSS', u'T1_US_FNAL_Buffer', u'T1_US_FNAL_MSS', u'T1_FR_CCIN2P3_Buffer', u'T1_FR_CCIN2P3_MSS', u'T1_ES_PIC_Buffer', u'T1_ES_PIC_Disk', u'T1_ES_PIC_MSS', u'T1_UK_RAL_Buffer', u'T1_UK_RAL_MSS', u'T2_IT_Bari', u'T2_CN_Beijing', u'T2_BE_IIHE', u'T2_BE_UCL', u'T2_UK_SGrid_Bristol', u'T2_HU_Budapest', u'T2_CH_CSCS', u'T2_US_Caltech', u'T2_DE_DESY', u'T3_GR_Demokritos', u'T2_EE_Estonia', u'T2_US_Florida', u'T2_FR_GRIF_LLR', u'T2_BR_UERJ', u'T2_FI_HIP', u'T2_RU_IHEP', u'T2_RU_ITEP', u'T2_RU_JINR', u'T2_KR_KNU', u'T2_IT_Legnaro', u'T2_UK_London_Brunel', u'T2_UK_London_IC', u'T3_UK_London_QMUL', u'T3_UK_London_RHUL', u'T2_US_MIT', u'T2_US_Nebraska', u'T2_IT_Pisa', u'T2_US_Purdue', u'T2_DE_RWTH', u'T2_IT_Rome', u'T2_UK_SGrid_RALPP', u'T2_RU_SINP', u'T2_BR_SPRACE', u'T2_ES_CIEMAT', u'T2_US_UCSD', u'T2_AT_Vienna', u'T2_PL_Warsaw', u'T2_US_Wisconsin', u'T3_DE_Karlsruhe', u'T3_US_Minnesota', u'T3_IT_Napoli', u'T3_IT_Perugia', u'T3_US_Princeton', u'T3_US_UIowa', u'T2_FR_IPHC', u'T2_ES_IFCA', u'T3_US_UCR', u'T2_US_Vanderbilt', u'T2_RU_INR', u'T3_US_FNALLPC', u'T3_UK_SGrid_Oxford', u'T3_ES_Oviedo', u'T3_CO_Uniandes', u'T3_UK_London_UCL', u'T3_US_UMD', u'T2_GR_Ioannina', u'T3_UMiss_Buffer', u'T2_UA_KIPT', u'T3_UCLASaxon_Buffer', u'T3_US_Kansas', u'T3_US_Colorado', u'T2_IN_TIFR', u'T2_TR_METU', u'T2_RU_RRC_KI', u'T3_CH_PSI', u'T3_GR_IASA_GR', u'T3_US_Rutgers', u'T3_US_Rice', u'T3_UK_ScotGrid_ECDF', u'T3_UK_ScotGrid_GLA', u'T2_FR_CCIN2P3', u'T3_US_Omaha', u'T3_US_Brown', u'T3_US_UMiss', u'T3_IT_Trieste', u'T3_IT_Bologna', u'T1_UK_RAL_Disk', u'T3_RU_FIAN', u'T3_BY_NCPHEP', u'T3_HU_Debrecen', u'T3_TH_CHULA', u'T3_US_SDSC', u'T3_US_JHU', u'T3_US_OSU', u'T3_US_UVA', u'T3_US_NotreDame', u'T3_IT_MIB', u'T3_US_TAMU', u'T3_TW_NTU_HEP', u'T3_US_PuertoRico', u'T2_CH_CERN', u'T1_US_FNAL_Disk', u'T1_DE_KIT_Disk', u'T1_FR_CCIN2P3_Disk', u'T3_KR_KISTI', u'T3_US_UTENN', u'T3_US_Princeton_ICSE', u'T1_DE_KIT_Buffer', u'T1_DE_KIT_MSS', u'T3_NZ_UOA', u'T3_US_Baylor', u'T2_PL_Swierk', u'T3_US_MIT']

You can get the IDs of all the not approved transfers at a site:

    phedex.PhedexNode2TransferRequest("T2_IT_Rome",approved=False)
    #['24352', '394170', '64500', '157225', '367808', '310606', '388385', '30630', '353', '253166', '30301', '19681', '66539', '203045', '30269', '117485', '401119', '406810', '397655', '240966', '140645', '241886', '367807', '24348', '24347', '387300', '21621', '108766', '17941', '21641', '181785', '49871', '367809', '248367', '420063', '414870', '403919', '101890', '318786', '53439', '181787', '339786', '19761', '367810', '24345', '63499', '248346', '102013', '393576', '320266', '200145', '400350', '382308', '24349', '148827', '220606', '108765']

And know the dataset they corresponds. For the first, for example:
    phedex.TransferRequest2Dataset('24352')
    #[u'/CSA07Electron/CMSSW_1_6_7-CSA07-Chowder-I1-PDElectron-Skims1-wToENu_Filter/USER', u'/CSA07Electron/CMSSW_1_6_7-CSA07-Gumbo-I1-PDElectron-Skims1-wToENu_Filter/USER', u'/CSA07Electron/CMSSW_1_6_7-CSA07-Stew-B2-PDElectronReReco-100pb-Skims1-wToENu_Filter/USER', u'/CSA07Electron/CMSSW_1_6_7-CSA07-Stew-C1-PDElectron-Skims1-wToENu_Filter/USER']

`PhEDEx` plugin can handle different types that can be used with the `Meta` plugin:

	 from whale.plugins.Meta import Meta
	 whale=Meta()
	 whale.types()
	 #[]
	 whale.addPlugin(phedex)
	 whale.types()
	 #['TransferRequest', 'StorageElement', 'Checksum', 'Lfn', 'Dataset', 'PhysicGroup', 'Adler', 'CMSSite', 'PhedexNode', 'Pfn', 'Datablock', 'Size']
	 
With this plugin we can use the more general `convert` function:

     datasets=whale.convert('PhedexNode','Dataset',"T2_IT_Rome")
     len(datasets)
     #2141
     datasets[0]
     #u'/TTToHplusBWB_csbar_M-155_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM'
     

We can get the list of files (accessible via SRM):

     whale.convert("Dataset","Pfn",datasets[0],more={'PhedexNode':'T2_IT_Rome','protocol':'srm'})
     #[u'srm://cmsrm-se01.roma1.infn.it:8443/srm/managerv2?SFN=/pnfs/roma1.infn.it/data/cms/store/mc/Summer12_DR53X/TTToHplusBWB_csbar_M-155_8TeV-pythia6-tauola/AODSIM/PU_S10_START53_V7C-v1/20000/46FD8D3C-586A-E211-B206-E0CB4E19F95B.root', u'srm://cmsrm-se01.roma1.infn.it:8443/srm/managerv2?SFN=/pnfs/roma1.infn.it/data/cms/s
     # continues...

Or accessible in direct mode:

   whale.convert("Dataset","Pfn",datasets[0],more={'PhedexNode':"T2_IT_Rome",'protocol':'direct'})
   #[u'/pnfs/roma1.infn.it/data/cms/store/mc/Summer12_DR53X/TTToHplusBWB_csbar_M-155_8TeV-pythia6-tauola/AODSIM/PU_S10_START53_V7C-v1/20000/B445BA38-796A-E211-B306-002590747DDC.root', u'/pnfs/roma1.infn.it/data/cms/store/mc/Summer12_DR53X/TTToHplusBWB_csbar_M-155_8TeV-pythia6-tauola/AODSIM/PU_S10_START53_V7C-v1/20000/2C8A
   # continues...



Introduction
======
WHALE: A management tool for Tier-2 LCG Sites

The LCG (Worldwide LHC Computing Grid) is a grid-based hierarchical
computing distributed facility, composed of more than 140 computing
centers, organized in 4 tiers, by size and offer of services. Every
site, although indipendent for many technical choices, has to provide
services with a well-defined set of interfaces. For this reason,
different LCG sites need frequently to manage very similar situations,
like jobs behaviour on the batch system, dataset transfers between
sites, operating system and experiment software installation and
configuration, monitoring of services.

WHALE is a generic, site indipendent tool written in python: it allows
administrator to interact in a uniform and coherent way with several
subsystems using a high level syntax which hides specific commands.

The architecture of WHALE is based on the plugin concept and on the
possibility of connecting the output of a plugin to the input of the
next one, in a pipe-like system, giving the administrator the
possibility of making complex functions by combining the simpler
ones. The core of WHALE just handles the plugin orchestrations, while
even the basic functions (eg. the WHALE activity logging) are
performed by plugins, giving the capability to tune and possibly
modify every component of the system. WHALE already provides many
plugins (making use of other APIs when avaiable) useful for a LCG site
and some more for a Tier-2 of the CMS experiment, expecially in the
field of job management, dataset transfer and analysis of performance
results and availability tests. Thanks to its architecture and the
provided plugins WHALE makes easy to perform tasks that, even if
logically simple, are technically complex or tedious, like eg. closing
all the worker nodes with a job-failure rate greater than a given
threshold.

Finally, thanks to the centralization of the activities on a single
point and to its logging functionalities, WHALES acts as a
knowledge-base of the site and a handful tool to keep track of the
activities at a given site. For this reason it also provides a
tailored plugin to perform advanced searches in the activity log.


Use cases
=========

lcgwhale.py is a shell-like tool, with special features that address
typical CMS Tier-2 administrator needs.


#### getting the status (up/down) of a host
Host cmsrm-cream02 Status

#### generate a list of Hosts

Host

### filter it

Host cmsrm-cream

### get the status of a set of hosts obtained from a generator

Host cmsrm-cream | Host Status

### list of datasets at a site

PhedexNode T2_IT_Rome Dataset

### Logical Filenames in a dataset

Dataset /sdfs/sdsd#sdsdv/fg Lfn

### list of all pools

Pool

### Physical Filenames of files on pool cmsrm-st14_1

Pool cmsrm-st14_1 Pfn

### list of hosts hosting a given file

Pfn /pnfs/roma1.infn.it/data/cms/store/user/talamoig/test12829 Host

### close a host in lsf

Host cmsrm-wn123 CloseHost

### close hosts where LSF service is in critical state

Status LSF,critical Host | Host CloseHost

### close hosts where user cms014 are running

User cms014 Jobs | Jobs CloseHost

### get the output of a command on a given host

Host cmsrm-cream01,uptime SSHCommand

Host cmsrm-wn

Usage
======

From command line: lcgwhale.py --help

From python shell:
[root@cmsrm-ui02 ~]# python2.6
Python 2.6.5 (r265:79063, Feb 28 2011, 21:55:45)
[GCC 4.1.2 20080704 (Red Hat 4.1.2-50)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> from tools.lcgwhale import *
host='cmsrm-dcache' dbname='chimera' user='whale'
host='cmsrm-dcache' dbname='dcache' user='whale'
Adding <whale.plugins.wlcg.cms.transfersystem.PhEDEx.PhEDEx object at 0x17900250>
Adding <whale.plugins.storagesystem.dcache.DCache.DCache object at 0x179002d0>
Adding <whale.plugins.wlcg.cms.datacatalogue.DAS.DAS object at 0x17900590>
Adding <whale.plugins.wlcg.cms.dashboard.Dashboard.Dashboard object at 0x1790c090>
Adding <whale.plugins.batchsystem.lsf.LSF.LSF object at 0x179005d0>
Adding <whale.plugins.wlcg.GridMapDir.GridMapDir object at 0x17900790>
Adding <whale.plugins.monitor.nagios.Nagios.Nagios object at 0x17900950>
Adding <whale.plugins.monitor.nagios.Nagios.Nagios object at 0x17900b10>
Adding <whale.plugins.monitor.nagios.Nagios.Nagios object at 0x17900cd0>