'''
Created on Mar 20, 2012

@author: talamoig
'''

from whale.plugins.Plugin import Plugin

class BatchSystem(Plugin):
    '''
    This is an abstract class to be implemented by
    specific batch systems.
    '''

    done="DONE"
    pending="PENDING"
    running="RUNNING"
    suspended="SUSPENDED"
    error="ERROR"
    unknown="UNKNOWN"
    wait="WAIT"
    zombi="ZOMBI"
    cancelled="CANCELLED"
    cleared="CLEARED"
    
    def JobId2RunningNode(self,job):
        pass

    def JobId2Queue(self,job):
        pass

    def JobId2SubmissionNode(self,job):
        pass

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
