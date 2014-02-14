from optparse import OptionParser
import sys

from whale.utils.Configurable import Configurable

configuration = None


def readConfig(configfile):
    global configuration
    try:
        open(configfile,"r")    
    except Exception:
        print("Cannot read %s"%configfile)
        sys.exit(1)
    try: 
        configuration=Configurable(configfile,"WHALE")
    except Exception:
        print("WHALE section not found")
        sys.exit(1)
    
def main():   
    parser = OptionParser()
    parser.add_option("-r","--run", dest="commands",
                      help="commands to run")
    parser.add_option("-c","--config", dest="configfile",
                      help="read configuration from FILE instead of default", metavar="FILE",
                      default="/etc/whale/whale.conf")
    parser.add_option("-f","--format", dest="format",
                      help="not implemented yet")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="set logging mode to verbose")
    (options, args) = parser.parse_args()
    readConfig(options.configfile)

    if options.commands==None:
        sys.exit(1)
    if options.commands=="-":
        while 1:
            try:    
                line = sys.stdin.readline()
            except KeyboardInterrupt:
                break
            if not line:
                break
            exec("print %s"%line.strip())
    else:
        exec("print %s"%options.commands)


config="/etc/whale/whale.conf"
readConfig(config)
initscript=configuration.getItem("initscript")
execfile(initscript)

if __name__ == "__main__":
    main()


