# -*- coding: utf-8 -*-
"""Web server

.. module:: testenv.web_server
   :platform: Unix
   :synopsis: Web server
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.core.masterhead import MasterHead
from hydratk.extensions.testenv.rest_handler import RestHandler
from hydratk.extensions.testenv.soap_handler import SoapHandler
from web import application, httpserver, input, data, NotFound, header, ctx
from os import path

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

class Server(object):   
    """Class Server
    """ 
        
    _server = None
    
    def __init__(self):
        """Class constructor
           
        Called when the object is initialized    
        
        Args:
           none
           
        """           
        
        global mh
        mh = MasterHead.get_head()               
        
    def _start(self):  
        """Method starts web server   
        
        Args:
           none
        
        Returns:
           void       
           
        """             
  
        ip = mh.cfg['Extensions']['TestEnv']['server_ip']
        port = mh.cfg['Extensions']['TestEnv']['server_port']   
        self._server = application(urls, globals())
        httpserver.runsimple(self._server.wsgifunc(), (str(ip), port))    
        
class Index(object):
    
    def GET(self):
        
        return 'Hello, World'
    
class Customer(object):
    """Handles requests on /rs/customer                           
    """     
    
    _rest = None
    
    def __init__(self):
    
        self._rest = RestHandler()
    
    def GET(self):
                
        return self._rest.read_customer(input())
    
    def POST(self):
        
        return self._rest.create_customer(data())
    
    def PUT(self):
        
        return self._rest.change_customer(data())
    
class Payer(object):
    """Handles requests on /rs/payer                           
    """       
    
    _rest = None
    
    def __init__(self):
        
        self._rest = RestHandler()
        
    def GET(self):
                
        return self._rest.read_payer(input())
    
    def POST(self):
        
        return self._rest.create_payer(data())
    
    def PUT(self):
        
        return self._rest.change_payer(data())    
    
class Subscriber(object):
    """Handles requests on /rs/subscriber                           
    """       
    
    _rest = None
    
    def __init__(self):
        
        self._rest = RestHandler()
        
    def GET(self):
                
        return self._rest.read_subscriber(input())
    
    def POST(self):
        
        return self._rest.create_subscriber(data())
    
    def PUT(self):
        
        return self._rest.change_subscriber(data())  
    
class Contact(object):
    """Handles requests on /rs/contact                           
    """       
    
    _rest = None
    
    def __init__(self):
        
        self._rest = RestHandler()
        
    def GET(self):
                
        return self._rest.read_contact(input())
    
    def POST(self):
        
        return self._rest.create_contact(data())
    
    def PUT(self):
        
        return self._rest.change_contact(data())  
    
class ContactRole(object):
    """Handles requests on /rs/contact/role                           
    """       
    
    _rest = None
    
    def __init__(self):
        
        self._rest = RestHandler()
    
    def POST(self):
        
        return self._rest.assign_contact_role(data())
    
    def PUT(self):
        
        return self._rest.revoke_contact_role(data())       
    
class Address(object):
    """Handles requests on /rs/address                           
    """       
    
    _rest = None
    
    def __init__(self):
        
        self._rest = RestHandler()
        
    def GET(self):
                
        return self._rest.read_address(input())
    
    def POST(self):
        
        return self._rest.create_address(data())
    
    def PUT(self):
        
        return self._rest.change_address(data()) 
    
class AddressRole(object):
    """Handles requests on /rs/address/role                           
    """       
    
    _rest = None
    
    def __init__(self):
        
        self._rest = RestHandler()
    
    def POST(self):
        
        return self._rest.assign_address_role(data())
    
    def PUT(self):
        
        return self._rest.revoke_address_role(data())  
    
class Service(object):
    """Handles requests on /rs/service                           
    """       
    
    _rest = None
    
    def __init__(self):
        
        self._rest = RestHandler()
        
    def GET(self):
        
        return self._rest.read_services(input())        
    
    def POST(self):
        
        return self._rest.create_service(data())
    
    def PUT(self):
        
        return self._rest.change_service(data())           
    
class SoapService(object):
    """Handles requests on /ws/crm                           
    """      
    
    _soap = None
    
    def __init__(self):
        
        self._soap = SoapHandler()    
        
    def GET(self):
        
        key = list(input().keys())[0]
        ext_dir = mh.cfg['Extensions']['TestEnv']['ext_dir'] 
        
        if (key == 'wsdl'):
            soap_file = path.join(ext_dir, 'crm.wsdl')
        elif (key == 'xsd'):
            soap_file = path.join(ext_dir, 'crm.xsd')
        else:
            return NotFound() 
        
        if (path.exists(soap_file)):            
            with open(soap_file, 'r') as file:
                header('Content-Type', 'text/xml')
                return file.read()
        else:
            mh.dmsg('htk_on_extension_error', self._mh._trn.msg('te_web_unknown_file', soap_file), 
                    self._mh.fromhere())
            return NotFound()         
        
    def POST(self):
        
        return self._soap.dispatcher(ctx.env, data())      