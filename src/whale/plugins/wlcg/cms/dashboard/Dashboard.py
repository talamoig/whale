'''
Created on Feb 27, 2012

@author: talamoig
'''

from time import time

from whale.plugins.batchsystem.BatchSystem import BatchSystem
from whale.utils.JsonUtils import JSonUtils

class Dashboard(BatchSystem):
    '''
    classdocs
    '''
## http://dashb-cms-job.cern.ch/dashboard/request.py/jobstatus2?user=&site=T2_IT_Rome&submissiontool=&application=&activity=production&status=aborted&check=submitted&tier=&sortby=activity&ce=&rb=&grid=&jobtype=&submissionui=&dataset=&submissiontype=&task=&subtoolver=&genactivity=&outputse=&appexitcode=&accesstype=&date1=2012-10-03+12%3A07&date2=2012-10-04+12%3A07&count=2623&offset=0&exitcode=&fail=&cat=&len=5000&prettyprint
## http://dashb-cms-job.cern.ch/dashboard/request.py/jobstatus2?user=&site=T2_IT_Rome&submissiontool=&application=&activity=production&status=terminated&check=submitted&tier=&sortby=activity&ce=&rb=&grid=&jobtype=&submissionui=&dataset=&submissiontype=&task=&subtoolver=&genactivity=&outputse=&appexitcode=&accesstype=&date1=2012-10-03+12%3A07&date2=2012-10-04+12%3A07&count=2661&offset=0&exitcode=&fail=&cat=&len=5000&prettyprint
    baseUrl="http://dashb-cms-job.cern.ch/dashboard/request.py/jobstatus2?user=&site=%s&submissiontool=&application=&activity=&status=&check=submitted&tier=&sortby=activity&ce=&rb=&grid=&jobtype=&submissionui=&dataset=&submissiontype=&task=&subtoolver=&genactivity=&outputse=&appexitcode=&accesstype=&date1=2012-10-03+12%%3A07&date2=2012-10-04+12%%3A07&count=2661&offset=0&exitcode=&fail=&cat=&len=100000"

    status={"SUCCEEDED":BatchSystem.done,"RETRIEVED":BatchSystem.done,"CLEARED":BatchSystem.cleared,"CANCELLED":BatchSystem.cancelled,"DONE":BatchSystem.done,"FAILED":BatchSystem.error}

    lastUpdate=0
    dashjobs={}
    
    def CMSSite2JobId(self,CMSSite,force=False):
        if self.lastUpdate+int(self.getItem("cachetime"))<time() or force:
            url=self.baseUrl%CMSSite
            querier=JSonUtils()
            tmp=querier.dataFromUrl(url)['jobs']
            self.dashjobs={}
            for job in tmp:
               self.dashjobs[job["jobId"]]=job
            self.lastUpdate=time()
        #    if result!=None:
        #        self.dashjobs=filter(lambda x:x['gridStatusName']==result,self.dashjobs)

        return self.dashjobs.keys()

    def JobId2User(self,job):
        pass    

    def RunningNode2JobId(self,workernode):
        pass

    def Queue2JobId(self,queue):
        pass

    def SubmissionNode2JobId(self,submissionnode):
        pass

    def User2JobId(self,user):
        pass

    def _2JobId(self):
        pass

    def _2Queue(self):
        pass
    
    def JobId2RunningNode(self,jobId):
        return self.dashjobs[jobId]['WNHostName']

    def JobId2JobStatus(self,jobId):
        return self.dashjobs[jobId]['gridStatusName']
    
    def __init__(self,configfile=None):
        self.config(configfile)
