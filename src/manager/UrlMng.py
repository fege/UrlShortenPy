'''
Created on 04/ago/2012

@author: fede
'''
import tornado.options
from tornado.options import define, options
import logging

class UrlMng(object):
    '''
    URLMANAGER class that interact with the Driver of the DB
    '''
    _LOGGER = logging.getLogger('URL_MANAGER')
    
    def __init__(self):
        '''
        connection with the right DB reading the conf file, to change the DB modify url.cnf
        '''
        define("url_driver"      , default="False"  , help="Enable Authentication")
        #READ Options
        tornado.options.parse_config_file(options.conf)
        resource_plugin = "%s.UrlDriver" % options.url_driver
        resource_mod = __import__(resource_plugin, globals(), locals(), ['UrlDriver'])
        Url = getattr(resource_mod, 'UrlDriver')
        self.url = Url()
                
    def getShort(self,long_url):
        #get short_url stored on DB given long_url
        return self.url.getShort(long_url)
    
    def getLong(self,short_url):
        #get long_url stored on DB given short_url
        return self.url.getLong(short_url)
    
    def checkUrl(self,long_url):
        #check the existence of long_url on the DB
        res = self.url.checkExist(long_url)
        if res != None and res > 0 :
            return True
        return False
    
    def checkShort(self,short_url):
        #check the existence of short_url on the DB
        res = self.url.checkExist(short_url)
        if res != None and res > 0 :
            return True
        return False
    
    def setBidir(self,short_url,long_url):
        #set the long_url linked to the short_url
        self.url.setBid(short_url,long_url)
    
    def setShort(self,long_url,short_url):
        #set the short_url linked to the long_url
        self.url.setShort(long_url,short_url)