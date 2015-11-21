# -*- coding: utf-8 -*-
"""This code is part of TestEnv extension

.. module:: testenv.application.web_server
   :platform: Unix
   :synopsis: Web server
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.core.masterhead import MasterHead
import hydratk.extensions.testenv.application.rest_handler as rest_handler
import hydratk.extensions.testenv.application.soap_handler as soap_handler
import web
import os

urls = (
         '/', 'Index',
         '/rs/customer', 'Customer',
         '/rs/payer', 'Payer',
         '/rs/subscriber', 'Subscriber',
         '/rs/contact', 'Contact',
         '/rs/contact/role', 'ContactRole',
         '/rs/address', 'Address',
         '/rs/address/role', 'AddressRole',
         '/rs/service', 'Service',
         '/ws/crm', 'SoapService'
        )
        
mh = None

class Server:    
        
    _server = None
    
    def __init__(self):
        """Class constructor
           
        Called when the object is initialized    
           
        """           
        
        global mh
        mh = MasterHead.get_head()               
        
    def _start(self):  
        """Method starts web server          
           
        """             
  
        ip = mh.cfg['Extensions']['TestEnv']['server_ip']
        port = mh.cfg['Extensions']['TestEnv']['server_port']   
        self._server = web.application(urls, globals())
        web.httpserver.runsimple(self._server.wsgifunc(), (str(ip), port))    
        
class Index:
    
    def GET(self):
        
        return 'Hello, World'
    
class Customer():
    """Handles requests on /rs/customer                           
    """     
    
    _rest = None
    
    def __init__(self):
    
        self._rest = rest_handler.RestHandler()
    
    def GET(self):
                
        return self._rest.read_customer(web.input())
    
    def POST(self):
        
        return self._rest.create_customer(web.data())
    
    def PUT(self):
        
        return self._rest.change_customer(web.data())
    
class Payer():
    """Handles requests on /rs/payer                           
    """       
    
    _rest = None
    
    def __init__(self):
        
        self._rest = rest_handler.RestHandler()
        
    def GET(self):
                
        return self._rest.read_payer(web.input())
    
    def POST(self):
        
        return self._rest.create_payer(web.data())
    
    def PUT(self):
        
        return self._rest.change_payer(web.data())    
    
class Subscriber():
    """Handles requests on /rs/subscriber                           
    """       
    
    _rest = None
    
    def __init__(self):
        
        self._rest = rest_handler.RestHandler()
        
    def GET(self):
                
        return self._rest.read_subscriber(web.input())
    
    def POST(self):
        
        return self._rest.create_subscriber(web.data())
    
    def PUT(self):
        
        return self._rest.change_subscriber(web.data())  
    
class Contact():
    """Handles requests on /rs/contact                           
    """       
    
    _rest = None
    
    def __init__(self):
        
        self._rest = rest_handler.RestHandler()
        
    def GET(self):
                
        return self._rest.read_contact(web.input())
    
    def POST(self):
        
        return self._rest.create_contact(web.data())
    
    def PUT(self):
        
        return self._rest.change_contact(web.data())  
    
class ContactRole():
    """Handles requests on /rs/contact/role                           
    """       
    
    _rest = None
    
    def __init__(self):
        
        self._rest = rest_handler.RestHandler()
    
    def POST(self):
        
        return self._rest.assign_contact_role(web.data())
    
    def PUT(self):
        
        return self._rest.revoke_contact_role(web.data())       
    
class Address():
    """Handles requests on /rs/address                           
    """       
    
    _rest = None
    
    def __init__(self):
        
        self._rest = rest_handler.RestHandler()
        
    def GET(self):
                
        return self._rest.read_address(web.input())
    
    def POST(self):
        
        return self._rest.create_address(web.data())
    
    def PUT(self):
        
        return self._rest.change_address(web.data()) 
    
class AddressRole():
    """Handles requests on /rs/address/role                           
    """       
    
    _rest = None
    
    def __init__(self):
        
        self._rest = rest_handler.RestHandler()
    
    def POST(self):
        
        return self._rest.assign_address_role(web.data())
    
    def PUT(self):
        
        return self._rest.revoke_address_role(web.data())  
    
class Service():
    """Handles requests on /rs/service                           
    """       
    
    _rest = None
    
    def __init__(self):
        
        self._rest = rest_handler.RestHandler()
        
    def GET(self):
        
        return self._rest.read_services(web.input())        
    
    def POST(self):
        
        return self._rest.create_service(web.data())
    
    def PUT(self):
        
        return self._rest.change_service(web.data())           
    
class SoapService():
    
    _soap = None
    
    def __init__(self):
        
        self._soap = soap_handler.SoapHandler()    
        
    def GET(self):
        
        key = web.input().keys()[0]
        ext_dir = mh.cfg['Extensions']['TestEnv']['ext_dir'] 
        
        if (key == 'wsdl'):
            soap_file = os.path.join(ext_dir, 'crm.wsdl')
        elif (key == 'xsd'):
            soap_file = os.path.join(ext_dir, 'crm.xsd')
        else:
            return web.NotFound() 
        
        if (os.path.exists(soap_file)):            
            with open(soap_file, 'r') as file:
                web.header('Content-Type', 'text/xml')
                return file.read()
        else:
            mh.dmsg('htk_on_extension_error', self._mh._trn.msg('te_web_unknown_file', soap_file), 
                    self._mh.fromhere())
            return web.NotFound()         
        
    def POST(self):
        
        return self._soap.dispatcher(web.ctx.env, web.data())      