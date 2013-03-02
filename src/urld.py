#!/usr/bin/env python
'''
Created on 04/ago/2012

@author: fede
'''
import sys
import tornado.options
import tornado.httpserver
import tornado.ioloop
from tornado import web
from tornado.options import define, options

#GLOBAL Options 
define("host"   ,         default="localhost"  , help="Default host")
define("conf"   ,         default="url.cnf"  , help="configuration file")
define("daemon"   ,       default="False"  , help="Run as daemon")
define("bin_path"   ,     default="./"  , help="Installation Path")
define("server_port",     default=80  ,         help="run on the given port", type=int)
define("server_proto",    default="SSL"  , help="enable ssl")
define("server_ssl_certfile",    default="./ssl/server.crt"  , help="enable ssl")
define("server_ssl_keyfile" ,    default="./ssl/server.key"  , help="enable ssl")

class UrlApp(tornado.web.Application):
    '''
    URL tornado web application
    '''
    def __init__(self):
        
        handlers =  [ ]
        # Set up GLOBAL VAR (Parameters)
        ##############################################################################
        
        # Define END POINT and HANDLERS
        self.url_hostname = options.host
        endpoint = r""
        for el in self.url_hostname.split('.'):
                if endpoint:
                    endpoint += r"\."+el
                else:
                    endpoint = el
        
        rootHandlers = []

        #INIT TONARDO APP
        ############################################################################
        web.Application.__init__(self, handlers)

        #SET UP MANAGER
        from manager.UrlMng import UrlMng
        self.UrlManager = UrlMng()
        ############################################################################
        #
        #URL HANDLER
        #############################################################################
        from handlers.InitialHandler import InitialHandler
        rootHandlers.append((r"/", InitialHandler))
        from handlers.UrlHandler import UrlHandler
        rootHandlers.append((r"/home", UrlHandler))
        from handlers.FinalHandler import FinalHandler
        rootHandlers.append((r"/(.*)", FinalHandler))   
        # Activate new URLS
        self.add_handlers(endpoint,rootHandlers)
        
                


def _setup_path():
        sys.path.append(options.bin_path)  
        
def _parse_opts():
        #Read Command Line 
        tornado.options.parse_command_line()
        # Read File 
        tornado.options.parse_config_file(options.conf)
        #Command line has precedence 
        tornado.options.parse_command_line()
   
def  main():
    #Read Command line
    ############################################   
    _parse_opts()
    _setup_path()
    
    #Run Application
    ############################################
    application = UrlApp()

    if options.server_proto == "SSL":
        http_server = tornado.httpserver.HTTPServer(application,ssl_options=dict(
            certfile=options.server_ssl_certfile,
            keyfile=options.server_ssl_keyfile))
    else:
        http_server = tornado.httpserver.HTTPServer(application)
        
    http_server.listen(options.server_port)
    
    tornado.ioloop.IOLoop.instance().start()  

if __name__ == "__main__":
    main()
