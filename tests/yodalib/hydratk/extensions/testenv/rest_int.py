# -*- coding: utf-8 -*-
"""REST interface methods to be used in helpers

.. module:: yodalib.testenv.rest_int
   :platform: Unix
   :synopsis: REST interface methods
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.core.masterhead import MasterHead
from hydratk.lib.network.rest.client import RESTClient
from hydratk.extensions.testenv.entities import Customer, Payer, Subscriber, Service, ServiceOperation
from hydratk.extensions.testenv.entities import Contact, ContactRole, Address, AddressRole
from simplejson import loads

class REST_INT(object):
    """Class REST_INT
    """
    
    _mh = None 
    _ip = None
    _url = None
    _client = None   
    
    def __init__(self):
        """Class constructor
           
        Called when the object is initialized 
        
        Args:
           none   
           
        """          
        
        self._mh = MasterHead.get_head()
        ip = self._mh.cfg['Extensions']['TestEnv']['server_ip']
        port = self._mh.cfg['Extensions']['TestEnv']['server_port']  
        self._url = 'http://{0}:{1}/rs/'.format(ip, port)
        self._client = RESTClient()            
        
    def read_customer(self, id):
        """Method reads customer
        
        Args:
           id (int): customer id           
             
        Returns:
           obj: crm_entities.Customer
                
        """       
        
        msg = 'id:{0}'.format(id)
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_func', 'read_customer', msg), 
                      self._mh.fromhere())
        
        params = {'id' : id}
        url = self._url + 'customer'
        status, content = self._client.send_request(url, method='GET', params=params)

        if (status == 200):
            
            doc = loads(content)
            customer = Customer(doc['id'], doc['name'], doc['status'], doc['segment'], 
                                doc['birth_no'], doc['reg_no'], doc['tax_no'])
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_entity_found', 'customer', customer),
                          self._mh.fromhere())
                
            return customer
            
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(status, content), self._mh.fromhere())
            return None
        
    def create_customer(self, name, segment, status='active', birth_no=None, reg_no=None, tax_no=None):
        """Method creates customer
        
        Args:
           name (str): name
           segment (int): segment id, lov_segment.id
           status (str): status, lov_status.title, default active
           birth_no (str): birth number
           reg_no (str): registration number
           tax_no (str): tax identification number      
             
        Returns:
           int: created customer id
                
        """        
        
        msg = 'name:{0}, status:{1}, segment:{2}, birth_no:{3}, reg_no:{4}, tax_no:{5}'.format(
               name, status, segment, birth_no, reg_no, tax_no)
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_func', 'create_customer', msg), 
                      self._mh.fromhere())  
        
        url = self._url + 'customer'       
        customer = Customer(None, name, status, segment, birth_no, reg_no, tax_no)                        
        body = customer.tojson()         
        status, content = self._client.send_request(url, method='POST', body=body, content_type='json')              

        if (status == 200):
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_entity_created', 'customer', body), 
                          self._mh.fromhere())
            return content
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(status, content), self._mh.fromhere())
            return None   
        
    def change_customer(self, id, name=None, status=None, segment=None, birth_no=None, reg_no=None, tax_no=None):
        """Method changes customer
        
        Args:
           id (int): customer id
           name (str): name
           status (str): status, lov_status.title
           segment (int): segment id, lov_segment.id           
           birth_no (str): birth number
           reg_no (str): registration number
           tax_no (str): tax identification number      
             
        Returns: 
           bool: result
                
        """  
        
        msg = 'id:{0}, name:{1}, status:{2}, segment:{3}, birth_no:{4}, reg_no:{5}, tax_no:{6}'. format(
               id, name, status, segment, birth_no, reg_no, tax_no)
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_func', 'change_customer', msg), 
                      self._mh.fromhere())
                 
        url = self._url + 'customer'    
        customer = Customer(id, name, status, segment, birth_no, reg_no, tax_no)
        body = customer.tojson()
        status, content = self._client.send_request(url, method='PUT', body=body, content_type='json')              

        if (status == 200):
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_entity_changed', 'customer', id), 
                          self._mh.fromhere())    
            return True
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(status, content), self._mh.fromhere())
            return False   
       
    def read_payer(self, id):
        """Method reads payer
        
        Args:
           id (int): payer id          
             
        Returns:
           obj: crm_entities.Payer
                
        """         
        
        msg = 'id:{0}'.format(id)
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_func', 'read_Payer', msg), 
                      self._mh.fromhere()) 
        
        params = {'id' : id}
        url = self._url + 'payer'
        status, content = self._client.send_request(url, method='GET', params=params)

        if (status == 200):
            
            doc = loads(content)
            payer = Payer(doc['id'], doc['name'], doc['status'], doc['billcycle'], 
                          doc['customer'], doc['bank_account'])
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_entity_found', 'payer', payer),
                          self._mh.fromhere())                           
                
            return payer
            
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(status, content), self._mh.fromhere())
            return None 
        
    def create_payer(self, name, billcycle, customer, status='active', bank_account=None):
        """Method creates payer
        
        Args:
           name (str): name
           billcycle (int): billcycle, lov_billcycle.id
           customer (int): assigned customer id
           status (str): status, lov_status.title, default active
           bank_account (str): banking account            
             
        Returns:
           int: created payer id
                
        """ 
        
        msg = 'name:{0}, status:{1}, billcycle:{2}, bank_account:{3}, customer:{4}'.format(
               name, status, billcycle, bank_account, customer)
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_func', 'create_payer', msg), 
                      self._mh.fromhere())
            
        url = self._url + 'payer'
        payer = Payer(None, name, status, billcycle, customer, bank_account)
        body = payer.tojson()
        status, content = self._client.send_request(url, method='POST', body=body, content_type='json')              

        if (status == 200):
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_entity_created', 'payer', payer), 
                          self._mh.fromhere())
            return content
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(status, content), self._mh.fromhere())
            return None   
        
    def change_payer(self, id, name=None, status=None, billcycle=None, bank_account=None, customer=None):
        """Method changes payer
        
        Args:
           id (int): payer id
           name (str): name
           status (str): status, lov_status.title
           billcycle (int): billcycle id, lov_billcycle.id
           bank_account (str): banking account 
           customer (int): assigned customer id                    
             
        Returns:
           bool: result
                
        """ 
        
        msg = 'id:{0}, name:{1}, status:{2}, billcycle:{3}, bank_account:{4}, customer:{5}'.format(
               id, name, status, billcycle, bank_account, customer)
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_func', 'change_payer', msg), 
                      self._mh.fromhere()) 
            
        url = self._url + 'payer'
        payer = Payer(id, name, status, billcycle, customer, bank_account)
        body = payer.tojson()        
        status, content = self._client.send_request(url, method='PUT', body=body, content_type='json')              

        if (status == 200):
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_entity_changed', 'payer', id), 
                          self._mh.fromhere())    
            return True
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(status, content), self._mh.fromhere())
            return False  
        
    def read_subscriber(self, id):
        """Method reads subscriber
        
        Args:
           id (int): subscriber id           
             
        Returns:
           obj: crm_entities.Subscriber
                
        """         
        
        msg = 'id:{0}'.format(id)
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_func', 'read_subscriber', msg), 
                      self._mh.fromhere())
        
        params = {'id' : id}
        url = self._url + 'subscriber'        
        status, content = self._client.send_request(url, method='GET', params=params)

        if (status == 200):
            
            doc = loads(content)
            subscriber = Subscriber(doc['id'], doc['name'], doc['msisdn'], doc['status'], doc['market'], 
                                    doc['tariff'], doc['customer'], doc['payer'])
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_entity_found', 'subscriber', subscriber),
                          self._mh.fromhere())                                      
                
            return subscriber
            
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(status, content), self._mh.fromhere())
            return None  
        
    def create_subscriber(self, name, msisdn, market, tariff, customer, payer, status='active'):
        """Method creates subscriber
        
        Args:
           name (str): name
           msisdn (str): MSISDN
           market (int): market id, lov_market.id
           tariff (int): tariff id, lov_tariff.id
           customer (int): assigned customer id
           payer (int): assigned payer id
           status (str): status, lov_status.title, default active                              
             
        Returns:
           int: created subscriber id
                
        """     
        
        msg = 'name:{0}, msisdn:{1}, status:{2}, market:{3}, tariff:{4}, customer:{5}, payer:{6}'.format(
               name, msisdn, status, market, tariff, customer, payer)
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_func', 'create_subscriber', msg), 
                      self._mh.fromhere()) 
                    
        url = self._url + 'subscriber'
        subscriber = Subscriber(None, name, msisdn, status, market, tariff, customer, payer)
        body = subscriber.tojson()
        status, content = self._client.send_request(url, method='POST', body=body, content_type='json')              

        if (status == 200):
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_entity_created', 'subscriber', content), 
                          self._mh.fromhere())
            return content
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(status, content), self._mh.fromhere())
            return None  
        
    def change_subscriber(self, id, name=None, msisdn=None, status=None, market=None, tariff=None, customer=None, payer=None):
        """Method changes subscriber
        
        Args:
           id (int): subscriber id
           name (str): name
           msisdn (str): MSISDN
           status (str): status, lov_status.title           
           market (int): market id, lov_market.id
           tariff (int): tariff id, lov_tariff.id
           customer (int): assigned customer id
           payer (int): assigned payer id                     
             
        Returns:
           result: bool
        
        """ 
        
        msg = 'id:{0}, name:{1}, msisdn:{2}, status:{3}, market:{4}, tariff:{5}, customer:{6}, payer:{7}'.format(
               id, name, msisdn, status, market, tariff, customer, payer)
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_func', 'change_subscriber', msg), 
                      self._mh.fromhere())
            
        url = self._url + 'subscriber'
        subscriber = Subscriber(id, name, msisdn, status, market, tariff, customer, payer)
        body = subscriber.tojson()
        status, content = self._client.send_request(url, method='PUT', body=body, content_type='json')              

        if (status == 200):
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_entity_changed', 'subscriber', id), 
                          self._mh.fromhere())    
            return True
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(status, content), self._mh.fromhere())
            return False  
        
    def read_contact(self, id):
        """Method reads contact
        
        Args:
           id (int): contact id         
             
        Returns:
           obj: crm_entities.Contact
                
        """  
                  
        msg = 'id:{0}'.format(id)
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_func', 'read_contact', msg), 
                      self._mh.fromhere())
        
        params = {'id' : id}
        url = self._url + 'contact'
        status, content = self._client.send_request(url, method='GET', params=params)

        if (status == 200):
            
            doc = loads(content)
            roles = []
            if ('roles' in doc):                    
                for role in doc['roles']['role']:
                    roles.append(ContactRole(role['id'], role['title'], role['customer'],
                                             role['payer'], role['subscriber']))
                
            contact = Contact(doc['id'], doc['name'], doc['phone'], doc['email'], roles)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_entity_found', 'contact', contact),
                          self._mh.fromhere())
                
            return contact
            
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(status, content), self._mh.fromhere())
            return None   
        
    def create_contact(self, name, phone=None, email=None):
        """Method creates contact
        
        Args:
           name (str): name
           phone (str): phone number
           email (str): email         
             
        Returns:
           int: created contact id
                
        """    
        
        msg = 'name:{0}, phone:{1}, email:{2}'.format(name, phone, email)
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_func', 'create_contact', msg), 
                      self._mh.fromhere())                   
        
        url = self._url + 'contact'
        contact = Contact(None, name, phone, email)
        body = contact.tojson()
        status, content = self._client.send_request(url, method='POST', body=body, content_type='json')              

        if (status == 200):
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_entity_created', 'contact', content), 
                          self._mh.fromhere())
            return content
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(status, content), self._mh.fromhere())
            return None    
        
    def change_contact(self, id, name=None, phone=None, email=None):
        """Method changes contact
        
        Args:
           id (int): contact id
           name (str): name
           phone (str): phone number
           email (str): email         
             
        Returns:
           bool: result
                
        """  
        
        msg = 'id:{0}, name:{1}, phone:{2}, email:{3}'.format(id, name, phone, email)
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_func', 'change_contact', msg), 
                      self._mh.fromhere())                    
        
        url = self._url + 'contact'
        contact = Contact(id, name, phone, email)
        body = contact.tojson()
        status, content = self._client.send_request(url, method='PUT', body=body, content_type='json')              

        if (status == 200):
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_entity_changed', 'contact', id), 
                          self._mh.fromhere())    
            return True
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(status, content), self._mh.fromhere())
            return False    
        
    def assign_contact_role(self, id, role, customer=None, payer=None, subscriber=None):
        """Method assigns contact role
        
        Args:
           id (int): contact id
           role (str): role title, lov_contact_role.title
           customer (int): assigned customer id
           payer (int): assigned payer id
           subscriber (int): assigned subscriber id     
             
        Returns:
           bool: result
                
        """    
        
        msg = 'id:{0}, role:{1}, customer:{2}, payer:{3}, subscriber:{4}'.format(
               id, role, customer, payer, subscriber)
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_func', 'assign_contact_role', msg), 
                      self._mh.fromhere())                   
        
        url = self._url + 'contact/role'
        contact_role = ContactRole(id, role, customer, payer, subscriber)
        body = contact_role.tojson()
        status, content = self._client.send_request(url, method='POST', body=body, content_type='json')              

        if (status == 200):
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_role_assigned', 'contact'), 
                          self._mh.fromhere())  
            return True
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(status, content), self._mh.fromhere())
            return False        
        
    def revoke_contact_role(self, id, role, customer=None, payer=None, subscriber=None):
        """Method revokes contact role
        
        Args:
           id (int): contact id
           role (str): role title, lov_contact_role.title
           customer (int): assigned customer id
           payer (int): assigned payer id
           subscriber (int): assigned subscriber id     
             
        Returns:
           bool: result
                
        """   
        
        msg = 'id:{0}, role:{1}, customer:{2}, payer:{3}, subscriber:{4}'.format(
               id, role, customer, payer, subscriber)
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_func', 'revoke_contact_role', msg), 
                      self._mh.fromhere())
            
        url = self._url + 'contact/role'
        contact_role = ContactRole(id, role, customer, payer, subscriber)
        body = contact_role.tojson()
        status, content = self._client.send_request(url, method='PUT', body=body, content_type='json')              

        if (status == 200):
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_role_revoked', 'contact'), 
                          self._mh.fromhere())  
            return True
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(status, content), self._mh.fromhere())
            return False               
        
    def read_address(self, id):
        """Method reads address
        
        Args:
           id (int): address id         
             
        Returns:
           obj: crm_entities.Address 
                
        """            
        
        msg = 'id:{0}'.format(id)
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_func', 'read_address', msg), 
                      self._mh.fromhere())
        
        params = {'id' : id}
        url = self._url + 'address'
        status, content = self._client.send_request(url, method='GET', params=params)

        if (status == 200):
            
            doc = loads(content)
                
            roles = []
            if ('roles' in doc):
                for role in doc['roles']['role']:
                    roles.append(AddressRole(role['id'], role['title'], role['contact'],
                                             role['customer'], role['payer'], role['subscriber']))
                
            address = Address(doc['id'], doc['street'], doc['street_no'], doc['city'], doc['zip'], roles)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_entity_found', 'address', address),
                          self._mh.fromhere())
                
            return address
            
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(status, content), self._mh.fromhere())
            return None  
        
    def create_address(self, street, street_no, city, zip):
        """Method creates address
        
        Args:
           street (str): street
           street_no (str): street number
           city (str): city
           zip (int): zip code       
             
        Returns:
           int: created address id
                
        """   
        
        msg = 'street:{0}, street_no:{1}, city:{2}, zip:{3}'.format(street, street_no, city, zip)
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_func', 'create_address', msg), 
                      self._mh.fromhere())                   
        
        url = self._url + 'address'
        address = Address(None, street, street_no, city, zip)
        body = address.tojson()
        status, content = self._client.send_request(url, method='POST', body=body, content_type='json')              

        if (status == 200):
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_entity_created', 'address', content), 
                          self._mh.fromhere())
            return content
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(status, content), self._mh.fromhere())
            return None    
        
    def change_address(self, id, street=None, street_no=None, city=None, zip=None):
        """Method changes address
        
        Args:
           id (int): address id
           street (str): street
           street_no (str): street number
           city (str): city
           zip (int): zip code    
             
        Returns:
           bool: result
                
        """     
        
        msg = 'id:{0}, street:{1}, street_no:{2}, city:{3}, zip:{4}'.format(id, street, street_no, city, zip)
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_func', 'change_address', msg), 
                      self._mh.fromhere())                   
        
        url = self._url + 'address'
        address = Address(id, street, street_no, city, zip)
        body = address.tojson()
        status, content = self._client.send_request(url, method='PUT', body=body, content_type='json')              

        if (status == 200):
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_entity_changed', 'address', id), 
                          self._mh.fromhere())    
            return True
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(status, content), self._mh.fromhere())
            return False                 
        
    def assign_address_role(self, id, role, contact=None, customer=None, payer=None, subscriber=None):
        """Method assigns address role
        
        Args:
           id (int): address id
           role (str): role title, lov_address_role.title
           contact (int): assigned contact id
           customer (int): assigned customer id
           payer (int): assigned payer id
           subscriber (int): assigned subscriber id  
            
        Returns:
           bool: result
                
        """  
        
        msg = 'id:{0}, role:{1}, contact:{2}, customer:{3}, payer:{4}, subscriber:{5}'.format(
               id, role, contact, customer, payer, subscriber)
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_func', 'assign_address_role', msg), 
                      self._mh.fromhere())
            
        url = self._url + 'address/role'
        address_role = AddressRole(id, role, contact, customer, payer, subscriber)
        body = address_role.tojson()
        status, content = self._client.send_request(url, method='POST', body=body, content_type='json')              

        if (status == 200):
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_role_assigned', 'address'), 
                          self._mh.fromhere())  
            return True
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(status, content), self._mh.fromhere())
            return False     
        
    def revoke_address_role(self, id, role, contact=None, customer=None, payer=None, subscriber=None):
        """Method revokes address role
        
        Args:
           id (int): address id
           role (str): role title, lov_address_role.title
           contact (int): assigned contact id
           customer (int): assigned customer id
           payer (int): assigned payer id
           subscriber (int): assigned subscriber id  
             
        Returns:
           bool: result
                
        """    
        
        msg = 'id:{0}, role:{1}, contact:{2}, customer:{3}, payer:{4}, subscriber:{5}'.format(
               id, role, contact, customer, payer, subscriber)
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_func', 'revoke_address_role', msg), 
                      self._mh.fromhere())
            
        url = self._url + 'address/role'
        address_role = AddressRole(id, role, contact, customer, payer, subscriber)
        body = address_role.tojson()
        status, content = self._client.send_request(url, method='PUT', body=body, content_type='json')              

        if (status == 200):
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_role_revoked', 'address'), 
                          self._mh.fromhere())  
            return True
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(status, content), self._mh.fromhere())
            return False   
        
    def read_services(self, customer=None, payer=None, subscriber=None, service=None):
        """Method read services
        
        Args:
           customer (int): assigned customer id
           payer (int): assigned payer id
           subscriber (int): assigned subscriber id
           service (int): service id, lov_service.id, default empty, read all services for entity     
             
        Returns:
           list: list of crm_entities.Service
                
        """  
        
        msg = 'customer:{0}, payer:{1}, subscriber:{2}, service:{3}'.format(
               customer, payer, subscriber, service)
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_func', 'read_services', msg), 
                      self._mh.fromhere())
            
        params = {}
        if (customer != None):
            params['customer'] = customer
        if (payer != None):
            params['payer'] = payer
        if (subscriber != None):
            params['subscriber'] = subscriber
        if (service != None):
            params['service'] = service                                    
        
        url = self._url + 'service'
        status, content = self._client.send_request(url, method='GET', params=params)

        if (status == 200):
            
            doc = loads(content)
             
            services = []
            for service in doc['services']['service']:
                   
                params = {}
                for param in service['params']['entry']:
                    params[param['key']] = param['value']
                
                services.append(Service(service['id'], service['name'], service['status'], params))
            
            for service in services:    
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_entity_found', 'service', service),
                              self._mh.fromhere())
                    
            return services                
                
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(status, content), self._mh.fromhere())
            return None              
        
    def create_service(self, service, customer=None, payer=None, subscriber=None, status='active', params={}):  
        """Method creates service
        
        Args: 
           service (int): service id, lov_service.id
           customer (int): assigned customer id
           payer (int): assigned payer id
           subscriber (int): assigned subscriber id
           status (str): status, lov_status.title, default active
           params (dict): key (int), lov_service_param.id, value (str)  
             
        Returns:
           bool: result
                
        """         
            
        msg = 'service:{0}, customer:{1}, payer:{2}, subscriber:{3}, status:{4}, params:{5}'.format(
               service, customer, payer, subscriber, status, params)
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_func', 'create_service', msg), 
                      self._mh.fromhere())
            
        url = self._url + 'service'
        service_operation = ServiceOperation(service, customer, payer, subscriber, status, params)
        body = service_operation.tojson()
        status, content = self._client.send_request(url, method='POST', body=body, content_type='json')              

        if (status == 200):
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_entity_created', 'service', service), 
                          self._mh.fromhere())
            return True
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(status, content), self._mh.fromhere())
            return False             
        
    def change_service(self, service, customer=None, payer=None, subscriber=None, status=None, params={}): 
        """Method changes service
        
        Args: 
           service (int): service id, lov_service.id
           customer (int): assigned customer id
           payer (int): assigned payer id
           subscriber (int): assigned subscriber id
           status (str): status, lov_status.title, default active
           params (dict): key (int), lov_service_param.id, value (str)  
             
        Returns:
           bool: result
                
        """        
        
        msg = 'service:{0}, customer:{1}, payer:{2}, subscriber:{3}, status:{4}, params:{5}'.format(
               service, customer, payer, subscriber, status, params)
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_func', 'change_service', msg), 
                      self._mh.fromhere())
            
        url = self._url + 'service'
        service_operation = ServiceOperation(service, customer, payer, subscriber, status, params)
        body = service_operation.tojson()
        status, content = self._client.send_request(url, method='PUT', body=body, content_type='json')              

        if (status == 200):
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_rest_entity_changed', 'service', service), 
                          self._mh.fromhere())
            return True
        else:
            self._mh.dmsg('htk_on_extension_error', 'status:{0}, content:{1}'.format(status, content), self._mh.fromhere())
            return False       
                