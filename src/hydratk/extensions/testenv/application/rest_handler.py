# -*- coding: utf-8 -*-
"""This code is part of TestEnv extension

.. module:: testenv.application.rest_handler
   :platform: Unix
   :synopsis: Handles REST operations
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.core.masterhead import MasterHead
from hydratk.extensions.testenv.interfaces.db_int import DB_INT
from web import OK, NotFound, BadRequest
from jsonlib2 import read, write

class RestHandler:
    
    _mh = None
    
    def __init__(self):
        """Class constructor
           
        Called when the object is initialized    
        
        Args:
           
        """            
        
        self._mh = MasterHead.get_head()

    def _get_db(self): 
        """Method connect to database     
           
        Args:

        Returns:
           DB_INT: DB client                 
                
        """              
    
        db = DB_INT()
        db.connect()
        return db

    def read_customer(self, data):
        """Method handles GET customer           
           
        Args:
           data (dict) - request input with customer id 
             
        Returns:
           http: HTTP 200 with customer detail in JSON,
                 HTTP 404 when customer not found,
                 HTTP 400 when param id is missing 
           
        Example:
        
        .. code-block:: javascript
        
           {
             "id": 1,
             "name": "Charlie Bowman",
             "status": "active",
             "segment": 2,
             "birth_no": "700101/0001",
             "reg_no": "123456",
             "tax_no": "CZ123456"
           }         
                
        """          
           
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_request', 'read_customer', data), 
                      self._mh.fromhere())
        
        if (data.has_key('id')):
        
            db = self._get_db()            
            customer = db.read_customer(data.id)
            db.disconnect()
            
            if (customer != None):
                return customer.tojson()
            else:
                return NotFound                        
        
        else:
            return BadRequest()
        
    def create_customer(self, data):   
        """Method handles POST customer           
           
        Args:
           data (json): customer detail  
             
        Returns:
           http: HTTP 200 with id of created customer,
                 HTTP 400 when customer not created
           
        Example:
        
        .. code-block:: javascript
        
           {
             "name": "Charlie Bowman",
             "status": "active",
             "segment": 2,
             "birth_no": "700101/0001",
             "reg_no": "123456",
             "tax_no": "CZ123456"
           }         
                
        """              
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_request', 'create_customer', data), 
                      self._mh.fromhere())        
        
        doc = read(data)
        name = doc['name'] if doc.has_key('name') else None
        status = doc['status'] if doc.has_key('status') else 'active'
        segment = doc['segment'] if doc.has_key('segment') else None
        birth_no = doc['birth_no'] if doc.has_key('birth_no') else None
        reg_no = doc['reg_no'] if doc.has_key('reg_no') else None
        tax_no = doc['tax_no'] if doc.has_key('tax_no') else None
        
        db = self._get_db()
        id = db.create_customer(name, segment, status, birth_no, reg_no, tax_no)
        db.disconnect()
        
        if (id != None):
            return id
        else:
            return BadRequest()
        
    def change_customer(self, data):  
        """Method handles PUT customer           
           
        Args:
           data (json): customer detail  
             
        Returns:
           http: HTTP 200 when customer changed,
                 HTTP 400 when customer not changed
           
        Example:
        
        .. code-block:: javascript
        
           {
             "id": 1,
             "name": "Charlie Bowman",
             "status": "active",
             "segment": 2,
             "birth_no": "700101/0001",
             "reg_no": "123456",
             "tax_no": "CZ123456"
           }                    
                
        """           
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_request', 'change_customer', data), 
                      self._mh.fromhere())        
        
        doc = read(data)
        id = doc['id'] if doc.has_key('id') else None
        name = doc['name'] if doc.has_key('name') else None
        status = doc['status'] if doc.has_key('status') else None
        segment = doc['segment'] if doc.has_key('segment') else None
        birth_no = doc['birth_no'] if doc.has_key('birth_no') else None
        reg_no = doc['reg_no'] if doc.has_key('reg_no') else None
        tax_no = doc['tax_no'] if doc.has_key('tax_no') else None
        
        db = self._get_db()
        res = db.change_customer(id, name, status, segment, birth_no, reg_no, tax_no)
        db.disconnect()
        
        if (res):
            return OK()
        else:
            return BadRequest()       
        
    def read_payer(self, data):  
        """Method handles GET payer           
           
        Args:
           data (dict): request input with payer id   
             
        Returns:
           http: HTTP 200 with payer detail in JSON,
                 HTTP 404 when payer not found,
                 HTTP 400 when param id is missing 
           
        Example:
        
        .. code-block:: javascript
        
           {
             "id": 1,
             "name": "Charlie Bowman",
             "status": "active",
             "billcycle": 1,
             "bank_account": "123456/0100",
             "customer": 1
           }         
                
        """             
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_request', 'read_payer', data), 
                      self._mh.fromhere())        
        
        if (data.has_key('id')):
        
            db = self._get_db()            
            payer = db.read_payer(data.id)
            db.disconnect()
            
            if (payer != None):
                return payer.tojson()
            else:
                return NotFound                        
        
        else:
            return BadRequest()
        
    def create_payer(self, data): 
        """Method handles POST payer           
           
        Args:
           data (json): payer detail  
             
        Returns:
           http: HTTP 200 with id of created payer,
                 HTTP 400 when payer not created
                
        Example:
        
        .. code-block:: javascript
        
           {
             "name": "Charlie Bowman",
             "status": "active",
             "billcycle": 1,
             "bank_account": "123456/0100",
             "customer": 1
           }                
                
        """            
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_request', 'create_payer', data), 
                      self._mh.fromhere())        
        
        doc = read(data)
        name = doc['name'] if doc.has_key('name') else None
        status = doc['status'] if doc.has_key('status') else 'active'
        billcycle = doc['billcycle'] if doc.has_key('billcycle') else None
        bank_account = doc['bank_account'] if doc.has_key('bank_account') else None
        customer = doc['customer'] if doc.has_key('customer') else None
        
        db = self._get_db()
        id = db.create_payer(name, billcycle, customer, status, bank_account)
        db.disconnect()
        
        if (id != None):
            return id
        else:
            return BadRequest()
        
    def change_payer(self, data): 
        """Method handles PUT payer           
           
        Args:
           data (json) - payer detail  
             
        Returns:
           http: HTTP 200 when payer changed,
                 HTTP 400 when payer not changed
                
        Example:
        
        .. code-block:: javascript
        
           {
             "id": 1,
             "name": "Charlie Bowman",
             "status": "active",
             "billcycle": 1,
             "bank_account": "123456/0100",
             "customer": 1
           }                 
                
        """             
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_request', 'change_payer', data), 
                      self._mh.fromhere())        
        
        doc = read(data)
        id = doc['id'] if doc.has_key('id') else None
        name = doc['name'] if doc.has_key('name') else None
        status = doc['status'] if doc.has_key('status') else None
        billcycle = doc['billcycle'] if doc.has_key('billcycle') else None
        bank_account = doc['bank_account'] if doc.has_key('bank_account') else None
        customer = doc['customer'] if doc.has_key('customer') else None
        
        db = self._get_db()
        res = db.change_payer(id, name, status, billcycle, bank_account, customer)
        db.disconnect()
        
        if (res):
            return OK()
        else:
            return BadRequest() 
        
    def read_subscriber(self, data):  
        """Method handles GET subscriber           
           
        Args:
           data (dict) - request input with subscriber id   
             
        Returns:
           http: HTTP 200 with subscriber detail in JSON,
                 HTTP 404 when subscriber not found,
                 HTTP 400 when param id is missing 
           
        Example:
        
        .. code-block:: javascript
        
           {
             "id": 1,
             "name": "Charlie Bowman",
             "msisdn": "123456"
             "status": "active",
             "market": 1,
             "tariff": 433,
             "customer": 1,
             "payer": 2
           }         
                
        """             
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_request', 'read_subscriber', data), 
                      self._mh.fromhere())        
        
        if (data.has_key('id')):
        
            db = self._get_db()            
            subscriber = db.read_subscriber(data.id)
            db.disconnect()
            
            if (subscriber != None):
                return subscriber.tojson()
            else:
                return NotFound                        
        
        else:
            return BadRequest()
        
    def create_subscriber(self, data):
        """Method handles POST subscriber           
           
        Args:
           data (json) - subscriber detail  
             
        Returns:
           http: HTTP 200 with id of created subscriber,
                 HTTP 400 when subscriber not created
                
        Example:
        
        .. code-block:: javascript
        
           {
             "name": "Charlie Bowman",
             "msisdn": "123456"
             "status": "active",
             "market": 1,
             "tariff": 433,
             "customer": 1,
             "payer": 2
           }                 
                
        """                 
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_request', 'create_subscriber', data), 
                      self._mh.fromhere())        
        
        doc = read(data)
        name = doc['name'] if doc.has_key('name') else None
        msisdn = doc['msisdn'] if doc.has_key('msisdn') else None
        status = doc['status'] if doc.has_key('status') else 'active'
        market = doc['market'] if doc.has_key('market') else None
        tariff = doc['tariff'] if doc.has_key('tariff') else None
        customer = doc['customer'] if doc.has_key('customer') else None
        payer = doc['payer'] if doc.has_key('payer') else None
        
        db = self._get_db()
        id = db.create_subscriber(name, msisdn, market, tariff, customer, payer, status)
        db.disconnect()
        
        if (id != None):
            return id
        else:
            return BadRequest()
        
    def change_subscriber(self, data):  
        """Method handles PUT subscriber           
           
        Args:
           data (json): payer detail  
             
        Returns:
           http: HTTP 200 when subscriber changed,
                 HTTP 400 when subscriber not changed
                
        Example:
        
        .. code-block:: javascript
        
           {
             "id": 1,
             "name": "Charlie Bowman",
             "msisdn": "123456"
             "status": "active",
             "market": 1,
             "tariff": 433,
             "customer": 1,
             "payer": 2
           }                 
                
        """            
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_request', 'change_subscriber', data), 
                      self._mh.fromhere())        
        
        doc = read(data)
        id = doc['id'] if doc.has_key('id') else None
        name = doc['name'] if doc.has_key('name') else None
        msisdn = doc['msisdn'] if doc.has_key('msisdn') else None
        status = doc['status'] if doc.has_key('status') else None
        market = doc['market'] if doc.has_key('market') else None
        tariff = doc['tariff'] if doc.has_key('tariff') else None
        customer = doc['customer'] if doc.has_key('customer') else None
        payer = doc['payer'] if doc.has_key('payer') else None
        
        db = self._get_db()
        res = db.change_subscriber(id, name, msisdn, status, market, tariff, customer, payer)
        db.disconnect()
        
        if (res):
            return OK()
        else:
            return BadRequest()  
        
    def read_contact(self, data):  
        """Method handles GET contact           
           
        Args:
           data (dict): request input with contact id   
             
        Returns:
           http: HTTP 200 with contact detail in JSON, choice customer|payer|subscriber,
                 HTTP 404 when contact not found,
                 HTTP 400 when param id is missing 
                
        Example:
        
        .. code-block:: javascript  
        
           {
             "id": 1,
             "name": "Charlie Bowman",
             "phone": "123456"
             "email": "aaa@xxx.com",
             "roles": {
               "role": [
                 {
                   "id": 1,
                   "title": "contract",
                   "customer": 1,
                   "payer": 1,
                   "subscriber": 1
                 }  
             ]}
           }               
                
        """             
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_request', 'read_contact', data), 
                      self._mh.fromhere())        
        
        if (data.has_key('id')):
        
            db = self._get_db()            
            contact = db.read_contact(data.id)
            db.disconnect()
            
            if (contact != None):
                return contact.tojson()
            else:
                return NotFound                        
        
        else:
            return BadRequest()
        
    def create_contact(self, data):  
        """Method handles POST contact           
           
        Args:
           data (json): contact detail  
             
        Returns:
           http: HTTP 200 with id of created contact,
                 HTTP 400 when contact not created
                
        Example:
        
        .. code-block:: javascript        
                
           {
             "name": "Charlie Bowman",
             "phone": "123456"
             "email": "aaa@xxx.com"
           }                 
                
        """           
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_request', 'create_contact', data), 
                      self._mh.fromhere())        
        
        doc = read(data)
        name = doc['name'] if doc.has_key('name') else None
        phone = doc['phone'] if doc.has_key('phone') else None
        email = doc['email'] if doc.has_key('email') else None
        
        db = self._get_db()
        id = db.create_contact(name, phone, email)
        db.disconnect()
        
        if (id != None):
            return id
        else:
            return BadRequest()
        
    def change_contact(self, data):  
        """Method handles PUT customer           
           
        Args:
           data (json): contact detail  
             
        Returns:
           http: HTTP 200 when contact changed,
                 HTTP 400 when contact not changed
           
        Example:
        
        .. code-block:: javascript        
                
           {
             "id": 1,
             "name": "Charlie Bowman",
             "phone": "123456"
             "email": "aaa@xxx.com"
           }             
                
        """            
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_request', 'change_contact', data), 
                      self._mh.fromhere())        
        
        doc = read(data)
        id = doc['id'] if doc.has_key('id') else None
        name = doc['name'] if doc.has_key('name') else None
        phone = doc['phone'] if doc.has_key('phone') else None
        email = doc['email'] if doc.has_key('email') else None
        
        db = self._get_db()
        res = db.change_contact(id, name, phone, email)
        db.disconnect()
        
        if (res):
            return OK()
        else:
            return BadRequest()                     
        
    def assign_contact_role(self, data):   
        """Method handles POST contact/role           
           
        Args:
           data (json): contact role detail, choice customer|payer|subscriber   
             
        Returns:
           http: HTTP 200 when contact role assigned,
                 HTTP 400 when customer role not assigned
           
        Example:
        
        .. code-block:: javascript
        
           {
             "id": 1,
             "title": "contract",
             "customer": 1,
             "payer": 1,
             "subscriber": 1
           }         
                
        """           
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_request', 'assign_contact_role', data), 
                      self._mh.fromhere())        
        
        doc = read(data)
        id = doc['id'] if doc.has_key('id') else None
        role = doc['title'] if doc.has_key('title') else None
        customer = doc['customer'] if doc.has_key('customer') else None
        payer = doc['payer'] if doc.has_key('payer') else None
        subscriber = doc['subscriber'] if doc.has_key('subscriber') else None
        
        db = self._get_db()
        res = db.assign_contact_role(id, role, customer, payer, subscriber)
        db.disconnect()
        
        if (res):
            return OK()
        else:
            return BadRequest()      
        
    def revoke_contact_role(self, data): 
        """Method handles PUT contact/role           
           
        Args:
           data (json): contact role detail, choice customer|payer|subscriber  
             
        Returns:
           http: HTTP 200 when contact role revoked,
                 HTTP 400 when customer role not revoked
           
        Example:
        
        .. code-block:: javascript
        
           {
             "id": 1,
             "title": "contract",
             "customer": 1,
             "payer": 1,
             "subscriber": 1
           }          
                
        """              
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_request', 'revoke_contat_role', data), 
                      self._mh.fromhere())        
        
        doc = read(data)
        id = doc['id'] if doc.has_key('id') else None
        role = doc['title'] if doc.has_key('title') else None
        customer = doc['customer'] if doc.has_key('customer') else None
        payer = doc['payer'] if doc.has_key('payer') else None
        subscriber = doc['subscriber'] if doc.has_key('subscriber') else None
        
        db = self._get_db()
        res = db.revoke_contact_role(id, role, customer, payer, subscriber)
        db.disconnect()
        
        if (res):
            return OK()
        else:
            return BadRequest()      
        
    def read_address(self, data):  
        """Method handles GET address           
           
        Args:
           data (dict): request input with address id   
             
        Returns:
           http: HTTP 200 with address detail in JSON, choice contact|customer|payer|subscriber,
                 HTTP 404 when address not found,
                 HTTP 400 when param id is missing
           
        Example:
        
        .. code-block:: javascript  
        
           {
             "id": 1,
             "street": "Tomickova",
             "street_no": "2144/1"
             "city": "Praha",
             "zip": 14800
             "roles": {
               "role": [
                 {
                   "id": 1,
                   "title": "contract",
                   "contact": 1,
                   "customer": 1,
                   "payer": 1,
                   "subscriber": 1
                 }  
             ]}
           }             
                
        """             
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_request', 'read_address', data), 
                      self._mh.fromhere())        
        
        if (data.has_key('id')):
        
            db = self._get_db()            
            address = db.read_address(data.id)
            db.disconnect()
            
            if (address != None):
                return address.tojson()
            else:
                return NotFound                        
        
        else:
            return BadRequest()
        
    def create_address(self, data): 
        """Method handles POST address           
           
        Args:
           data (json): address detail  
             
        Returns:
           http: HTTP 200 with id of created address,
                 HTTP 400 when address not created
           
        Example:
        
        .. code-block:: javascript
        
           {
             "street": "Tomickova",
             "street_no": "2144/1"
             "city": "Praha",
             "zip": 14800
           }                    
                
        """            
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_request', 'create_address', data), 
                      self._mh.fromhere())        
        
        doc = read(data)
        street = doc['street'] if doc.has_key('street') else None
        street_no = doc['street_no'] if doc.has_key('street_no') else None
        city = doc['city'] if doc.has_key('city') else None
        zip = doc['zip'] if doc.has_key('zip') else None
        
        db = self._get_db()
        id = db.create_address(street, street_no, city, zip)
        db.disconnect()
        
        if (id != None):
            return id
        else:
            return BadRequest()
        
    def change_address(self, data):   
        """Method handles PUT address           
           
        Args:
           data (json): address detail  
             
        Returns:
           http: HTTP 200 when address changed,
                 HTTP 400 when address not changed
           
        Example:
        
        .. code-block:: javascript   
           
           {
             "id": 1,
             "street": "Tomickova",
             "street_no": "2144/1"
             "city": "Praha",
             "zip": 14800
           }            
                
        """           
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_request', 'change_address', data), 
                      self._mh.fromhere())        
        
        doc = read(data)
        id = doc['id'] if doc.has_key('id') else None
        street = doc['street'] if doc.has_key('street') else None
        street_no = doc['street_no'] if doc.has_key('street_no') else None
        city = doc['city'] if doc.has_key('city') else None
        zip = doc['zip'] if doc.has_key('zip') else None
        
        db = self._get_db()
        res = db.change_address(id, street, street_no, city, zip)
        db.disconnect()
        
        if (res):
            return OK()
        else:
            return BadRequest()                     
        
    def assign_address_role(self, data): 
        """Method handles POST address/role           
           
        Args:
           data (json): address role detail  
             
        Returns:
           http: HTTP 200 when address role assigned,
                 HTTP 400 when address role not assigned
           
        Example:
        
        .. code-block:: javascript
        
          {
             "id": 1,
             "title": "contract",
             "contact": 1,
             "customer": 1,
             "payer": 1,
             "subscriber": 1
           }         
                
        """              
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_request', 'assign_address_role', data), 
                      self._mh.fromhere())        
        
        doc = read(data)
        id = doc['id'] if doc.has_key('id') else None
        role = doc['title'] if doc.has_key('title') else None
        contact = doc['contact'] if doc.has_key('contact') else None
        customer = doc['customer'] if doc.has_key('customer') else None
        payer = doc['payer'] if doc.has_key('payer') else None
        subscriber = doc['subscriber'] if doc.has_key('subscriber') else None
        
        db = self._get_db()
        res = db.assign_address_role(id, role, contact, customer, payer, subscriber)
        db.disconnect()
        
        if (res):
            return OK()
        else:
            return BadRequest()      
        
    def revoke_address_role(self, data):
        """Method handles PUT address/role           
           
        Args:
           data (json): address role detail  
             
        Returns:
           http: HTTP 200 when address role revoked,
                 HTTP 400 when address role not revoked
           
        Example:
        
        .. code-block:: javascript
        
          {
             "id": 1,
             "title": "contract",
             "contact": 1,
             "customer": 1,
             "payer": 1,
             "subscriber": 1
           }         
                
        """               
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_request', 'revoke_address_role', data), 
                      self._mh.fromhere())        
        
        doc = read(data)
        id = doc['id'] if doc.has_key('id') else None
        role = doc['title'] if doc.has_key('title') else None
        contact = doc['contact'] if doc.has_key('contact') else None
        customer = doc['customer'] if doc.has_key('customer') else None
        payer = doc['payer'] if doc.has_key('payer') else None
        subscriber = doc['subscriber'] if doc.has_key('subscriber') else None
        
        db = self._get_db()
        res = db.revoke_address_role(id, role, contact, customer, payer, subscriber)
        db.disconnect()
        
        if (res):
            return OK()
        else:
            return BadRequest() 
        
    def read_services(self, data):  
        """Method handles GET service           
           
        Args:
           data (dict): request input entity and service id (all services if empty), choice customer|payer|subscriber, 
             
        Returns:
           http: HTTP 200 with list of services in JSON,
                 HTTP 404 when service not found,
                 HTTP 400 when no entity is provided 
           
        Example:
        
        .. code-block:: javascript
        
           {
             "service": 
             {
               "service": 
               [
                 {
                   "id": 615,
                   "name": "Telefonni cislo",
                   "status": "active",
                   "params": 
                   {
                     "entry": 
                     [
                       {
                         "key": 121,
                         "value": "12345"
                       }
                     ]
                   } 
                 }  
               ]
             } 
           }         
                
        """          
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_request', 'read_services', data), 
                      self._mh.fromhere())               
        
        customer = data['customer'] if data.has_key('customer') else None
        payer = data['payer'] if data.has_key('payer') else None
        subscriber = data['subscriber'] if data.has_key('subscriber') else None
        service = data['service'] if data.has_key('service') else None
        
        if (customer == None and payer == None and subscriber == None):
            return BadRequest()
        
        db = self._get_db()            
        srv_list = db.read_services(customer, payer, subscriber, service)
        db.disconnect()
            
        if (len(srv_list) > 0):
            
            root = {}
            
            services = []                                            
            for service in srv_list:  
                el_service = {'id': service.id, 'name': service.name, 'status': service.status}
                
                el_params = []             
                for key, value in service.params.items():  
                    el_params.append({'key': key, 'value': value}) 
                
                el_service['params'] = {'entry' : el_params} 
                services.append(el_service)                            
            
            root['services'] = {'service': services}
            
            return write(root)
            
        else:
            return NotFound    
        
    def create_service(self, data):
        """Method handles POST service           
           
        Args:
           data (json): service operation, choice customer|payer|subscriber  
           
        Returns:
           http: HTTP 200 when service created,
                 HTTP 400 when service not created           
           
        Example:
        
        .. code-block:: javascript
        
           {
             "customer": 1,
             "payer": 1,
             "subscriber": 1,
             "service": 615,
             "status": "active",
             "params": 
             {
               "entry": 
               [
                 {
                   "key": 121,
                   "value": "12345"
                 }
               ]
             } 
           }             
                
        """  
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_request', 'create_service', data), 
                      self._mh.fromhere())                  
        
        doc = read(data)
        customer = doc['customer'] if doc.has_key('customer') else None
        payer = doc['payer'] if doc.has_key('payer') else None
        subscriber = doc['subscriber'] if doc.has_key('subscriber') else None
        service = doc['service'] if doc.has_key('service') else None
        status = doc['status'] if doc.has_key('status') else 'active' 
        
        params = {}
        for param in doc['params']['entry']:
            params[param['key']] = param['value']
            
        db = self._get_db()
        res = db.create_service(service, customer, payer, subscriber, status, params)
        db.disconnect()
        
        if (res):
            return OK()
        else:
            return BadRequest()      
        
    def change_service(self, data):
        """Method handles PUT service           
           
        Args:
           data (json): service operation, choice customer|payer|subscriber  
             
        Returns:
           http: HTTP 200 when service changed,
                 HTTP 400 when service not changed
           
        Example:
        
        .. code-block:: javascript
        
           {
             "customer": 1,
             "payer": 1,
             "subscriber": 1,
             "service": 615,
             "status": "active",
             "params": 
             {
               "entry": 
               [
                 {
                   "key": 121,
                   "value": "12345"
                 }
               ]
             } 
           }          
                
        """  
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_request', 'change_service', data), 
                      self._mh.fromhere())                
        
        doc = read(data)
        customer = doc['customer'] if doc.has_key('customer') else None
        payer = doc['payer'] if doc.has_key('payer') else None
        subscriber = doc['subscriber'] if doc.has_key('subscriber') else None
        service = doc['service'] if doc.has_key('service') else None
        status = doc['status'] if doc.has_key('status') else None 
        
        params = {}
        for param in doc['params']['entry']:
            params[param['key']] = param['value']
            
        db = self._get_db()
        res = db.change_service(service, customer, payer, subscriber, status, params)
        db.disconnect()
        
        if (res):
            return OK()
        else:
            return BadRequest()                                                                           