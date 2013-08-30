whale
===

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