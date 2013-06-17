#!/usr/bin/env python

import config as myconfig
from libmproxy import controller, proxy
import os
import Cookie

import MySQLdb as mdb

def conn():
    con = mdb.connect(myconfig.dbhost,
        myconfig.dbuser, myconfig.dbpass, myconfig.dbname)
    
    return con

class CookieMaster(controller.Master):
    def __init__(self, server):
        controller.Master.__init__(self, server)

    def run(self):
        try:
            return controller.Master.run(self)
        except KeyboardInterrupt:
            self.shutdown()

    def handle_request(self, msg):
        if msg.headers["set-cookie"]:
            print msg.headers["set-cookies"]
        
        msg.reply()

    def handle_response(self, msg):
        cookie = None
        
        for h in msg.headers:
            if h[0].lower() == "set-cookie":
                cookie = h[1]
        
        if cookie:
            
            host = msg.request.host
            
            c = Cookie.BaseCookie()
            
            try:
                c.load(cookie)
                
                co = c.items()[0][1]
                
                name = c.items()[0][0]
                
                con = conn()
                cur = con.cursor(mdb.cursors.DictCursor)
                print host
                cur.execute("""insert into proxy_cookies (datetime, name, value, expiry, host) 
                    values (NOW(), %s ,%s, %s, %s)""", (
                                                   str(name), 
                                                   str(co.value[:200]),
                                                   str(co['expires']),
                                                   str(host)))
                
                con.commit()
                con.close()
            except:
                print "error"
                pass
            
        
        msg.reply()


config = proxy.ProxyConfig(
    #cacert = os.path.expanduser("~/.mitmproxy/mitmproxy-ca.pem")
)
server = proxy.ProxyServer(config, 8080)
m = CookieMaster(server)
m.run()
