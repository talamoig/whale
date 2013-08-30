'''
Created on Feb 20, 2012

@author: talamoig
'''


class ReflectionHelper(object):
    '''
    Utility class that helps digging into reflection
    '''
    

    def __init__(self):
        '''
        Constructor
        '''
        self.objs=set()
        
    def addObj(self,obj):
        self.objs.add(obj)

    def remObj(self,obj):
        self.objs.remove(obj)

    def objList(self):
        return self.objs
    
    def publicMethods(self):
        methods=[]
        for c in self.objs:
            methodList = [(c,method) for method in dir(c) if (callable(getattr(c, method)) and not method.startswith("__"))]
            methods+=methodList
        return methods
        
## see http://www.diveintopython.net/power_of_introspection/index.html
    def info(self,obj, spacing=10, collapse=1):
        methodList = [method for method in dir(obj) if callable(getattr(obj, method))]
        processFunc = collapse and (lambda s: " ".join(s.split())) or (lambda s: s)
        print "\n".join(["%s %s" %
                         (method.ljust(spacing),
                          processFunc(str(getattr(obj, method).__doc__)))
                         for method in methodList])
