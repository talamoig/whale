whale
=====

Introduction
===
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
===

From command line: lcgwhale.py