from tools.lcgwhale import *
import sys

def main(host):
    puppetclass=w.convert("Host","PuppetClass",host)[0]
    if puppetclass==None:
        puppetclass="default"
    print "----"
    print "classes:"
    print "\t- %s"%puppetclass    
    
if __name__ == "__main__":
    if len(sys.argv)!=2:
        print "Usage: %s <hostname>"%sys.argv[0]
    host=sys.argv[1]
    main(host)
