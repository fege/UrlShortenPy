'''
Created on 04/ago/2012

@author: fede
'''
import tornado.web
import logging 

class FinalHandler(tornado.web.RequestHandler):
    '''
    FINALHANDLER which permit the redirect via browser
    '''
    _LOGGER = logging.getLogger('FINAL_HANDLER')
    
    def get(self,url):
        '''
        given the short_url redirect on the right long_url
        '''
        self._LOGGER.debug("Get operation to redirect ")

        long_url = self.application.UrlManager.getLong(url)
        
        self._LOGGER.debug("Redirect to %s " %long_url)
        self.redirect(long_url, True, 301)
