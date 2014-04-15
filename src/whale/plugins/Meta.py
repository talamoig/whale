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
    The most important method is convert.
    convert is capable of chaining conversion method of different plugins to realize complex conversions.
    The result of a convert("sourceType","targetType","sourceElementList")
    is a list of elements of target type.
    Furthermore, after a conversion, the variable last contains all the steps of the conversion and can be used
    to obtain details about it.    
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.reflection=ReflectionHelper()
        self.params={}
        self.loggers=[]
        self.last=None
        self.reduction=None
        self.converters={}
        self.priority=True
        self.setGlobalInfoProvider({})
        self.cacheVals={}

    def addToCacheVals(self,val,kind):
        if not self.cacheVals.has_key(kind):
            self.cacheVals[kind]=[]
        self.cacheVals[kind].append(val)
        self.cacheVals[kind]=list(set(self.cacheVals[kind]))

    def getCachedVals(self,kind):
        if not self.cacheVals.has_key(kind):
            return []
        return self.cacheVals[kind]
        
    def priority(self,val):
        self.priority=val

    def usePriority(self):
        return self.priority
        
    def addLogger(self,whaleLogger):
        self.loggers.append(whaleLogger)

    def log(self,message):
        for l in self.loggers:
            l.log(message)

    def addPlugin(self,obj):
        try:
##            print "Adding %s"%obj.getName()
            self.reflection.addObj(obj)
            obj.setGlobalInfoProvider(self.infoProvider)
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
        return list(set([self.source(conv) for conv in self._converters()]+[self.target(conv) for conv in self._converters()]))                        

    def getGraph(self):
        dg=digraph()
        for t in self.types(): dg.add_node(t)
        for c in self._converters():
            classname=c[0].__class__.__name__
            source=self.source(c)
            target=self.target(c)
            if not dg.has_edge((source,target)):
                dg.add_edge((source,target))
            dg.add_edge_attribute((source,target),("conv",c))
        return dg    

    def resetConverter(self,source,target):
        converterName="%s2%s"%(source,target)
        if converterName in self.converters: self.converters.pop(converterName)
    
    def findConverter(self,source,target,store=False):
        ## return a converter from source to target
        ## if more than a path is possible interacts
        ## with the user to pick up one.
        converterName="%s2%s"%(source,target)
        if store and converterName in self.converters:
            return self.converters[converterName]
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
        for ind,c in enumerate(convs):
            if type(c)==list:
                index=-1
                if self.usePriority():
                    c=sorted(c, key = lambda x : x[0].getPriority())
                    c=[x for x in c if x[0].getPriority()==c[0][0].getPriority()]
                    if len(c)==1:
                        convs[ind]=c[0]
                        continue                    
                print("More than one converter found. Choose one between the following:")
                for i in range(1,len(c)+1):
                    print "%s) %s"%(i,self.singleConverterRep(c[i-1]))
                while index<0 or index>len(c)-1:
                    index=int(raw_input("Index: "))-1
                convs[ind]=c[index]
