#WHALE

## Quickstart installation
To install:

    git clone https://github.com/talamoig/whale
    cd whale
    sudo python src/setup.py install

And then on a python prompt:
    
    from whale.plugins.wlcg.cms.transfersystem.PhEDEx import PhEDEx
    phedex=PhEDEx()
    phedex.setDB("prod")
    phedex._2PhedexNode()
    #[u'T2_PK_NCP', u'T3_US_FIT', u'T3_US_UCD', u'T3_MX_Cinvestav', ...

You can get the IDs of all the not approved transfers at a site:

    phedex.PhedexNode2TransferRequest("T2_IT_Rome",approved=False)
    #['24352', '394170', '64500', '157225', '367808', '310606', ...

And know the dataset they corresponds. For the first, for example:
    phedex.TransferRequest2Dataset('24352')
    #[u'/CSA07Electron/CMSSW_1_6_7-CSA07-Chowder-I1-PDElectron-Skim ...

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