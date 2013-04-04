'''

@author: talamoig
'''
import subprocess
import select

class Exec(object):

##   def osExec(self,command,timeout=None):
##       child = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, cwd="/")
##       out=child.communicate()[0]
##       ret=child.returncode
##       return (ret,out.split("\n"))

    def osExec(self,command,timeout=None):
        retlines=[]
        child = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, cwd="/")
        if timeout:
            while True:
                rfds, _, _ = select.select( [child.stdout], [], [], timeout)
                if rfds==[]:
                    break
                line=child.stdout.readline()
                if line=='':
                    break
                retlines.append(line.strip("\r").strip("\n"))
            child.kill()
            return retlines
        else:
            return child.communicate()[0].split("\n")
            
            
    
    