'''
Created on 04/ago/2012

@author: fede
'''
import redis
import tornado.options
from tornado.options import define, options
from datetime import datetime
import logging
import logging.config
logging.config.fileConfig("logging.conf")

class UrlDriver():
    '''
    URLDRIVER class that talk directly with the DB
    '''
    _LOGGER = logging.getLogger('URL_DRIVER')
    
    def __init__(self):
        define("url_db",     default="1"         , help="Redis DB",)
        define("url_host",   default="urlshorten.alluneed.it" , help="Redis DB host",)
        define("url_port",   default=6379        , help="Redis DB port", type=int)
        define("url_passwd", default=None        , help="Redis DB password",)
        #READ Options
        tornado.options.parse_config_file(options.conf)
        #initializing of Redis not developed by ME
        self.redis = redis.StrictRedis(host=options.url_host, port=options.url_port, db=options.url_db,password=options.url_passwd)
    
    def checkExist(self,url):
        self._LOGGER.info("Check if %s exist " %url) 
        return self.redis.exists(url)
    
    def getShort(self,long_url,field='short'):
        self._LOGGER.info("Get short url")
        self._LOGGER.debug("Request related to %s" %long_url)
        return self.redis.hget(long_url, field)
    
    def getLong(self,short_url,field='long'):
        self._LOGGER.info("Get long url")
        self._LOGGER.debug("Request related to %s" %short_url)
        return self.redis.hget(short_url, field)

    def getVisit(self,long_url,field='visit'):
        self._LOGGER.info("Get number of visit of long url")
        self._LOGGER.debug("Request related to %s" %long_url)
        return self.redis.hget(long_url, field)

    def getDate(self,long_url,field='date'):
        self._LOGGER.info("Get date of insert of long url")
        self._LOGGER.debug("Request related to %s" %long_url)
        return self.redis.hget(long_url, field)
    
    def setShort(self, long_url, value, field='short'):
        self._LOGGER.info("Set short url")
        self._LOGGER.debug("Request related to %s" %long_url)
        self.redis.hset(long_url, field , value)
    
    def setBid(self,short_url,value,field='long'):
        self._LOGGER.info("Set long url")
        self._LOGGER.debug("Request related to %s" %short_url)
        self.redis.hset(short_url, field , value)
    
    def setVisit(self,long_url, field='visit'):
        value = self.getVisit(long_url)
        if not value:
            value = 0
        self._LOGGER.info("Set visit for long url")
        self._LOGGER.debug("Request related to %s" %long_url)
        self.redis.hset(long_url, field , int(value) + 1)

    def setDate(self,long_url, field='date'):
        value = datetime.now().isoformat()
        self._LOGGER.info("Set date of first request for long url")
        self._LOGGER.debug("Request related to %s" %long_url)
        self.redis.hset(long_url, field , value)

        
        
        
