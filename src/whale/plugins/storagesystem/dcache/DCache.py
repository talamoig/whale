'''
Created on Jan 30, 2012

@author: talamoig
'''
from whale.plugins.Plugin import Plugin
from whale.utils.Exec import Exec
from whale.utils.PGSQLConnector import PGSQLConnector
from whale.utils.DCache import AdminDoor

## http://trac.dcache.org/wiki/How-tos/TranslatePathnamesIntoPNFS-IDs

class DCache(Plugin):
    
    def Pnfsid2Adler(self,pnfsid):
        try:
            adler32,=self.__chimeraQuery(table="t_inodes_checksum",fields=["isum"],append="where ipnfsid='%s' and itype=1"%pnfsid)[0]
            return [adler32]
        except:    
            return []
    
    def adminCommand(self,cmd_list):
        return self.__adminDoor.exec_cmd(cmd_list)

    def DN2User(self,DN,FQAN=""):
        res=self.adminCommand(["cd gPlazma",'get mapping "%s" "%s"'%(DN,FQAN)])
        try:
            res=res[2]            
            mapindex=res.find("mapped as: ")
            if mapindex==-1:                
                return None
            return res[mapindex+11:].split()[0]
        except Exception:
            return None

    def PoolInfo(self,Pool,Info=None):
        res=self.adminCommand(["cd %s"%Pool,"info"])
        if Info==None:
            return "\n".join(res)
        ret=filter(lambda x: x.find(Info)!=-1,res)
        try:
            return ret[0].split(":")[1].split()[0]
        except Exception:
            return ret
        
    def Pool2FreeSpace(self,Pool):
        return self.PoolInfo(Pool,"Free")
    
    def Pool2UsedSpace(self,Pool):
        return self.PoolInfo(Pool,"Used")

    def Pool2TotalSpace(self,Pool):
        free=int(self.PoolInfo(Pool,"Free"))
        used=int(self.PoolInfo(Pool,"Used"))
        return str(free+used)

    def setPoolReadOnly(self,pool):
        return self.__setPoolAccess(pool,"rdonly")

    def setPoolReadWrite(self,pool):
        return self.__setPoolAccess(pool,"notrdonly")

    def isOrphan(self,Pnfsid):
        return len(self.Pnfsid2Pool(Pnfsid))==0
    
    def migratePool(self,source,targetPools):
        pools=" ".join(targetPools)
        cmds=["cd %s"%source,"migration move -state=precious %s"%pools]
        return self.adminCommand(cmds)

    def RemovePool(self,pool):
        self.adminCommand(["cd PoolManager","psu remove pool %s"%pool, "save"])
        
    def Migration2Pnfsid(self,migration):
        (pool,id)=migration.split(":")
        info=self.adminCommand(["cd %s"%pool,"migration info %s"%id])[2:]
        pnfsids=[]
        index=0
        for line in info:
            if line.startswith("Running tasks:"):
                break
            index+=1
        for line in info[index+1:]:
            if line.startswith("Most recent errors"):
                break
            ## expecting a line like:
            ## '[6378] 0000AF5C148DC7FC494CBA6F4136CEB59AC0: TASK.Copying -> [cmsrm-st09_3@local]'
            pnfsids.append(line.split()[1][:-1])
        return pnfsids
            
    
    def _2Migration(self):
        return sum([self.Pool2Migration(pool) for pool in self._2Pools()],[])
    
    def MigrationInfo(self,migration):
        (pool,id)=migration.split(":")
        return "\n".join(self.adminCommand(["cd %s"%pool,"migration info %s"%id])[2:])
    
    def enablePool(self,pool):
        self.adminCommand(["cd %s"%pool,"pool enable"])
    
    def disablePool(self,pool):
        self.adminCommand(["cd %s"%pool,"pool disable"])
    
    def MigrationStatus(self,migration):
        (pool,id)=migration.split(":")
        info=self.adminCommand(["cd %s"%pool,"migration info %s"%id])[2:]
        status=info[1].split(":")[1].strip()
        percent="-"
        for f in info:
            if f.startswith("Completed"):
                percent=f.split(";")[-1].strip()
        return "%s(%s)"%(status,percent)
    
    
    def Pool2Migration(self,pool):
        cmds=["cd %s"%pool,"migration ls"]
        running=[]
        for m in self.adminCommand(cmds)[2:]:
