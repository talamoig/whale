'''
Created on Feb 24, 2012

Credits go to: http://www.osmonov.com/2009/04/client-certificates-with-urllib2.html

@author: talamoig
'''


import urllib2, httplib
class HTTPSClientAuthHandler(urllib2.HTTPSHandler):

    def __init__(self, key, cert):
        urllib2.HTTPSHandler.__init__(self)
        self.key = key
        self.cert = cert

    def https_open(self, req):
        # Rather than pass in a reference to a connection class, we pass in
        # a reference to a function which, for all intents and purposes,
        # will behave as a constructor
        print "certificate path: %s"%self.cert
        return self.do_open(self.getConnection, req)

    def getConnection(self, host, timeout=300):
        return httplib.HTTPSConnection(host, key_file=self.key, cert_file=self.cert)

        
