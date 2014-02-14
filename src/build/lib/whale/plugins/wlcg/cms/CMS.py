'''
Created on Mar 20, 2012

@author: talamoig
'''

import re
from whale.plugins.Plugin import Plugin

class CMS(Plugin):
    ''' This class collects various utilities
    for the CMS experiment.
    '''
    EDGJobIdMatch='.*EDG_WL_JOBID="([^"]*)".*'

    def __init__(self,configfile=None):
        self.config(configfile)
        
    def LSFJobCommand2GridJobId(self,LSFJobCommand):
        ''' Extracts the GridJobId from the command of
        an LSF job'''
        c=re.compile(self.EDGJobIdMatch)
        m=c.match(LSFJobCommand)
        if m:
            return m.group(1)
        return None