#                print convs[i]
        if store:
            self.converters[converterName]=convs
        return convs

    def singleConvert(self,converter,value=None,more=None):
        (obj,method)=converter
        params=inspect.getargspec(getattr(obj,method))[0]
        all={}
        for p in params:
            if more.has_key(p):
                all[p]=more[p]
        if value:
            all[params[1]]=value
        return getattr(obj,method)(**all)
        
            
    def flatten(self,x):
        if isinstance(x, collections.Iterable) and not isinstance(x,str) and not isinstance(x,unicode):
            return [a for i in x for a in self.flatten(i)]
        else:
            return [x]

    def setDefault(self,value,param):
        self.params.update({value:param})

    def g(self,target,filter=None,args={},generator=None):
        return self.generate(target,filter,args,generator)

    def generate(self,target,like=None,args={},generator=None):
        generators=[]
        if not generator:
            for g in self._generators():
                if target==self.target(g):
                    generators.append(g)
            if len(generators)==0:
                raise MetaException("No generator found for %s"%target)
            if len(generators)==1:
                generator=generators[0]
                print generators
            if len(generators)>1:
                index=-1
                if self.usePriority():
                    generators=sorted(generators, key = lambda x : x[0].getPriority())
                    generators=[x for x in generators if x[0].getPriority()==generators[0][0].getPriority()]
                    if len(generators)==1:
                        index=0
                    else:
                        print("More than one generator found. Choose one between the following:")
                        for i in range(1,len(generators)+1):
                            print "%s) %s"%(i,self.singleConverterRep(generators[i-1]))
                        while index<0 or index>len(generators)-1:
                            index=int(raw_input("Index: "))-1
                generator=generators[index]
        (obj,method)=generator
        res=getattr(obj,method)(**args)
        for val in res:
            self.addToCacheVals(val,target)
        if like!=None:
            return filter(lambda x:x.find(like)!=-1,res)
        return res

    def c(self,source,target,value=None,more={},converters=None,duplicates=False):
        return self.convert(source,target,value,more,converters,duplicates)

    def countedlist(self,alist):
        '''Given a list returns a list of couples (elem, count) where
        elem are elements of alist without duplicated and count is the
        number of occurences of elem in alist'''
        noduplicates=list(set(alist))
        return [(x,alist.count(x)) for x in noduplicates]
        
    def convert3(self,source,target,value=None,more={},converters=None):
        ## if converter is not provided we have to build it
        if not converters:
            converters=self.findConverter(source,target,True)
        ## and if none is available we fail
        if not converters:
            raise MetaException("Converter from %s to %s not found"%(source,target))
        ## we now have to build the "more" variable
        ## and we fill it with user-defined variables
        more=dict(self.getGlobalInfoProvider().items()+more.items())
        ## after we will add values coming from intermediate steps

        ## we now have to find out the first value (or list of values)
        ## if no value is present BUT a good key is present we use it
        if value==None and more.has_key(source):
            value=more[source]

        ## and make sure it is a list
        if type(value)!=list:
            value=[value]

        ## and compress/convert to what we need (see countedlist doc fore more info)
        value=self.countedlist(value)
        self.last=[]
        ## the magic begins...
        ## for each conversion step        
        addinfo={}
        for converter in converters:
            dic={}
            self.last.append(dic)
            tmp=[]
            ## for every element to be converted
            for (val,count) in value:
                self.addToCacheVals(val,self.source(converter))
                ## do the single conversion
                res=self.singleConvert(converter,val,more)
                if (type(res))==list:
                    res.sort()
                dic[val]=res
                ## and accumulate stuff in the tmp variable
                tmp.append(res)
            tmp=self.flatten(tmp)
            for t in tmp:
                self.addToCacheVals(t,self.target(converter))
            ## we prepare values for the next step
            value=self.countedlist(tmp)
        try:
            return sum([int(x) for x in self.last[-1].values()])
        except Exception:
            pass
        return list(set(self.flatten(self.last[-1].values())))
            
    
    def convert2(self,source,target,values=None,more={},converters=None):
        ## "last" variable
        ## to contain all the conversion steps
        self.last=[]
        if not converters:
            converters=self.findConverter(source,target,True)
        if not converters:
            raise MetaException("Converter from %s to %s not found"%(source,target))
        if type(values)!=list:
            values=[values]
        values=self.countedlist(values)

        for converter in converters:
            if type(converter)==list:
                raise MetaException("Malformed list of converters found:%s"%converter)

        prev=None
        for converter in converters:
            singlevals=list(set([val for (val,count) in values]))
            dic={}
            for val in singlevals:
                dic[val]=self.singleConvert(converter,val,more)
            self.last.append(dic)
                    
    def convert(self,source,target,value=None,more={},converters=None):
        ## "last" variable
        ## to contain all the conversion steps
        self.last=[]
        if not converters:
            converters=self.findConverter(source,target,True)
        if not converters:
            raise MetaException("Converter from %s to %s not found"%(source,target))
        more=dict(self.getGlobalInfoProvider().items()+more.items())
        if value==None and more.has_key(source):
            value=more[source]
        if type(value)!=list:
            value=[value]
        value=self.countedlist(value)
        
        for converter in converters:
            if type(converter)==list:
                raise MetaException("Malformed list of converters found:%s"%converter)
            
        ## here the magic begins...
        for converter in converters:
            ## dictionary to be used in self.last to contain a conversion step
            dic={}
            self.last.append(dic)
            tmp=[]
            for (val,count) in value:
                res=self.singleConvert(converter,val,more)
                dic[val]=res
                tmp.append(res)
            ## we ensure tmp to be a list for the next step
            tmp=self.flatten(tmp)
