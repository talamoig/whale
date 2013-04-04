'''
Created on Mar 20, 2012

@author: talamoig
'''

from pylsf import *
from time import ctime
from time import time
from whale.utils.Exec import Exec
from whale.plugins.batchsystem.BatchSystem import BatchSystem

class LSF(BatchSystem):
    status={192:BatchSystem.done,1:BatchSystem.pending, 4:BatchSystem.running,32:BatchSystem.zombi,2:BatchSystem.suspended, 320: BatchSystem.done, 65536: BatchSystem.unknown}
    alljobs=[]
    lastUpdate=0

    def printSummary(self,jobs=None):
        if jobs==None:
            jobs=self.jobs()
        print 'Id\tStatus\tUser\tExecHost\tFromHost\tQueue\tSubmitted\tStarted\tEnded\GridID'
        for j in jobs:
            id=j[0]
            status=self.status[j[2]]
            user=j[1]
            submittime=ctime(j[4])
            starttime="-"
            if j[6]>0:
                starttime=ctime(j[6])
            endtime="-"
            if j[8]>0:
                endtime=ctime(j[8])
            runningNode="-"
            try:
                runningNode=j[17][0][0]
            except Exception:
                None
            submissionNode=j[16]
            queue=j[19][1]
            print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s"%(id,status,user,runningNode,submissionNode,queue,submittime,starttime,endtime)

    def jobByJobId(self,JobId):
        for j in self.jobs():
            if str(j[0])==str(JobId):
                return j

    def JobId2JobKill(self,JobId,dry=False):
        ex=Exec()
        command="bkill %s"%JobId
        if dry:
            print command
        else:
            ex.osExec(command)
        return None

    def JobId2LSFJobCommand(self,JobId):
        job=self.jobByJobId(JobId)
        if job:
            return job[19][13]
        return None

    def GridJobId2JobId(self,GridJobId):
        jobs=self.jobs()
        for j in jobs:
            if j[19][13].find(GridJobId)!=-1:
                return j[0]
        return None

    
    
    def allJobs(self,force=False):
        if self.lastUpdate+int(self.getItem("cachetime"))<time() or force:
            self.alljobs=[]
            jobsize = lsb_openjobinfo()
            for jobnum in range(jobsize):
                job=lsb_readjobinfo(jobnum)
                self.alljobs.append(job)
            self.lastUpdate=time()
            if self.getItem("queuefilter"):
                self.alljobs=filter(lambda x:x[19][1].find(self.getItem("queuefilter"))!=-1,self.alljobs)
        return self.alljobs
    
    def jobs(self,User=None,RunningNode=None,SubmissionNode=None,JobStatus=None,Queue=None,JobId=None,jobs=None,invert=False,force=False):
        if jobs==None:
            jobs=self.allJobs(force)
        if RunningNode:
            tmp=[]
            for j in jobs:
                try:
                    if (j[17][0][0].find(RunningNode)!=-1) != invert:
                        tmp.append(j)
                except Exception:
                    None
            jobs=tmp
        if SubmissionNode!=None:
            jobs=filter(lambda x:(x[16].find(SubmissionNode)!=-1) != invert,jobs)
        if User!=None:
            jobs=filter(lambda x:(x[1].find(User)!=-1) != invert,jobs)
        if JobStatus!=None:            
            jobs=filter(lambda x:(self.status[x[2]] in JobStatus) != invert,jobs)
        if Queue!=None:
            jobs=filter(lambda x:(x[19][1].find(Queue)!=-1) != invert,jobs)
        if JobId!=None:
            jobs=filter(lambda x:(str(x[0])==str(JobId)) != invert,jobs)
        return jobs

    def _2JobStatus(self):
        return map(lambda x: self.status[x],set(map(lambda x: x[2],self.jobs())))

    def _2User(self):
        return set(map(lambda x: x[1],self.jobs()))

    def _2Queue(self):
        return set(map(lambda x: x[19][1],self.jobs()))

    def _2SubmissionNode(self):
        return set(map(lambda x: x[16],self.jobs()))    

    def _2RunningNode(self):
        nodes=[]
        for x in self.jobs():
            try:
                nodes.append(x[17][0][0])
            except Exception:
                None
        return set(nodes)

    def JobIdFromJob(self,Job):
        return Job[0]

    def JobId2RunningNode(self,JobId):
        job=self.jobByJobId(JobId)
        if not job:
            return None
        try:
            return job[17][0][0]
        except Exception:
            return None
     
        
    def JobId2Queue(self,JobId):
        job=self.jobByJobId(JobId)
        if not job:
            return None
        try:
            return job[19][1]
        except Exception:
            return None


    def JobId2SubmissionNode(self,JobId):
        job=self.jobByJobId(JobId)
        if not job:
            return None
        try:
            return job[16]
        except Exception:
            return None
    

    def JobId2User(self,JobId):
        job=self.jobByJobId(JobId)
        if not job:
            return None
        try:
            return job[1]
        except Exception:
            return None


    def JobId2JobStatus(self,JobId):
        job=self.jobByJobId(JobId)
        if not job:
            return None
        try:
            return self.status[job[2]]
        except Exception:
            return None

    def RunningNode2JobId(self,RunningNode):
        try:
            return [x[0] for x in self.jobs(RunningNode=RunningNode)]
        except Exception:
            return None

    def Queue2JobId(self,Queue):
        try:
            return [x[0] for x in self.jobs(Queue=Queue)]
        except Exception:
            return None

    def SubmissionNode2JobId(self,SubmissionNode):
        try:
            return [x[0] for x in self.jobs(SubmissionNode=SubmissionNode)]
        except Exception:
            return None

    def User2JobId(self,User):
        try:
            return [x[0] for x in self.jobs(User=User)]
        except Exception:
            return None

    def RunningNode2Host(self,RunningNode):
        return RunningNode

    def Host2RunningNode(self,Host):
        return Host

    def RunningNode2NodeClose(self,RunningNode):
        ex=Exec()
        command="badmin hclose %s"%RunningNode
        print command
        ex.osExec(command)
        return None

    def RunningNode2NodeOpen(self,RunningNode):
        ex=Exec()
        ex.osExec("badmin hopen %s"%RunningNode)
        return None

    def Queue2QueueClose(self,Queue):
        ex=Exec()
        ex.osExec("badmin qclose %s"%Queue)
        return None

    def Queue2QueueOpen(self,Queue):
        ex=Exec()
        ex.osExec("badmin qopen %s"%Queue)
        return None

    def _2JobId(self,**args):
        return map(lambda x:self.JobIdFromJob(x),self.jobs(**args))
        

    def __init__(self,configfile=None):
        self.config(configfile)
        if lsb_init("pylsf")==-1:
            print("Error")