##            if m.find("RUNNING")!=-1 or m.find("SLEEPING")!=-1:
              running.append("%s:%s"%(pool,m[m.find("[")+1:m.find("]")]))
        return running
    
    def __setPoolAccess(self,pool,mode):
        cmd_list=['cd PoolManager','psu set pool %s %s'%(pool,mode)]
        self.adminCommand(cmd_list)
    
#    def User2Transfer(self,user):
#        query="select putfilerequests.parentfileid from putfilerequests,putrequests,srmrequestcredentials where putrequests.id=putfilerequests.requestid and srmrequestcredentials.id=putfilerequests.credentialid and srmrequestcredentials.credentialname like '%%%s%%' order by putrequests.creationtime desc limit 100"%user
#        #print query
#        return self.__basicQuery(self.__dcachedb,query)
    
    def Pnfsid2MD5(self,pnfsid):
        try:
            md5,=self.__chimeraQuery(table="t_inodes_checksum",fields=["isum"],append="where ipnfsid='%s' and itype=2"%pnfsid)[0]
            return [md5]
        except:
            return []


    def Pnfsid2Size(self,pnfsid):
        try:
            size,=self.__chimeraQuery(table="t_inodes",fields=["isize"],append="where ipnfsid='%s'"%pnfsid)[0]
            return [size]
        except:
            return []            

    def _2Pnfsid(self,pnfsid=None):
        wherepart=""
        if pnfsid!=None:
            wherepart=" and ipnfsid='%s'"%pnfsid
        return self.__chimeraQuery(table="t_inodes",fields=["ipnfsid"],append="where itype=32768%s"%wherepart)

    def Transfers(self):
        pass
        
    def _2Pool(self):
        pools=self.adminCommand(["cd PoolManager", "psu ls pool"])[2:]
        return pools
        
    def Host2Pool(self,host):
        pools=self._2Pool()
        pools = filter(lambda(x): x.find(host+'_')!=-1 ,  pools)        
        return pools
      
    def Pool2Host(self,pool):
        return [pool.split("_")[0]]
                
    def Pool2Pfn(self,pool):
        pnfsids=self.Pool2Pnfsid(pool)
        return map(self.Pnfsid2Pfn,pnfsids)
    
    def Pool2Pnfsid(self,pool):
        return [k for (k,) in self.__chimeraQuery(table="t_locationinfo",fields=["ipnfsid"],append="where ilocation='%s'"%pool)]
    ##return self.__query(table="t_locationinfo",fields=["ipnfsid"],append="where ilocation='%s'"%pool)
    
    def Pnfsid2Pool(self,pnfsid):
        return [k for (k,) in self.__chimeraQuery(table="t_locationinfo",fields=["ilocation"],append="where ipnfsid='%s'"%pnfsid)]
    
    __chimeraRoot="000000000000000000000000000000000000"
    
    def Pfn2Pool(self,pfn):
        return self.Pnfsid2Pool(self.Pfn2Pnfsid(pfn))

    def Pfn2User(self,pfn):
        return

    def Pfn2Group(self,pfn):
        return
    
    def Pfn2Pnfsid(self,pfn):
        return self.__chimeraBasicQuery("VALUES (path2inode('%s', '%s'))"%(self.__chimeraRoot,pfn[1:]))[0][0]
        
    def Pnfsid2Pfn(self,pnfsid):
        return self.__chimeraBasicQuery("VALUES(inode2path('%s'))"%pnfsid)[0][0]
    
    def __basicQuery(self,db,query):
        return db.runquery(query)
    
    def Pool(self):
        pass
    
    def __chimeraBasicQuery(self,query):
        if self.verbose():
            print "query%s"%query
        return self.__basicQuery(self.__chimeradb,query)
    
    def __chimeraQuery(self,table,fields,append=""):
        query="select "+",".join(fields)+" from %s "%table+append
        return self.__chimeraBasicQuery(query)
        
    def __init__(self,configfile):
        self.config(configfile)
        self.__chimeradb=PGSQLConnector(self.getItem("dbhost"),self.getItem("dbuser"),None,"chimera")
        self.__dcachedb=PGSQLConnector(self.getItem("dbhost"),self.getItem("dbuser"),None,"dcache")  
        self.__adminDoor=AdminDoor(host=self.getItem("adminhost"))
        ##  self.billingdb=PGSQLConnector(self.getItem("dbhost"),self.getItem("dbuser"),None,"billing")
      
##        self.AdminDoor=AdminDoor(host=self.getItem("adminhost"))
