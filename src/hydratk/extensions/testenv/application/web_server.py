# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.extensions.testenv.application.web_server
   :platform: Unix
   :synopsis: Web server
.. moduleauthor:: Petr Rašek <pr@hydratk.org>

"""

import hydratk.extensions.testenv.application.rest_handler as rest_handler;
import web;

urls = (
         '/', 'Index',
         '/rs/customer', 'Customer',
         '/rs/payer', 'Payer',
         '/rs/subscriber', 'Subscriber',
         '/rs/contact', 'Contact',
         '/rs/contact/role', 'ContactRole',
         '/rs/address', 'Address',
         '/rs/address/role', 'AddressRole',
         '/rs/service', 'Service'
        );
        
mh = None;

class Server:    
        
    _server = None;
    
    def __init__(self, _mh):
        
        global mh;
        mh = _mh;                 
        
    def _start(self):    
  
        ip = mh.cfg['Extensions']['TestEnv']['server_ip'];
        port = mh.cfg['Extensions']['TestEnv']['server_port'];   
        self._server = web.application(urls, globals());
        web.httpserver.runsimple(self._server.wsgifunc(), (str(ip), port));    
        
class Index:
    
    def GET(self):
        
        return 'Hello, World';
    
class Customer():
    """Handles requests on /rs/customer                           
    """     
    
    rest = None;
    
    def __init__(self):
    
        self.rest = rest_handler.REST_handler(mh);
    
    def GET(self):
                
        return self.rest.read_customer(web.input());
    
    def POST(self):
        
        return self.rest.create_customer(web.data());
    
    def PUT(self):
        
        return self.rest.change_customer(web.data());
    
class Payer():
    """Handles requests on /rs/payer                           
    """       
    
    rest = None;
    
    def __init__(self):
        
        self.rest = rest_handler.REST_handler(mh);
        
    def GET(self):
                
        return self.rest.read_payer(web.input());
    
    def POST(self):
        
        return self.rest.create_payer(web.data());
    
    def PUT(self):
        
        return self.rest.change_payer(web.data());    
    
class Subscriber():
    """Handles requests on /rs/subscriber                           
    """       
    
    rest = None;
    
    def __init__(self):
        
        self.rest = rest_handler.REST_handler(mh);
        
    def GET(self):
                
        return self.rest.read_subscriber(web.input());
    
    def POST(self):
        
        return self.rest.create_subscriber(web.data());
    
    def PUT(self):
        
        return self.rest.change_subscriber(web.data());  
    
class Contact():
    """Handles requests on /rs/contact                           
    """       
    
    rest = None;
    
    def __init__(self):
        
        self.rest = rest_handler.REST_handler(mh);
        
    def GET(self):
                
        return self.rest.read_contact(web.input());
    
    def POST(self):
        
        return self.rest.create_contact(web.data());
    
    def PUT(self):
        
        return self.rest.change_contact(web.data());  
    
class ContactRole():
    """Handles requests on /rs/contact/role                           
    """       
    
    rest = None;
    
    def __init__(self):
        
        self.rest = rest_handler.REST_handler(mh);
    
    def POST(self):
        
        return self.rest.assign_contact_role(web.data());
    
    def PUT(self):
        
        return self.rest.revoke_contact_role(web.data());       
    
class Address():
    """Handles requests on /rs/address                           
    """       
    
    rest = None;
    
    def __init__(self):
        
        self.rest = rest_handler.REST_handler(mh);
        
    def GET(self):
                
        return self.rest.read_address(web.input());
    
    def POST(self):
        
        return self.rest.create_address(web.data());
    
    def PUT(self):
        
        return self.rest.change_address(web.data()); 
    
class AddressRole():
    """Handles requests on /rs/address/role                           
    """       
    
    rest = None;
    
    def __init__(self):
        
        self.rest = rest_handler.REST_handler(mh);
    
    def POST(self):
        
        return self.rest.assign_address_role(web.data());
    
    def PUT(self):
        
        return self.rest.revoke_address_role(web.data());  
    
class Service():
    """Handles requests on /rs/service                           
    """       
    
    rest = None;
    
    def __init__(self):
        
        self.rest = rest_handler.REST_handler(mh);
        
    def GET(self):
        
        return self.rest.read_services(web.input());        
    
    def POST(self):
        
        return self.rest.create_service(web.data());
    
    def PUT(self):
        
        return self.rest.change_service(web.data());                    