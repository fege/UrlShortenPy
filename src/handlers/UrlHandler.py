'''
Created on 04/ago/2012

@author: fede
'''
import tornado.web
import time
from datetime import datetime
import sys
import logging
import logging.config
logging.config.fileConfig("logging.conf")

#alphabet to use in short url
ALPHABET=map(str,range(0, 10)) + map(chr, range(97, 123) + range(65, 91))

class UrlHandler(tornado.web.RequestHandler):
    '''
    URLHANLDER used to write the interface and to generate short_url
    ''' 
    _LOGGER = logging.getLogger('URL_HANDLER')

    def get(self):
        '''
        get operation show the form to generate the link
        '''
        self._LOGGER.info("Get operation on web page")
         
        self.write("<br>")
        self.write("<form method=post action=''>") 
        self.write("<table>"
        "<tr><td>insert url: </td><td><input type='text' size='20' value=' ' name='long_url'/></td></tr>"
        "<tr><td><input type=submit name=shortButton value=Generate></td>"
        "<td><input type=reset name=resetButton value=Reset></td></tr>"
        "</table>")
        self.write("</form>")
    
    def post(self):
        '''
        post operation which generate the short_url given the long_url passed by a form
        '''
        self._LOGGER.info("post operation on web page")
        
        long_url = self.get_argument('long_url')
        
        if not long_url:
            self._LOGGER.debug("no long url %s " %long_url)
            self.write("Form was empty")
            self.write("<br>")
            #self.write("<a href='https://ec2-23-23-28-101.compute-1.amazonaws.com/home'>Back</a>")
            self.write("<a href='https://urlshorten.alluneed.it/home'>Back</a>")
        elif self.check_long_url(long_url):
            self._LOGGER.debug("Url already short %s " %long_url)
            self.write("Url is already short %s " %long_url)
            self.write("<br>")
            #self.write("<a href='https://ec2-23-23-28-101.compute-1.amazonaws.com/home'>Back</a>") 
            self.write("<a href='https://urlshorten.alluneed.it/home'>Back</a>")
        else:
            short_url = ''
            #check if the long_url it is already created a short_url
            res = self.application.UrlManager.checkUrl(long_url)
            self._LOGGER.debug("Url already saved %s " %res)

            if res:
                #return the short_url
                short_url = self.application.UrlManager.getShort(long_url)
                #add 1 visit to the counter
                self.application.UrlManager.setVisit(long_url)
                self._LOGGER.info("Increment the visit at %s " %res)
            
            else:
                #check the existence of short_url because it is random
                #it will be better to use an hash function
                while True:
                    short_url = self.conv_code((time.time()*10))
                    if not self.application.UrlManager.checkShort(short_url):
                        break
                #set the short_url given the long_url
                self.application.UrlManager.setShort(long_url,short_url)
                #set the long_url linked to the short_url
                self.application.UrlManager.setBidir(short_url,long_url)
                #initialize the counter
                self.application.UrlManager.setVisit(long_url)
                #initialize the date
                self.application.UrlManager.setDate(long_url)
            
            num_view = self.application.UrlManager.getVisit(long_url)
            date_insert = self.application.UrlManager.getDate(long_url)
            #intervall = datetime.now()-datetime(date_insert)
            
            self._LOGGER.debug("short url saved %s " %short_url)
            self._LOGGER.debug("long url saved %s " %long_url)
            self._LOGGER.debug("num view %s for %s getted" %(num_view,long_url))
            self._LOGGER.debug("date getted %s " %date_insert)
            
            self.write("<br>")
            self.write("click below or copy and paste on a browser")
            self.write("<br>")
            self.write("link: <a href='https://localhost/"+str(short_url)+"'>https://urlshorten.alluneed.it/"+str(short_url)+"</a>")
            #self.write("link: <a href='https://ec2-23-23-28-101.compute-1.amazonaws.com/"+str(short_url)+"'>https://ec2-23-23-28-101.compute-1.amazonaws.com/"+str(short_url)+"</a>")
            self.write("<br>")
            self.write("number of visit for "+str(long_url)+" is "+num_view)
            self.write("<br>")
            self.write("saved the first time the "+str(date_insert))
            self.write("<br>")
            #self.write("present in the db for "+intervall+" days")
            #self.write("<br>")
            self.write("<a href='https://urlshorten.alluneed.it/home'>Back</a>")
            #self.write("<a href='https://ec2-23-23-28-101.compute-1.amazonaws.com/home'>Back</a>")
        
    def conv_code(self,num_url, letters=ALPHABET):
        '''
        function to create a pseudo-random string
        '''
        self._LOGGER.info("Conversion operation ")

        base = len(letters)-1
        chars = []
        while (num_url>0):    
            chars.append(letters[int(num_url % base)])
            num_url //= base
        return ''.join(chars)
    
    def base62_encode(self,num, alphabet=ALPHABET):
        if (num == 0):
            return alphabet[0]
        arr = []
        base = len(alphabet)
        while num:
            rem = num % base
            num = num // base
            arr.append(alphabet[rem])
        arr.reverse()
        return ''.join(arr)
    
    def check_long_url(self,long_url):
        '''
        function to control if long url is already short
        '''
        if long_url.count('/') == 2:
            return True
        
        if long_url.count('/') == 3 and long_url.rfind('/')+1 == len(long_url):
            return True
        
        return False

    
