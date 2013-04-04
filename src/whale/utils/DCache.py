'''
Created on Jan 30, 2012

@author: talamoig
'''

import sys
import subprocess
import select

class AdminDoorError(Exception):
    '''
    classdocs
    '''
    def __init__(self, value):
                self.value = value
    def __str__(self):
                return repr(self.value)
        

class AdminDoor(object):
    '''
    classdocs
    ''' 
    
    def __init__(self,host='localhost',port='22223',cypher='blowfish', servKey='/opt/d-cache/config/server_key', login='admin'):
        self.__serverKey=servKey
        self.__port=port
        self.__cypher=cypher
        self.__login=login
        self.__host=host
    
    def adminCommand(self,domain,commands):
        cmds=["cd %s"%domain]+commands
                    
                
    def exec_cmd(self,cmd_list):
        """Takes a list of commands to pass to the adminDoor of dCache. logoff instruction is not mandatory.
        """
        idx=0
        cmds = '\n'.join(cmd_list)
        # Append '\n..\nlogoff' to the commands if necessary
        if not cmds.endswith('\n..\nlogoff\n'):
            cmds += '\n..\nlogoff\n'
        
        sshcmd = ['/usr/bin/ssh','-q','-T','-p',self.__port,'-c',self.__cypher,'-l',self.__login,self.__host]
        print " ".join(sshcmd)
        sshproc=subprocess.Popen(sshcmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=None)
        sshproc.stdin.write(cmds)
        ##ret=sshproc.communicate(cmds)
        retlines=[]
        while True:
            rfds, _, _ = select.select( [sshproc.stdout], [], [], 5)
            if rfds==[]:
                break
            line=sshproc.stdout.readline()
            if line=='':
                break
            retlines.append(line.strip("\r").strip("\n"))
        try:
            if retlines[6].startswith("No Route to cell for packet"):
                return []
        except Exception:
            None    
        return retlines[4:-4]
        
##        (output,ret) = sshproc.communicate(cmds)
##        return output.split("\n\r")[4:-4]
        

        
