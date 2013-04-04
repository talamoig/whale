'''
Created on Mar 20, 2012

@author: talamoig
'''

class StorageSystem(object):
    '''
    This abstract class describes a generic distributed storage system.
    By distributed we mean that file are spread over different "containers", called
    "storage pools". A storage pool is associated to a server, but a server
    can have many storage pools.
    '''

    def Pfn2StoragePool(self):
        pass
    
    def StoragePool2Pfn(self):
        pass
    
    def StoragePool2Host(self):
        pass
    
    def Host2StoragePool(self):
        pass
    

    def __init__(self):
        '''
        Constructor
        '''
        