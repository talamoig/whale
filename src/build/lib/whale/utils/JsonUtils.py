'''
Created on Feb 24, 2012

@author: talamoig
'''

import json
import urllib2

class JSonUtils(object):
    '''
    This class is a collection of methods for easily accessing json data
    '''

    def __init__(self):
        '''
        Constructor
        '''   
        
    def dataFromUrl(self, url, data=None):
        '''
        Retrieve json data from @url and @returns the python object obtained from it.
        It can handle both single and double-quotes json content.
        '''
        req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()
        try:
            return json.loads(response)
        except Exception:
            None
        try:
            return json.loads(json.dumps(eval(response)))
        except Exception:
            return None
