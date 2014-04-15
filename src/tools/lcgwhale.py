import cmd
import os
import traceback
from os.path import expanduser
from optparse import OptionParser
from whale.utils.Configurable import Configurable
import sys

rootconfig="/etc/whale/whale.conf"
userconfig=expanduser("~")+"/.whale/whale.conf"
configuration = None

class LcgWhale(cmd.Cmd):
    """Cmd interpreter for lcg-whale"""

    configuration=None
    more={}
    
    def do_set(self,line):
        vals=line.split()
        try:
            self.w.setGlobalInfo(vals[0],vals[1])
        except Exception:
            print traceback.format_exc()

    def do_unset(self,line):
        try:
            self.w.unsetGlobalInfo(line)
        except Exception:
            print traceback.format_exc()

    def do_env(self,line):
        provider=self.w.getGlobalInfoProvider()
        for k in provider.keys():
            print "%s=%s"%(k,provider[k])
            
    def configure(self,configuration):
        self.configuration=configuration
        self.addplugin("whale.plugins.wlcg.cms.transfersystem.PhEDEx","p")
        initscript=self.configuration.getItem("initscript")
        execfile(initscript)
        print "Available types:"
        print self.w.types()        

    def addplugin(self,modulepath,objname="",classname=""):
        if classname=='':
            classname=modulepath.split(".")[-1]
        if objname=='':
            objname=classname
        try:
            mod=__import__(modulepath, fromlist=[classname])
            exec("self.%s=mod.%s()"%(objname,classname))
            print "Created %s:%s"%(objname,classname)
        except Exception:
            print "Error creating plugin object"
        
    def do_EOF(self, line):
        print ""
        return True

    def default(self, line):
        if line in self.w.types():
            self.printCache(line)
            return
        try:
            exec(line)
        except Exception:
            print traceback.format_exc()

    def complete_c(self, text, line, begidx, endidx):        
        num=len(line.strip().split(" "))
        if num==2 and line[-1]!=" ":
            return [i for i in self.w.types() if i.lower().startswith(text.lower())]
        if num==3 or (num==2 and line[-1]==" "):
            cached=self.w.getCachedVals(line.split(" ")[1])
            return [i for i in cached if i.startswith(text)]
        return []
    
    def do_config(self,line):
        for item in configuration.getItems():
            print item
            
    def do_generate(self,line):
        try:
            print self.w.generate(line)
        except Exception:
            print "No generator found"
            
    def do_convert(self,line):
        args=line.split()
        if len(args)<2:
            print "convert requires at least 2 arguments"
            return
        try:
            if len(args)==2:
                res=self.w.convert3(args[0],args[1],value=None,more=self.more)
            if len(args)==3:
                vals=args[2].split(",")
                res=self.w.convert3(args[0],args[1],vals,more=self.more)
            if len(args)>3:
                converter=[]
                for i in range(0,len(args)-2):
                    converter+=self.w.findConverter(args[i],args[i+1])
                res=self.w.convert3(args[0],args[-2],args[-1],converters=converter)
            print res
        except Exception as e:
            print traceback.format_exc()

    def emptyline(self):
        pass

    def do_last(self,s):
        try:
            print self.w.last
        except Exception:
            print traceback.format_exc()

    def do_shell(self, s):
        os.system(s)

    def help_shell(self):
        print "execute shell commands"

    def complete_set(self, text, line, begidx, endidx):
        num=len(line.strip().split(" "))
        if  num<2 or (num==2 and line[-1]!=" "):
            return [i for i in self.w.types() if i.lower().startswith(text.lower())]
        cached=self.w.getCachedVals(line.split(" ")[1])
        return [i for i in cached if i.startswith(text)]
    
    def complete_generate(self, text, line, begidx, endidx):
        return self.complete_convert(text,line,begidx,endidx)
    
    def complete_convert(self, text, line, begidx, endidx):
        num=len(line.strip().split(" "))
        if  num<3 or (num==3 and line[-1]!=" "):
            return [i for i in self.w.types() if i.lower().startswith(text.lower())]
        cached=self.w.getCachedVals(line.split(" ")[1])
        return [i for i in cached if i.startswith(text)]

    def printCached(self,key=None):
        if key==None:
            print self.w.cacheVals
        else:
            print self.w.getCachedVals(key)
    
    def do_c(self,s):
        args=s.split()
##        print args
        if len(args)==1:
            self.printCached(s)
        if len(args)==2:
            cache=self.w.getCachedVals(args[0])
            sub=[x for x in cache if x.startswith(args[1])]
            print sub
            


def readConfig(configfile):
    global configuration
    try:
        open(configfile,"r")    
    except Exception:
        print("Cannot read configuration file:%s"%configfile)
        sys.exit(1)
    try: 
        configuration=Configurable(configfile,"WHALE")
    except Exception:
        print("WHALE section not found in configfile %s"%configfile)
        sys.exit(1)


def main():
    if os.geteuid() != 0:
        defaultconfig=userconfig
    else:
        defaultconfig=rootconfig
    parser = OptionParser()
    parser.add_option("-r","--run", dest="commands",
                      help="commands to run")
    parser.add_option("-c","--config", dest="configfile",
                      help="read configuration from FILE instead of default", metavar="FILE",
                      default=defaultconfig)
    parser.add_option("-f","--format", dest="format",
                      help="not implemented yet")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="set logging mode to verbose")
    (options, args) = parser.parse_args()
    readConfig(options.configfile)
    whale=LcgWhale()
    whale.configure(configuration)    
    whale.cmdloop()

if __name__ == "__main__":
    main()