#            value=tmp
            value=self.countedlist(tmp)
##            value=list(set(tmp))
        valstr=str(val)
        self.reduct={}
        midval=None
        midkey=None
        
        logmessage="convert(%s,%s)=%s"%(source,target,str(value)[:30])
        self.log(logmessage)
        return list(set(self.flatten(self.last[-1].values())))
##        return list(set(self.flatten(self.last[-1].values())))
        
    def canConvert(self,converter,source=None,target=None):
        if source==None and target==None:
            return True
        if target==None:
            return self.source(converter)==source
        if source==None:
            return self.target(converter)==target
        return self.target(converter)==target and self.source(converter)==source

    def _generators(self, target=None):
        return [(obj,method) for (obj,method) in self.reflection.publicMethods() if len(method.split("2"))==2 and self.source((obj,method))=='_' and (target==None or self.target((obj,method))==target)]
            
    def _converters(self,source=None,target=None):
        return [(obj,method) for (obj,method) in self.reflection.publicMethods() if len(method.split("2"))==2 and self.source((obj,method))!='_' and (source==None or self.source((obj,method)) == source) and (target==None or self.target((obj,method)) == target)]
    
    def sources(self):
        return [(obj,method) for (obj,method) in self.reflection.publicMethods() if method.find("_2")==0 ]

    def getSources(self):
        sources=self.sources()
        vals=list(set([b.split("2")[1] for (a,b) in sources]))
        ret={}
        for v in vals:
            ret[v]=[ a.getName() for (a,b) in filter(lambda (x,y): v==y.split("2")[1], sources)]
        return ret

    def __plugins(self):
        return self.reflection.objList()

    def plugin(self,pluginName=""):
        '''
        This is a utility method to inspect plugins.
        It accepts a string to match the plugins name.
        If more than one match is obtained the list of all the plugins is printed.
        If only one plugin is matched it prints the name and the list of its generators and converters.
        '''
        plugins=self.__plugins()
        ## we first get the list of matching
        plugin=filter(lambda x:x.getName().lower().find(pluginName.lower())!=-1,plugins)
        exact=filter(lambda x:x.getName()==pluginName,plugins)
        ## but if there's an exact match (case sensitive) we give it precedence
        if len(exact)==1:
            plugin=exact
        if len(plugin)>1:
            print ", ".join([x.getName() for x in plugin])
            return
        if len(plugin)==0:
            print("No occurence found")
            return
        plugin=plugin[0]
        generators=[method for (obj,method) in self._generators() if obj==plugin]
        converters=[method for (obj,method) in self._converters() if obj==plugin]
        print plugin.getName()
        if len(generators)>0:
            for g in generators:
                print "*"+g.split("2")[1]
        if len(converters)>0:
            for c in converters:
                print "->".join(c.split("2"))

    def p(self,pluginName=""):
        return self.plugin(pluginName)

    def generators(self,target=None):
        generators=list(set([method.split("2")[1] for (obj,method) in self._generators(target)]))
        for g in generators:
            all=self._generators(g)
            print g+":"+", ".join([obj.getName() for (obj,method) in all])

    def converters(self,source=None,target=None):
        converters=list(set([method for (obj,method) in self._converters(source=source,target=target)]))
        for c in converters:
            all=self._converters(c.split("2")[0],c.split("2")[1])
            print "->".join(c.split("2"))+": "+", ".join([obj.getName() for (obj,method) in all])
    
    def singleConverterRep(self,conv):
        (obj,method)=conv
        ret=""
        if method.split("2")[0]=="_":
            ret="*"+method.split("2")[1]
        else:
            ret="->".join(method.split("2"))
        ret+="@"+obj.getName()
        return ret
        
    def printConverter(self,converter):
        print "->".join([self.singleConverterRep(c) for c in converter])

    def getDotGraph(self):
        g=Graph()
        for t in self.types():
            g.add_node(Node(t))
        for conv in self._converters():
            source=self.source(conv)
            target=self.target(conv)
            g.add_edge(Edge(source,target,label=conv[0].__class__.__name__))
        return g.to_string()
    
