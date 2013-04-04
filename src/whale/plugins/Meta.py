from whale.utils.ReflectionHelper import ReflectionHelper 
from whale.plugins.Plugin import Plugin
from whale.plugins.logger.WhaleLogger import WhaleLogger

'''
Created on Feb 27, 2012

@author: talamoig
'''
'''
Created on Feb 20, 2012

@author: talamoig
'''

import inspect
import collections
from pydot import *
from copy import deepcopy
from pygraph.classes.digraph import digraph
from pygraph.algorithms.minmax import shortest_path

class MetaException(Exception):
    def __init__(self,msg):
        self.msg=msg
        
    def __str__(self):
        return repr(self.msg)


class Meta(Plugin):
    '''
    This class provides a way to easily and transparently connect converters and generators
    of different plugins.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.reflection=ReflectionHelper()
        self.params={}
        self.loggers=[]
        self.lastConversion=None
        self.reduction=None

    def addLogger(self,whaleLogger):
        self.loggers.append(whaleLogger)

    def log(self,message):
        for l in self.loggers:
            l.log(message)
        
    def addPlugin(self,obj):
        try:
            print "Adding %s"%obj
            self.reflection.addObj(obj)
        except e:
            None

    def removePlugin(self,obj):
        self.reflection.remObj(obj)
            
    def source(self,converter):
        (obj,method)=converter
        return method.split("2")[0]    

    def target(self,converter):
        (obj,method)=converter
        return method.split("2")[1]    
        
    def types(self):
        return list(set([self.source(conv) for conv in self.converters()]+[self.target(conv) for conv in self.converters()]))                        

    def getGraph(self):
        dg=digraph()
        for t in self.types(): dg.add_node(t)
        for c in self.converters():
            classname=c[0].__class__.__name__
            source=self.source(c)
            target=self.target(c)
            if not dg.has_edge((source,target)):
                dg.add_edge((source,target))
            dg.add_edge_attribute((source,target),("conv",c))
        return dg
    
    def findConverter(self,source,target):
        graph=self.getGraph()
        (map,_)=shortest_path(graph,source)
        convs=[]
        curr=target
        while curr!=source:
            if not map[curr]: return None
            edges=graph.edge_attributes((map[curr],curr))
            if len(edges)==1:
                convs.append(edges[0][1])
            else:
                tmp=[]
                for e in edges:
                    tmp.append(e[1])
                convs.append(tmp)
            curr=map[curr]
        convs.reverse()
        return convs
                     
    def _findConverter(self,source,target,maxdepth=1):
        for c in self.converters():
            if self.canConvert(c,source,target):
                return [c]
        if maxdepth==1:
            return None
        for c in self.converters():
            m1=self._findConverter(source,self.target(c),1)
            m2=self._findConverter(self.target(c),target,maxdepth-1)
            if m1 and m2:
                return m1+m2
        return None

    def singleConvert(self,converter,value=None,more=None):
        (obj,method)=converter
        params=inspect.getargspec(getattr(obj,method))[0]
        all={}
        all.update(self.params)
        if more:
            all.update(more)
        if value:
            all[params[1]]=value
        for k in all.keys():
            if not k in params:
                del all[k]

        return getattr(obj,method)(**all)
            
    def flatten(self,x):
        if isinstance(x, collections.Iterable) and not isinstance(x,str) and not isinstance(x,unicode):
            return [a for i in x for a in self.flatten(i)]
        else:
            return [x]


    def setDefault(self,value,param):
        self.params.update({value:param})

    def generate(self,target,args={},generator=None):
        generators=[]
        if not generator:
            for g in self.generators():
                if target==self.target(g):
                    generators.append(g)
            if len(generators)==0:
                raise MetaException("No generator found for %s"%target)
            if len(generators)==1:
                generator=generators[0]
            if len(generators)>1:
                index=-1                
                print("More than one generator found. Choose one between the following:")
                for i in range(1,len(generators)+1):
                    print "%s) %s"%(i,self.singleConverterRep(generators[i-1]))
                while index<0 or index>len(generators)-1:
                    index=int(raw_input("Index: "))-1
                generator=generators[index]
        (obj,method)=generator
        return getattr(obj,method)(**args)
 
    def convert(self,source,target,value=None,more={},converters=None,duplicates=False):
        self.lastConversion=[]
        if not converters:
            converters=self.findConverter(source,target)
        if not converters:
            raise MetaException("Converter from %s to %s not found"%(source,target))
        if type(value)!=list:
            value=[value]
        vals=value
        for converter in converters:
            if type(converter)==list:
                index=-1                
                print("More than one converter found. Choose one between the following:")
                for i in range(1,len(converter)+1):
                    print "%s) %s"%(i,self.singleConverterRep(converter[i-1]))
                while index<0 or index>len(converter)-1:
                    index=int(raw_input("Index: "))-1
                converter=converter[index]
            dic={}
            self.lastConversion.append(dic)
            tmp=[]
            for val in value:
                res=self.singleConvert(converter,val,more)
                dic[val]=res
                tmp.append(res)
            tmp=self.flatten(tmp)
            value=tmp
            if not duplicates:
                value=list(set(tmp))
##        self.lastConversion.append(value)
        valstr=str(val)
        self.reduct={}
        midval=None
        midkey=None
        if vals!=None:
            for k in vals:
                midval=k
                for x in range(len(self.lastConversion)):
                    midval=self.lastConversion[x][midval]
                self.reduct[k]=midval
            self.inv_map = {}
            for k, v in self.reduct.iteritems():
                self.inv_map[str(v)] = self.inv_map.get(str(v), [])
                self.inv_map[str(v)].append(k)
            self.reduct=self.inv_map
        
        logmessage="convert(%s,%s)=%s"%(source,target,str(value)[:30])
        self.log(logmessage)
        return value
        
    def canConvert(self,converter,source=None,target=None):
        if source==None and target==None:
            return True
        if target==None:
            return self.source(converter)==source
        if source==None:
            return self.target(converter)==target
        return self.target(converter)==target and self.source(converter)==source

    def generators(self):
        return [(obj,method) for (obj,method) in self.reflection.publicMethods() if len(method.split("2"))==2 and self.source((obj,method))=='_' ]
            
    def converters(self):
        return [(obj,method) for (obj,method) in self.reflection.publicMethods() if len(method.split("2"))==2 and self.source((obj,method))!='_' ]
    
    def sources(self):
        return [(obj,method) for (obj,method) in self.reflection.publicMethods() if method.find("_2")==0 ]
    
    def singleConverterRep(self,conv):
        (obj,method)=conv
        return "%s.%s"%(obj.getDescription() or obj.__class__.__name__,method)
        
    def printConverter(self,converter):
        print "->".join([self.singleConverterRep(c) for c in converter])

    def getDotGraph(self):
        g=Graph()
        for t in self.types():
            g.add_node(Node(t))
        for conv in self.converters():
            source=self.source(conv)
            target=self.target(conv)
            g.add_edge(Edge(source,target,label=conv[0].__class__.__name__))
        return g.to_string()
    
