# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.extensions.testenv.application.rest_handler
   :platform: Unix
   :synopsis: Handles REST operations
.. moduleauthor:: Petr Rašek <pr@hydratk.org>

"""
import hydratk.extensions.testenv.interfaces.db_int as db_int; 
import web;
import jsonlib2;

class REST_handler:
    
    _mh = None;
    
    def __init__(self, _mh):
        
        self._mh = _mh;

    def _get_db(self):    
    
        db = db_int.DB_INT(self._mh);
        db.connect();
        return db;

    def read_customer(self, data):
        """Method handles GET customer           
           
        Args:
           id - URL param, int   
             
        Returns:
           HTTP 200 with crm_entities.Customer in JSON
           HTTP 404 when customer not found
           HTTP 400 when param id is missing 
                
        """             
        
        if (data.has_key('id')):
        
            db = self._get_db();            
            customer = db.read_customer(data.id);
            db.disconnect();
            
            if (customer != None):
                return customer.tojson();
            else:
                return web.NotFound;                        
        
        else:
            return web.BadRequest();
        
    def create_customer(self, data):   
        """Method handles POST customer           
           
        Args:
           customer - crm_entities.Customer in JSON  
           {
             "name": "Charlie Bowman",
             "status": "active",
             "segment": 2,
             "birth_no": "700101/0001",
             "reg_no": "123456",
             "tax_no": "CZ123456"
           } 
             
        Returns:
           HTTP 200 with id of created customer
           HTTP 400 when customer not created
                
        """              
        
        doc = jsonlib2.read(data);
        name = doc['name'] if doc.has_key('name') else None;
        status = doc['status'] if doc.has_key('status') else 'active';
        segment = doc['segment'] if doc.has_key('segment') else None;
        birth_no = doc['birth_no'] if doc.has_key('birth_no') else None;
        reg_no = doc['reg_no'] if doc.has_key('reg_no') else None;
        tax_no = doc['tax_no'] if doc.has_key('tax_no') else None;
        
        db = self._get_db();
        id = db.create_customer(name, segment, status, birth_no, reg_no, tax_no);
        db.disconnect();
        
        if (id != None):
            return id;
        else:
            return web.BadRequest();
        
    def change_customer(self, data):  
        """Method handles PUT customer           
           
        Args:
           customer - crm_entities.Customer in JSON  
             
        Returns:
           HTTP 200 when customer changed
           HTTP 400 when customer not changed
                
        """           
        
        doc = jsonlib2.read(data);
        id = doc['id'] if doc.has_key('id') else None;
        name = doc['name'] if doc.has_key('name') else None;
        status = doc['status'] if doc.has_key('status') else None;
        segment = doc['segment'] if doc.has_key('segment') else None;
        birth_no = doc['birth_no'] if doc.has_key('birth_no') else None;
        reg_no = doc['reg_no'] if doc.has_key('reg_no') else None;
        tax_no = doc['tax_no'] if doc.has_key('tax_no') else None;
        
        db = self._get_db();
        res = db.change_customer(id, name, status, segment, birth_no, reg_no, tax_no);
        db.disconnect();
        
        if (res):
            return web.OK();
        else:
            return web.BadRequest();       
        
    def read_payer(self, data):  
        """Method handles GET payer           
           
        Args:
           id - URL param, int   
             
        Returns:
           HTTP 200 with crm_entities.Payer in JSON
           HTTP 404 when payer not found
           HTTP 400 when param id is missing 
                
        """             
        
        if (data.has_key('id')):
        
            db = self._get_db();            
            payer = db.read_payer(data.id);
            db.disconnect();
            
            if (payer != None):
                return payer.tojson();
            else:
                return web.NotFound;                        
        
        else:
            return web.BadRequest();
        
    def create_payer(self, data): 
        """Method handles POST payer           
           
        Args:
           payer - crm_entities.Payer in JSON  
           {
             "name": "Charlie Bowman",
             "status": "active",
             "billcycle": 1,
             "bank_account": "123456/0100",
             "customer": 1
           } 
             
        Returns:
           HTTP 200 with id of created payer
           HTTP 400 when payer not created
                
        """            
        
        doc = jsonlib2.read(data);
        name = doc['name'] if doc.has_key('name') else None;
        status = doc['status'] if doc.has_key('status') else 'active';
        billcycle = doc['billcycle'] if doc.has_key('billcycle') else None;
        bank_account = doc['bank_account'] if doc.has_key('bank_account') else None;
        customer = doc['customer'] if doc.has_key('customer') else None;
        
        db = self._get_db();
        id = db.create_payer(name, billcycle, customer, status, bank_account);
        db.disconnect();
        
        if (id != None):
            return id;
        else:
            return web.BadRequest();
        
    def change_payer(self, data): 
        """Method handles PUT payer           
           
        Args:
           payer - crm_entities.Payer in JSON  
             
        Returns:
           HTTP 200 when payer changed
           HTTP 400 when payer not changed
                
        """             
        
        doc = jsonlib2.read(data);
        id = doc['id'] if doc.has_key('id') else None;
        name = doc['name'] if doc.has_key('name') else None;
        status = doc['status'] if doc.has_key('status') else None;
        billcycle = doc['billcycle'] if doc.has_key('billcycle') else None;
        bank_account = doc['bank_account'] if doc.has_key('bank_account') else None;
        customer = doc['customer'] if doc.has_key('customer') else None;
        
        db = self._get_db();
        res = db.change_payer(id, name, status, billcycle, bank_account, customer);
        db.disconnect();
        
        if (res):
            return web.OK();
        else:
            return web.BadRequest(); 
        
    def read_subscriber(self, data):  
        """Method handles GET subscriber           
           
        Args:
           id - URL param, int   
             
        Returns:
           HTTP 200 with crm_entities.Subscriber in JSON
           HTTP 404 when subscriber not found
           HTTP 400 when param id is missing 
                
        """             
        
        if (data.has_key('id')):
        
            db = self._get_db();            
            subscriber = db.read_subscriber(data.id);
            db.disconnect();
            
            if (subscriber != None):
                return subscriber.tojson();
            else:
                return web.NotFound;                        
        
        else:
            return web.BadRequest();
        
    def create_subscriber(self, data):
        """Method handles POST subscriber           
           
        Args:
           payer - crm_entities.Subscriber in JSON  
           {
             "name": "Charlie Bowman",
             "msisdn": "123456"
             "status": "active",
             "market": 1,
             "tariff": 433,
             "customer": 1,
             "payer": 2
           } 
             
        Returns:
           HTTP 200 with id of created subscriber
           HTTP 400 when subscriber not created
                
        """                 
        
        doc = jsonlib2.read(data);
        name = doc['name'] if doc.has_key('name') else None;
        msisdn = doc['msisdn'] if doc.has_key('msisdn') else None;
        status = doc['status'] if doc.has_key('status') else 'active';
        market = doc['market'] if doc.has_key('market') else None;
        tariff = doc['tariff'] if doc.has_key('tariff') else None;
        customer = doc['customer'] if doc.has_key('customer') else None;
        payer = doc['payer'] if doc.has_key('payer') else None;
        
        db = self._get_db();
        id = db.create_subscriber(name, msisdn, market, tariff, customer, payer, status);
        db.disconnect();
        
        if (id != None):
            return id;
        else:
            return web.BadRequest();
        
    def change_subscriber(self, data):  
        """Method handles PUT subscriber           
           
        Args:
           subscriber - crm_entities.Subscriber in JSON  
             
        Returns:
           HTTP 200 when subscriber changed
           HTTP 400 when subscriber not changed
                
        """            
        
        doc = jsonlib2.read(data);
        id = doc['id'] if doc.has_key('id') else None;
        name = doc['name'] if doc.has_key('name') else None;
        msisdn = doc['msisdn'] if doc.has_key('msisdn') else None;
        status = doc['status'] if doc.has_key('status') else None;
        market = doc['market'] if doc.has_key('market') else None;
        tariff = doc['tariff'] if doc.has_key('tariff') else None;
        customer = doc['customer'] if doc.has_key('customer') else None;
        payer = doc['payer'] if doc.has_key('payer') else None;
        
        db = self._get_db();
        res = db.change_subscriber(id, name, msisdn, status, market, tariff, customer, payer);
        db.disconnect();
        
        if (res):
            return web.OK();
        else:
            return web.BadRequest();  
        
    def read_contact(self, data):  
        """Method handles GET contact           
           
        Args:
           id - URL param, int   
             
        Returns:
           HTTP 200 with crm_entities.Contact in JSON
           HTTP 404 when contact not found
           HTTP 400 when param id is missing 
                
        """             
        
        if (data.has_key('id')):
        
            db = self._get_db();            
            contact = db.read_contact(data.id);
            db.disconnect();
            
            if (contact != None):
                return contact.tojson();
            else:
                return web.NotFound;                        
        
        else:
            return web.BadRequest();
        
    def create_contact(self, data):  
        """Method handles POST contact           
           
        Args:
           payer - crm_entities.Contact in JSON  
           {
             "name": "Charlie Bowman",
             "phone": "123456"
             "email": "aaa@xxx.com"
           } 
             
        Returns:
           HTTP 200 with id of created contact
           HTTP 400 when contact not created
                
        """           
        
        doc = jsonlib2.read(data);
        name = doc['name'] if doc.has_key('name') else None;
        phone = doc['phone'] if doc.has_key('phone') else None;
        email = doc['email'] if doc.has_key('email') else None;
        
        db = self._get_db();
        id = db.create_contact(name, phone, email);
        db.disconnect();
        
        if (id != None):
            return id;
        else:
            return web.BadRequest();
        
    def change_contact(self, data):  
        """Method handles PUT customer           
           
        Args:
           contact - crm_entities.Contact in JSON  
             
        Returns:
           HTTP 200 when contact changed
           HTTP 400 when contact not changed
                
        """            
        
        doc = jsonlib2.read(data);
        id = doc['id'] if doc.has_key('id') else None;
        name = doc['name'] if doc.has_key('name') else None;
        phone = doc['phone'] if doc.has_key('phone') else None;
        email = doc['email'] if doc.has_key('email') else None;
        
        db = self._get_db();
        res = db.change_contact(id, name, phone, email);
        db.disconnect();
        
        if (res):
            return web.OK();
        else:
            return web.BadRequest();                     
        
    def assign_contact_role(self, data):   
        """Method handles POST contact/role           
           
        Args:
           contact_role - crm_entities.ContactRole in JSON  
           {
             "id": 1,
             "title": "contract",
             "customer": 1,
             "payer": 1,
             "subscriber": 1
           } 
             
        Returns:
           HTTP 200 when contact role assigned
           HTTP 400 when customer role not assigned
                
        """           
        
        doc = jsonlib2.read(data);
        id = doc['id'] if doc.has_key('id') else None;
        role = doc['title'] if doc.has_key('title') else None;
        customer = doc['customer'] if doc.has_key('customer') else None;
        payer = doc['payer'] if doc.has_key('payer') else None;
        subscriber = doc['subscriber'] if doc.has_key('subscriber') else None
        
        db = self._get_db();
        res = db.assign_contact_role(id, role, customer, payer, subscriber);
        db.disconnect();
        
        if (res):
            return web.OK();
        else:
            return web.BadRequest();      
        
    def revoke_contact_role(self, data): 
        """Method handles PUT contact/role           
           
        Args:
           contact_role - crm_entities.ContactRole in JSON  
           {
             "id": 1,
             "title": "contract",
             "customer": 1,
             "payer": 1,
             "subscriber": 1
           } 
             
        Returns:
           HTTP 200 when contact role revoked
           HTTP 400 when customer role not revoked
                
        """              
        
        doc = jsonlib2.read(data);
        id = doc['id'] if doc.has_key('id') else None;
        role = doc['title'] if doc.has_key('title') else None;
        customer = doc['customer'] if doc.has_key('customer') else None;
        payer = doc['payer'] if doc.has_key('payer') else None;
        subscriber = doc['subscriber'] if doc.has_key('subscriber') else None
        
        db = self._get_db();
        res = db.revoke_contact_role(id, role, customer, payer, subscriber);
        db.disconnect();
        
        if (res):
            return web.OK();
        else:
            return web.BadRequest();      
        
    def read_address(self, data):  
        """Method handles GET address           
           
        Args:
           id - URL param, int   
             
        Returns:
           HTTP 200 with crm_entities.Address in JSON
           HTTP 404 when address not found
           HTTP 400 when param id is missing 
                
        """             
        
        if (data.has_key('id')):
        
            db = self._get_db();            
            address = db.read_address(data.id);
            db.disconnect();
            
            if (address != None):
                return address.tojson();
            else:
                return web.NotFound;                        
        
        else:
            return web.BadRequest();
        
    def create_address(self, data): 
        """Method handles POST address           
           
        Args:
           payer - crm_entities.Address in JSON  
           {
             "street": "Tomickova",
             "street_no": "2144/1"
             "city": "Praha",
             "zip": 14800
           } 
             
        Returns:
           HTTP 200 with id of created address
           HTTP 400 when address not created
                
        """            
        
        doc = jsonlib2.read(data);
        street = doc['street'] if doc.has_key('street') else None;
        street_no = doc['street_no'] if doc.has_key('street_no') else None;
        city = doc['city'] if doc.has_key('city') else None;
        zip = doc['zip'] if doc.has_key('zip') else None;
        
        db = self._get_db();
        id = db.create_address(street, street_no, city, zip);
        db.disconnect();
        
        if (id != None):
            return id;
        else:
            return web.BadRequest();
        
    def change_address(self, data):   
        """Method handles PUT address           
           
        Args:
           address - crm_entities.Address in JSON  
             
        Returns:
           HTTP 200 when address changed
           HTTP 400 when address not changed
                
        """           
        
        doc = jsonlib2.read(data);
        id = doc['id'] if doc.has_key('id') else None;
        street = doc['street'] if doc.has_key('street') else None;
        street_no = doc['street_no'] if doc.has_key('street_no') else None;
        city = doc['city'] if doc.has_key('city') else None;
        zip = doc['zip'] if doc.has_key('zip') else None;
        
        db = self._get_db();
        res = db.change_address(id, street, street_no, city, zip);
        db.disconnect();
        
        if (res):
            return web.OK();
        else:
            return web.BadRequest();                     
        
    def assign_address_role(self, data): 
        """Method handles POST address/role           
           
        Args:
           address_role - crm_entities.AddressRole in JSON  
           {
             "id": 1,
             "title": "contract",
             "contact": 1,
             "customer": 1,
             "payer": 1,
             "subscriber": 1
           } 
             
        Returns:
           HTTP 200 when address role assigned
           HTTP 400 when address role not assigned
                
        """              
        
        doc = jsonlib2.read(data);
        id = doc['id'] if doc.has_key('id') else None;
        role = doc['title'] if doc.has_key('title') else None;
        contact = doc['contact'] if doc.has_key('contact') else None;
        customer = doc['customer'] if doc.has_key('customer') else None;
        payer = doc['payer'] if doc.has_key('payer') else None;
        subscriber = doc['subscriber'] if doc.has_key('subscriber') else None
        
        db = self._get_db();
        res = db.assign_address_role(id, role, contact, customer, payer, subscriber);
        db.disconnect();
        
        if (res):
            return web.OK();
        else:
            return web.BadRequest();      
        
    def revoke_address_role(self, data):
        """Method handles PUT address/role           
           
        Args:
           address_role - crm_entities.AddressRole in JSON  
           {
             "id": 1,
             "title": "contract",
             "contact": 1,
             "customer": 1,
             "payer": 1,
             "subscriber": 1
           } 
             
        Returns:
           HTTP 200 when address role revoked
           HTTP 400 when address role not revoked
                
        """               
        
        doc = jsonlib2.read(data);
        id = doc['id'] if doc.has_key('id') else None;
        role = doc['title'] if doc.has_key('title') else None;
        contact = doc['contact'] if doc.has_key('contact') else None;
        customer = doc['customer'] if doc.has_key('customer') else None;
        payer = doc['payer'] if doc.has_key('payer') else None;
        subscriber = doc['subscriber'] if doc.has_key('subscriber') else None
        
        db = self._get_db();
        res = db.revoke_address_role(id, role, contact, customer, payer, subscriber);
        db.disconnect();
        
        if (res):
            return web.OK();
        else:
            return web.BadRequest(); 
        
    def read_services(self, data):  
        """Method handles GET service           
           
        Args:
           customer - URL param, int
           payer - URL param, int
           subscriber - URL param, int
           service - URL param, int   
             
        Returns:
           HTTP 200 with list of crm_entities.Service in JSON
           HTTP 404 when service not found
           HTTP 400 when no entity is provided 
                
        """                 
        
        customer = data['customer'] if data.has_key('customer') else None;
        payer = data['payer'] if data.has_key('payer') else None;
        subscriber = data['subscriber'] if data.has_key('subscriber') else None;
        service = data['service'] if data.has_key('service') else None;
        
        if (customer == None and payer == None and subscriber == None):
            return web.BadRequest();
        
        db = self._get_db();            
        srv_list = db.read_services(customer, payer, subscriber, service);
        db.disconnect();
            
        if (len(srv_list) > 0):
            
            root = {};
            
            services = [];                                            
            for service in srv_list:  
                el_service = {'id': service.id, 'name': service.name, 'status': service.status};
                
                el_params = [];             
                for key, value in service.params.items():  
                    el_params.append({'key': key, 'value': value}); 
                
                el_service['params'] = {'entry' : el_params}; 
                services.append(el_service);                            
            
            root['services'] = {'service': services};
            
            return jsonlib2.write(root);
            
        else:
            return web.NotFound;    
        
    def create_service(self, data):
        """Method handles POST service           
           
        Args:
           service - crm_entities.ServiceOperation in JSON  
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
             
        Returns:
           HTTP 200 when service created
           HTTP 400 when service not created
                
        """            
        
        doc = jsonlib2.read(data);
        customer = doc['customer'] if doc.has_key('customer') else None;
        payer = doc['payer'] if doc.has_key('payer') else None;
        subscriber = doc['subscriber'] if doc.has_key('subscriber') else None;
        service = doc['service'] if doc.has_key('service') else None;
        status = doc['status'] if doc.has_key('status') else 'active'; 
        
        params = {};
        for param in doc['params']['entry']:
            params[param['key']] = param['value'];
            
        db = self._get_db();
        res = db.create_service(service, customer, payer, subscriber, status, params);
        db.disconnect();
        
        if (res):
            return web.OK();
        else:
            return web.BadRequest();      
        
    def change_service(self, data):
        """Method handles PUT service           
           
        Args:
           service - crm_entities.ServiceOperation in JSON  
             
        Returns:
           HTTP 200 when service changed
           HTTP 400 when service not changed
                
        """          
        
        doc = jsonlib2.read(data);
        customer = doc['customer'] if doc.has_key('customer') else None;
        payer = doc['payer'] if doc.has_key('payer') else None;
        subscriber = doc['subscriber'] if doc.has_key('subscriber') else None;
        service = doc['service'] if doc.has_key('service') else None;
        status = doc['status'] if doc.has_key('status') else None; 
        
        params = {};
        for param in doc['params']['entry']:
            params[param['key']] = param['value'];
            
        db = self._get_db();
        res = db.change_service(service, customer, payer, subscriber, status, params);
        db.disconnect();
        
        if (res):
            return web.OK();
        else:
            return web.BadRequest();                                                                           