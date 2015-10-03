# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.extensions.testenv.interfaces.rest_int
   :platform: Unix
   :synopsis: REST interface for testenv
.. moduleauthor:: Petr Rašek <pr@hydratk.org>

"""

import hydratk.extensions.testenv.entities.crm_entities as crm;
import httplib2;
import urllib;
import jsonlib2;

class REST_INT():
    
    _mh = None;    
    
    def __init__(self, _mh):
        
        self._mh = _mh; 
        self.ip = self._mh.cfg['Extensions']['TestEnv']['server_ip'];
        self.port = self._mh.cfg['Extensions']['TestEnv']['server_port'];  
        self.url = 'http://{0}:{1}/rs/'.format(self.ip, self.port);
        self.client = httplib2.Http();            
        
    def read_customer(self, id):
        """Method reads customer
        
        Args:
           id - int, mandatory            
             
        Returns:
           customer - crm_entities.Customer
                
        """        
        
        self._mh.dmsg('htk_on_debug_info', 'params - id:{0}'.format(id), self._mh.fromhere());
        
        path = 'customer';
        params = {'id' : id};
        url = self.url + path + '?' + urllib.urlencode(params);
        headers = {'Accept' : 'application/json'};
        response, content = self.client.request(url, method='GET', headers=headers);

        if (response.status == 200):
            
            doc = jsonlib2.read(content);
            customer = crm.Customer(doc['id'], doc['name'], doc['status'], doc['segment'], 
                                    doc['birth_no'], doc['reg_no'], doc['tax_no']);
            self._mh.dmsg('htk_on_debug_info', 'customer - {0}'.format(customer), self._mh.fromhere());
                
            return customer;
            
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(response.status, content), self._mh.fromhere());
            return None;
        
    def create_customer(self, name, segment, status='active', birth_no=None, reg_no=None, tax_no=None):
        """Method creates customer
        
        Args:
           name - string, mandatory
           segment - int, mandatory, lov_segment.id
           status - string, optional, lov_status.title, default active
           birth_no - string, optional
           reg_no - string, optional
           tax_no - string, optional              
             
        Returns:
           id - int
                
        """           
        
        msg = 'params - name:{0}, status:{1}, segment:{2}, birth_no:{3}, reg_no:{4}, tax_no:{5}';
        self._mh.dmsg('htk_on_debug_info', msg.format(name, status, segment, birth_no, reg_no, tax_no), self._mh.fromhere());        
        
        path = 'customer';
        url = self.url + path;
        headers = {'Content-Type' : 'application/json'};        
        customer = crm.Customer(None, name, status, segment, birth_no, reg_no, tax_no);                        
        body = customer.tojson();         
        response, content = self.client.request(url, method='POST', headers=headers, body=body);              

        if (response.status == 200):
            self._mh.dmsg('htk_on_debug_info', 'customer {0} created'.format(content), self._mh.fromhere());
            return content;
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(response.status, content), self._mh.fromhere());
            return None;   
        
    def change_customer(self, id, name=None, status=None, segment=None, birth_no=None, reg_no=None, tax_no=None):
        """Method changes customer
        
        Args:
           id - int, mandatory
           name - string, optional
           status - string, optional, lov_status.title
           segment - int, optional, lov_segment.id           
           birth_no - string, optional
           reg_no - string, optional
           tax_no - string, optional              
             
        Returns:
           result - bool
                
        """  
        
        msg = 'params - id:{0}, name:{1}, status:{2}, segment:{3}, birth_no:{4}, reg_no:{5}, tax_no:{6}';
        self._mh.dmsg('htk_on_debug_info', msg.format(id, name, status, segment, birth_no, reg_no, tax_no), self._mh.fromhere());         
               
        path = 'customer';
        url = self.url + path;
        headers = {'Content-Type' : 'application/json'}        
        customer = crm.Customer(id, name, status, segment, birth_no, reg_no, tax_no);
        body = customer.tojson();
        response, content = self.client.request(url, method='PUT', headers=headers, body=body);              

        if (response.status == 200):
            self._mh.dmsg('htk_on_debug_info', 'customer changed', self._mh.fromhere());
            return True;
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(response.status, content), self._mh.fromhere());
            return False;   
        
    def read_payer(self, id):
        """Method reads payer
        
        Args:
           id - int, mandatory           
             
        Returns:
           payer - crm_entities.Payer
                
        """           
        
        self._mh.dmsg('htk_on_debug_info', 'params - id:{0}'.format(id), self._mh.fromhere());
        
        path = 'payer';
        params = {'id' : id};
        url = self.url + path + '?' + urllib.urlencode(params);
        headers = {'Accept' : 'application/json'};
        response, content = self.client.request(url, method='GET', headers=headers);

        if (response.status == 200):
            
            doc = jsonlib2.read(content);
            payer = crm.Payer(doc['id'], doc['name'], doc['status'], doc['billcycle'], 
                              doc['customer'], doc['bank_account']);
            self._mh.dmsg('htk_on_debug_info', 'payer - {0}'.format(payer), self._mh.fromhere());                              
                
            return payer;
            
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(response.status, content), self._mh.fromhere());
            return None; 
        
    def create_payer(self, name, billcycle, customer, status='active', bank_account=None):
        """Method creates payer
        
        Args:
           name - string, mandatory
           billcycle - int, mandatory, lov_billcycle.id
           customer - int, mandatory
           status - string, optional, lov_status.title, default active
           bank_account - string, optional            
             
        Returns:
           id - int
                
        """  
        
        msg = 'params - name:{0}, status:{1}, billcycle:{2}, bank_account:{3}, customer:{4}';
        self._mh.dmsg('htk_on_debug_info', msg.format(name, status, billcycle, bank_account, customer), self._mh.fromhere());                
        
        path = 'payer';
        url = self.url + path;
        headers = {'Content-Type' : 'application/json'};
        payer = crm.Payer(None, name, status, billcycle, customer, bank_account);
        body = payer.tojson();
        response, content = self.client.request(url, method='POST', headers=headers, body=body);              

        if (response.status == 200):
            self._mh.dmsg('htk_on_debug_info', 'payer {0} created'.format(content), self._mh.fromhere());
            return content;
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(response.status, content), self._mh.fromhere());
            return None   
        
    def change_payer(self, id, name=None, status=None, billcycle=None, bank_account=None, customer=None):
        """Method changes payer
        
        Args:
           id - int, mandatory
           name - string, optional
           status - string, optional, lov_status.title
           billcycle - int, optional, lov_billcycle.id
           bank_account - string, optional 
           customer - int, optional                               
             
        Returns:
           result - bool
                
        """ 
        
        msg = 'params - id:{0}, name:{1}, status:{2}, billcycle:{3}, bank_account:{4}, customer:{5}';
        self._mh.dmsg('htk_on_debug_info', msg.format(id, name, status, billcycle, bank_account, customer), self._mh.fromhere());                
        
        path = 'payer';
        url = self.url + path;        
        headers = {'Content-Type' : 'application/json'};
        payer = crm.Payer(id, name, status, billcycle, customer, bank_account);
        body = payer.tojson();        
        response, content = self.client.request(url, method='PUT', headers=headers, body=body);              

        if (response.status == 200):
            self._mh.dmsg('htk_on_debug_info', 'payer changed', self._mh.fromhere());
            return True;
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(response.status, content), self._mh.fromhere());
            return False;  
        
    def read_subscriber(self, id):
        """Method reads subscriber
        
        Args:
           id - int, mandatory            
             
        Returns:
           subscriber - crm_entities.Subscriber
                
        """           
        
        self._mh.dmsg('htk_on_debug_info', 'params - id:{0}'.format(id), self._mh.fromhere());
        
        path = 'subscriber';
        params = {'id' : id};
        url = self.url + path + '?' + urllib.urlencode(params);
        headers = {'Accept' : 'application/json'};
        response, content = self.client.request(url, method='GET', headers=headers);

        if (response.status == 200):
            
            doc = jsonlib2.read(content);
            subscriber = crm.Subscriber(doc['id'], doc['name'], doc['msisdn'], doc['status'], doc['market'], 
                                        doc['tariff'], doc['customer'], doc['payer']);
            self._mh.dmsg('htk_on_debug_info', 'subscriber - {0}'.format(subscriber), self._mh.fromhere());                                        
                
            return subscriber;
            
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(response.status, content), self._mh.fromhere());
            return None;  
        
    def create_subscriber(self, name, msisdn, market, tariff, customer, payer, status='active'):
        """Method creates subscriber
        
        Args:
           name - string, mandatory
           msisdn - string, mandatory
           market - int, mandatory, lov_market.id
           tariff - int, mandatory, lov_tariff.id
           customer - int, mandatory
           payer - int, mandatory
           status - string, optional, lov_status.title, default active                              
             
        Returns:
           id - int
                
        """     
        
        msg = 'params - name:{0}, msisdn:{1}, status:{2}, market:{3}, tariff:{4}, customer:{5}, payer:{6}';
        self._mh.dmsg('htk_on_debug_info', msg.format(name, msisdn, status, market, tariff, customer, payer), self._mh.fromhere());              
        
        path = 'subscriber';
        url = self.url + path;
        headers = {'Content-Type' : 'application/json'};
        subscriber = crm.Subscriber(None, name, msisdn, status, market, tariff, customer, payer);
        body = subscriber.tojson();
        response, content = self.client.request(url, method='POST', headers=headers, body=body);              

        if (response.status == 200):
            self._mh.dmsg('htk_on_debug_info', 'subscriber {0} created'.format(content), self._mh.fromhere());
            return content;
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(response.status, content), self._mh.fromhere());
            return None;  
        
    def change_subscriber(self, id, name=None, msisdn=None, status=None, market=None, tariff=None, customer=None, payer=None):
        """Method changes subscriber
        
        Args:
           id - int, mandatory
           name - string, optional
           msisdn - string, optional
           status - string, optional, lov_status.title           
           market - int, optional, lov_market.id
           tariff - int, optional, lov_tariff.id
           customer - int, optional
           payer - int, optional                                    
             
        Returns:
           result - bool
        
        """  
        
        msg = 'params - id:{0}, name:{1}, msisdn:{2}, status:{3}, market:{4}, tariff:{5}, customer:{6}, payer:{7}';
        self._mh.dmsg('htk_on_debug_info', msg.format(id, name, msisdn, status, market, tariff, customer, payer), self._mh.fromhere());                   
        
        path = 'subscriber';
        url = self.url + path;
        headers = {'Content-Type' : 'application/json'};
        subscriber = crm.Subscriber(id, name, msisdn, status, market, tariff, customer, payer);
        body = subscriber.tojson();
        response, content = self.client.request(url, method='PUT', headers=headers, body=body);              

        if (response.status == 200):
            self._mh.dmsg('htk_on_debug_info', 'subscriber changed', self._mh.fromhere());
            return True;
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(response.status, content), self._mh.fromhere());
            return False;  
        
    def read_contact(self, id):
        """Method reads contact
        
        Args:
           id - int           
             
        Returns:
           contact - crm_entities.Contact
                
        """           
        
        self._mh.dmsg('htk_on_debug_info', 'params - id:{0}'.format(id), self._mh.fromhere());
        
        path = 'contact';
        params = {'id' : id};
        url = self.url + path + '?' + urllib.urlencode(params);
        headers = {'Accept' : 'application/json'};
        response, content = self.client.request(url, method='GET', headers=headers);

        if (response.status == 200):
            
            doc = jsonlib2.read(content);
            roles = [];
            if (doc.has_key('roles')):                    
                for role in doc['roles']['role']:
                    roles.append(crm.ContactRole(role['id'], role['title'], role['customer'],
                                                 role['payer'], role['subscriber']));
                
            contact = crm.Contact(doc['id'], doc['name'], doc['phone'], doc['email'], roles);
            self._mh.dmsg('htk_on_debug_info', 'contact - {0}'.format(contact), self._mh.fromhere());
                
            return contact;
            
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(response.status, content), self._mh.fromhere());
            return None;   
        
    def create_contact(self, name, phone=None, email=None):
        """Method creates contact
        
        Args:
           name - string, mandatory
           phone - string, optional
           email - string, optional          
             
        Returns:
           id - int
                
        """    
        
        msg = 'params - name:{0}, phone:{1}, email:{2}';
        self._mh.dmsg('htk_on_debug_info', msg.format(name, phone, email), self._mh.fromhere());                  
        
        path = 'contact';
        url = self.url + path;
        headers = {'Content-Type' : 'application/json'};
        contact = crm.Contact(None, name, phone, email);
        body = contact.tojson();
        response, content = self.client.request(url, method='POST', headers=headers, body=body);              

        if (response.status == 200):
            self._mh.dmsg('htk_on_debug_info', 'contact {0} created'.format(content), self._mh.fromhere());
            return content;
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(response.status, content), self._mh.fromhere());
            return None;    
        
    def change_contact(self, id, name=None, phone=None, email=None):
        """Method changes contact
        
        Args:
           id - int, mandatory
           name - string, optional
           phone - string, optional
           email - string, optional          
             
        Returns:
           result - bool
                
        """  
        
        msg = 'params - id:{0}, name:{1}, phone:{2}, email:{3}';
        self._mh.dmsg('htk_on_debug_info', msg.format(id, name, phone, email), self._mh.fromhere());                     
        
        path = 'contact';
        url = self.url + path;
        headers = {'Content-Type' : 'application/json'};
        contact = crm.Contact(id, name, phone, email);
        body = contact.tojson();
        response, content = self.client.request(url, method='PUT', headers=headers, body=body);              

        if (response.status == 200):
            self._mh.dmsg('htk_on_debug_info', 'contact changed', self._mh.fromhere());
            return True;
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(response.status, content), self._mh.fromhere());
            return False;    
        
    def assign_contact_role(self, id, role, customer=None, payer=None, subscriber=None):
        """Method assigns contact role
        
        Args:
           id - int, mandatory
           role - string, mandatory, lov_contact_role.title
           customer - int, optional
           payer - int, optional
           subscriber - int, optional         
             
        Returns:
           result - bool
                
        """    
        
        msg = 'params - id:{0}, role:{1}, customer:{2}, payer:{3}, subscriber:{4}';
        self._mh.dmsg('htk_on_debug_info', msg.format(id, role, customer, payer, subscriber), self._mh.fromhere());                    
        
        path = 'contact/role';
        url = self.url + path;
        headers = {'Content-Type' : 'application/json'};
        contact_role = crm.ContactRole(id, role, customer, payer, subscriber);
        body = contact_role.tojson();
        response, content = self.client.request(url, method='POST', headers=headers, body=body);              

        if (response.status == 200):
            self._mh.dmsg('htk_on_debug_info', 'contact role assigned', self._mh.fromhere()); 
            return True;
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(response.status, content), self._mh.fromhere());
            return False;        
        
    def revoke_contact_role(self, id, role, customer=None, payer=None, subscriber=None):
        """Method revokes contact role
        
        Args:
           id - int, mandatory
           role - string, mandatory, lov_contact_role.title
           customer - int, optional
           payer - int, optional
           subscriber - int, optional         
             
        Returns:
           result - bool
                
        """   
        
        msg = 'params - id:{0}, role:{1}, customer:{2}, payer:{3}, subscriber:{4}';
        self._mh.dmsg('htk_on_debug_info', msg.format(id, role, customer, payer, subscriber), self._mh.fromhere());                 
        
        path = 'contact/role';
        url = self.url + path;
        headers = {'Content-Type' : 'application/json'};
        contact_role = crm.ContactRole(id, role, customer, payer, subscriber);
        body = contact_role.tojson();
        response, content = self.client.request(url, method='PUT', headers=headers, body=body);              

        if (response.status == 200):
            self._mh.dmsg('htk_on_debug_info', 'contact role revoked', self._mh.fromhere()); 
            return True;
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(response.status, content), self._mh.fromhere());
            return False;               
        
    def read_address(self, id):
        """Method reads address
        
        Args:
           id - int            
             
        Returns:
           address - crm_entities.Address 
                
        """           
        
        self._mh.dmsg('htk_on_debug_info', 'params - id:{0}'.format(id), self._mh.fromhere());
        
        path = 'address';
        params = {'id' : id};
        url = self.url + path + '?' + urllib.urlencode(params);
        headers = {'Accept' : 'application/json'};
        response, content = self.client.request(url, method='GET', headers=headers);

        if (response.status == 200):
            
            doc = jsonlib2.read(content);
                
            roles = [];
            if (doc.has_key('roles')):
                for role in doc['roles']['role']:
                    roles.append(crm.AddressRole(role['id'], role['title'], role['contact'],
                                                 role['customer'], role['payer'], role['subscriber']));
                
            address = crm.Address(doc['id'], doc['street'], doc['street_no'], doc['city'], doc['zip'], roles);
            self._mh.dmsg('htk_on_debug_info', 'address - {0}'.format(address), self._mh.fromhere());
                
            return address;
            
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(response.status, content), self._mh.fromhere());
            return None;  
        
    def create_address(self, street, street_no, city, zip):
        """Method creates address
        
        Args:
           street - string, mandatory
           street_no - string, mandatory
           city - string, mandatory
           zip - int, mandatory       
             
        Returns:
           id - int
                
        """ 
        
        msg = 'params - street:{0}, street_no:{1}, city:{2}, zip:{3}';
        self._mh.dmsg('htk_on_debug_info', msg.format(street, street_no, city, zip), self._mh.fromhere());                     
        
        path = 'address';
        url = self.url + path;
        headers = {'Content-Type' : 'application/json'};
        address = crm.Address(None, street, street_no, city, zip);
        body = address.tojson();
        response, content = self.client.request(url, method='POST', headers=headers, body=body);              

        if (response.status == 200):
            self._mh.dmsg('htk_on_debug_info', 'address {0} created'.format(content), self._mh.fromhere());
            return content;
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(response.status, content), self._mh.fromhere());
            return None;    
        
    def change_address(self, id, street=None, street_no=None, city=None, zip=None):
        """Method changes address
        
        Args:
           id - int, mandatory
           street - string, optional
           street_no - string, optional
           city - string, optional
           zip - int, optional    
             
        Returns:
           result - bool
                
        """  
        
        msg = 'params - id:{0}, street:{1}, street_no:{2}, city:{3}, zip:{4}';
        self._mh.dmsg('htk_on_debug_info', msg.format(id, street, street_no, city, zip), self._mh.fromhere());                     
        
        path = 'address';
        url = self.url + path;
        headers = {'Content-Type' : 'application/json'};
        address = crm.Address(id, street, street_no, city, zip);
        body = address.tojson();
        response, content = self.client.request(url, method='PUT', headers=headers, body=body);              

        if (response.status == 200):
            self._mh.dmsg('htk_on_debug_info', 'address changed', self._mh.fromhere());
            return True;
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(response.status, content), self._mh.fromhere());
            return False;                 
        
    def assign_address_role(self, id, role, contact=None, customer=None, payer=None, subscriber=None):
        """Method assigns address role
        
        Args:
           id - int, mandatory
           role - string, mandatory, lov_address_role.title
           contact - int, optional
           customer - int, optional
           payer - int, optional
           subscriber - int, optional      
             
        Returns:
           result - bool
                
        """ 
        
        msg = 'params - id:{0}, role:{1}, contact:{2}, customer:{3}, payer:{4}, subscriber:{5}';
        self._mh.dmsg('htk_on_debug_info', msg.format(id, role, contact, customer, payer, subscriber), self._mh.fromhere());                     
        
        path = 'address/role';
        url = self.url + path;
        headers = {'Content-Type' : 'application/json'};
        address_role = crm.AddressRole(id, role, contact, customer, payer, subscriber);
        body = address_role.tojson();
        response, content = self.client.request(url, method='POST', headers=headers, body=body);              

        if (response.status == 200):
            self._mh.dmsg('htk_on_debug_info', 'address role assigned', self._mh.fromhere()); 
            return True;
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(response.status, content), self._mh.fromhere());
            return False;     
        
    def revoke_address_role(self, id, role, contact=None, customer=None, payer=None, subscriber=None):
        """Method revokes address role
        
        Args:
           id - int, mandatory
           role - string, mandatory, lov_address_role.title
           contact - int, optional
           customer - int, optional
           payer - int, optional
           subscriber - int, optional      
             
        Returns:
           result - bool
                
        """   
        
        msg = 'params - id:{0}, role:{1}, contact:{2}, customer:{3}, payer:{4}, subscriber:{5}';
        self._mh.dmsg('htk_on_debug_info', msg.format(id, role, contact, customer, payer, subscriber), self._mh.fromhere());                 
        
        path = 'address/role';
        url = self.url + path;
        headers = {'Content-Type' : 'application/json'};
        address_role = crm.AddressRole(id, role, contact, customer, payer, subscriber);
        body = address_role.tojson();
        response, content = self.client.request(url, method='PUT', headers=headers, body=body);              

        if (response.status == 200):
            self._mh.dmsg('htk_on_debug_info', 'address role revoked', self._mh.fromhere()); 
            return True;
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(response.status, content), self._mh.fromhere());
            return False;   
        
    def read_services(self, customer=None, payer=None, subscriber=None, service=None):
        """Method read services
        
        Args:
           customer - int, optional
           payer - int, optional
           subscriber - int, optional
           service - int, optional, lov_service.id, default read all services for entity     
             
        Returns:
           services - list of crm_entities.Service
                
        """    
        
        msg = 'params - customer:{0}, payer:{1}, subscriber:{2}, service:{3}';
        self._mh.dmsg('htk_on_debug_info', msg.format(customer, payer, subscriber, service), self._mh.fromhere());                
        
        path = 'service';        
        headers = {'Accept' : 'application/json'};
        params = {};
        if (customer != None):
            params['customer'] = customer;
        if (payer != None):
            params['payer'] = payer;
        if (subscriber != None):
            params['subscriber'] = subscriber;
        if (service != None):
            params['service'] = service;                                    
        
        url = self.url + path + '?' + urllib.urlencode(params); 
        response, content = self.client.request(url, method='GET', headers=headers);

        if (response.status == 200):
            
            doc = jsonlib2.read(content);
             
            services = [];
            for service in doc['services']['service']:
                   
                params = {};
                for param in service['params']['entry']:
                    params[param['key']] = param['value'];
                
                services.append(crm.Service(service['id'], service['name'], service['status'], params));
            
            for service in services:    
                self._mh.dmsg('htk_on_debug_info', 'service - {0}'.format(service), self._mh.fromhere()); 
                    
            return services;                
                
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(response.status, content), self._mh.fromhere());
            return None;              
        
    def create_service(self, service, customer=None, payer=None, subscriber=None, status='active', params={}):  
        """Method creates service
        
        Args: 
           service - int, mandatory, lov_service.id
           customer - int, optional
           payer - int, optional
           subscriber - int, optional
           status - string, optional, lov_status.title, default active
           params - dictionary, optional, key - int, lov_service_param.id, value - string  
             
        Returns:
           result - bool
                
        """           
            
        msg = 'params - service:{0}, customer:{1}, payer:{2}, subscriber:{3}, status:{4}, params:{5}';
        self._mh.dmsg('htk_on_debug_info', msg.format(service, customer, payer, subscriber, status, params), self._mh.fromhere());                
        
        path = 'service';
        url = self.url + path;
        headers = {'Content-Type' : 'application/json'};
        service_operation = crm.ServiceOperation(service, customer, payer, subscriber, status, params)
        body = service_operation.tojson();
        response, content = self.client.request(url, method='POST', headers=headers, body=body);              

        if (response.status == 200):
            self._mh.dmsg('htk_on_debug_info', 'service created', self._mh.fromhere());
            return True;
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(response.status, content), self._mh.fromhere());
            return False;             
        
    def change_service(self, service, customer=None, payer=None, subscriber=None, status=None, params={}): 
        """Method changes service
        
        Args: 
           service - int, mandatory, lov_service.id
           customer - int, optional
           payer - int, optional
           subscriber - int, optional
           status - string, optional, lov_status.title
           params - dictionary, optional, key - int, lov_service_param.id, value - string  
             
        Returns:
           result - bool
                
        """   
        
        msg = 'params - service:{0}, customer:{1}, payer:{2}, subscriber:{3}, status:{4}, params:{5}';
        self._mh.dmsg('htk_on_debug_info', msg.format(service, customer, payer, subscriber, status, params), self._mh.fromhere());                 
        
        path = 'service';
        url = self.url + path;
        headers = {'Content-Type' : 'application/json'};
        service_operation = crm.ServiceOperation(service, customer, payer, subscriber, status, params);
        body = service_operation.tojson();
        response, content = self.client.request(url, method='PUT', headers=headers, body=body);              

        if (response.status == 200):
            self._mh.dmsg('htk_on_debug_info', 'service changed', self._mh.fromhere());
            return True;
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(response.status, content), self._mh.fromhere());
            return False;                    