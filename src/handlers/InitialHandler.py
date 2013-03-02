'''
Created on 04/ago/2012

@author: fede
'''
import tornado.web
import logging
import logging.config
logging.config.fileConfig("logging.conf")

class InitialHandler(tornado.web.RequestHandler):
    '''
    INITIALHANDLER which permit the redirect to home
    '''
    _LOGGER = logging.getLogger('INITIAL_HANDLER')
    
    def get(self):
        '''
        redirect on home
        '''
        self._LOGGER.debug("redirect initial")

        self._LOGGER.debug("Redirect to home " )
        self.redirect("/home", True, 301)
