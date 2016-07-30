# -*- coding: utf-8 -*-
"""SOAP interface methods to be used in helpers

.. module:: testenv.interfaces.soap_int
   :platform: Unix
   :synopsis: SOAP interface methods to be used in helpers
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.core.masterhead import MasterHead
from hydratk.lib.network.soap.client import SOAPClient
from hydratk.extensions.testenv.entities import Customer, Payer, Subscriber, Service
from hydratk.extensions.testenv.entities import Contact, ContactRole, Address, AddressRole
from lxml.etree import Element, SubElement, tostring

class SOAP_INT(object):
    """Class SOAP_INT
    """
    
    _mh = None
    _wsdl = None
    _ns = None
    
    def __init__(self):
        """Class constructor
           
        Called when the object is initialized  
        
        Args:  
           none
           
        """          
        
        self._mh = MasterHead.get_head()
        ip = self._mh.cfg['Extensions']['TestEnv']['server_ip']
        port = self._mh.cfg['Extensions']['TestEnv']['server_port'] 
        self._wsdl = 'http://{0}:{1}/ws/crm?wsdl'.format(ip, port)      
        self._client = SOAPClient()
        self._client.load_wsdl(self._wsdl)
        self._ns = '{http://hydratk.org/}'
        
    def is_soap_fault(self, res):
        """Method checks if response is SOAP fault
        
        Args:
           res (str): response
           
        Returns:
           bool: result
                
        """         
        
        allowed = ['int', 'bool', 'customer', 'payer', 'subscriber', 'contact', 'address', 'services']
        return (res.__class__.__name__ not in allowed)        
    
    def read_customer(self, id):
        """Method reads customer
        
        Args:
           id (int): customer id           
             
        Returns:
           obj: crm_entities.Customer
                
        """         
        
        msg = 'id:{0}'.format(id)
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'read_customer', msg), 
                      self._mh.fromhere())
            
        root = Element(self._ns+'read_customer')
        SubElement(root, 'id').text = str(id)
            
        res = self._client.send_request('read_customer', body=root, headers={'SOAPAction': 'read_customer'})
            
        if (self.is_soap_fault(res)):
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
            return None
        else:
            birth_no = res.birth_no if (hasattr(res, 'birth_no')) else None
            reg_no = res.reg_no if (hasattr(res, 'reg_no')) else None
            tax_no = res.tax_no if (hasattr(res, 'tax_no')) else None                
            customer = Customer(res.id, res.name, res.status, res.segment, birth_no, reg_no, tax_no)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_entity_found', 'customer', customer),
                          self._mh.fromhere())                           
            return customer   
        
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
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'create_customer', msg), 
                      self._mh.fromhere()) 
        
        root = Element(self._ns+'create_customer')
        SubElement(root, 'name').text = name
        SubElement(root, 'status').text = status
        SubElement(root, 'segment').text = str(segment)
        if (birth_no != None): 
            SubElement(root, 'birth_no').text = birth_no
        if (reg_no != None):
            SubElement(root, 'reg_no').text = reg_no
        if (tax_no != None):
            SubElement(root, 'tax_no').text = tax_no
            
        res = self._client.send_request('create_customer', body=tostring(root), headers={'SOAPAction': 'create_customer'})
            
        if (self.is_soap_fault(res)):
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
            return None
        else:
            id = res
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_entity_created', 'customer', id), 
                          self._mh.fromhere())           
            return id
                
       
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
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'change_customer', msg), 
                      self._mh.fromhere())
            
        root = Element(self._ns+'change_customer')
        SubElement(root, 'id').text = str(id)
        if (name != None):
            SubElement(root, 'name').text = name
        if (status != None):
            SubElement(root, 'status').text = status
        if (segment != None):
            SubElement(root, 'segment').text = str(segment)
        if (birth_no != None):
            SubElement(root, 'birth_no').text = birth_no
        if (reg_no != None):
            SubElement(root, 'reg_no').text = reg_no
        if (tax_no != None):    
            SubElement(root, 'tax_no').text = tax_no    
            
        res = self._client.send_request('change_customer', body=tostring(root), headers={'SOAPAction': 'change_customer'})
            
        if (self.is_soap_fault(res)):
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
            return False
        else:
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_entity_changed', 'customer', id), 
                          self._mh.fromhere())                
            return True            
        
    def read_payer(self, id):
        """Method reads payer
        
        Args:
           id (int): payer id          
             
        Returns:
           obj: crm_entities.Payer
                
        """         
        
        msg = 'id:{0}'.format(id)
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'read_payer', msg), 
                      self._mh.fromhere()) 
        
        root = Element(self._ns+'read_payer')
        SubElement(root, 'id').text = str(id)
            
        res = self._client.send_request('read_payer', body=tostring(root), headers={'SOAPAction': 'read_payer'})
            
        if (self.is_soap_fault(res)):
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
            return None
        else:
            bank_account = res.bank_account if (hasattr(res, 'bank_account')) else None
            payer = Payer(res.id, res.name, res.status, res.billcycle, res.customer, bank_account)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_entity_found', 'payer', payer),
                          self._mh.fromhere())         
            return payer   
        
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
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'create_payer', msg), 
                      self._mh.fromhere())
         
        root = Element(self._ns+'create_payer')
        SubElement(root, 'name').text = name 
        SubElement(root, 'status').text = status 
        SubElement(root, 'billcycle').text = str(billcycle)
        if (bank_account != None):
            SubElement(root, 'bank_account').text = bank_account
        SubElement(root, 'customer').text = str(customer) 
            
        res = self._client.send_request('create_payer', body=tostring(root), headers={'SOAPAction': 'create_payer'})
            
        if (self.is_soap_fault(res)):
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
            return None
        else:
            id = res
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_entity_created', 'payer', id), 
                          self._mh.fromhere())        
            return id     
        
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
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'change_payer', msg), 
                      self._mh.fromhere())  
            
        root = Element(self._ns+'change_payer')
        
        SubElement(root, 'id').text = str(id)
        if (name != None):
            SubElement(root, 'name').text = name 
        if (status != None):
            SubElement(root, 'status').text = status
        if (billcycle != None):         
            SubElement(root, 'billcycle').text = str(billcycle)
        if (bank_account != None):
            SubElement(root, 'bank_account').text = bank_account
        if (customer != None):
            SubElement(root, 'customer').text = str(customer)     
            
        res = self._client.send_request('change_payer', body=tostring(root), headers={'SOAPAction': 'change_payer'})
            
        if (self.is_soap_fault(res)):
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
            return False
        else:
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_entity_changed', 'payer', id), 
                          self._mh.fromhere())              
            return True   
        
    def read_subscriber(self, id):
        """Method reads subscriber
        
        Args:
           id (int): subscriber id           
             
        Returns:
           obj: crm_entities.Subscriber
                
        """          
        
        msg = 'id:{0}'.format(id)
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'read_subscriber', msg), 
                      self._mh.fromhere())
            
        root = Element(self._ns+'read_subscriber')
        SubElement(root, 'id').text = str(id)    
            
        res = self._client.send_request('read_subscriber', body=tostring(root), headers={'SOAPAction': 'read_subscriber'})        
            
        if (self.is_soap_fault(res)):
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
            return None
        else:
            subscriber = Subscriber(res.id, res.name, res.msisdn, res.status, res.market, res.tariff,
                                    res.customer, res.payer)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_entity_found', 'subscriber', subscriber),
                          self._mh.fromhere())           
            return subscriber     
        
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
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'create_subscriber', msg), 
                      self._mh.fromhere())    
            
        root = Element(self._ns+'create_subscriber')
        SubElement(root, 'name').text = name  
        SubElement(root, 'msisdn').text = msisdn
        SubElement(root, 'status').text = status
        SubElement(root, 'market').text = str(market)
        SubElement(root, 'tariff').text = str(tariff)
        SubElement(root, 'customer').text = str(customer)
        SubElement(root, 'payer').text = str(payer)   
            
        res = self._client.send_request('create_subscriber', body=tostring(root), headers={'SOAPAction': 'create_subscriber'})
            
        if (self.is_soap_fault(res)):
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
            return None
        else:
            id = res
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_entity_created', 'subscriber', id), 
                          self._mh.fromhere())           
            return id   
        
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
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'change_subscriber', msg), 
                      self._mh.fromhere())
            
        root = Element(self._ns+'change_subscriber')
        SubElement(root, 'id').text = str(id)
        if (name != None):
            SubElement(root, 'name').text = name
        if (msisdn != None):  
            SubElement(root, 'msisdn').text = msisdn
        if (status != None):
            SubElement(root, 'status').text = status
        if (market != None):
            SubElement(root, 'market').text = str(market)
        if (tariff != None):
            SubElement(root, 'tariff').text = str(tariff)
        if (customer != None):
            SubElement(root, 'customer').text = str(customer)
        if (payer != None):
            SubElement(root, 'payer').text = str(payer)       
            
        res = self._client.send_request('change_subscriber', body=tostring(root), headers={'SOAPAction': 'change_subscriber'})
            
        if (self.is_soap_fault(res)):
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
            return False
        else:
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_entity_changed', 'subscriber', id), 
                          self._mh.fromhere())              
            return True           
        
    def read_contact(self, id):
        """Method reads contact
        
        Args:
           id (int): contact id         
             
        Returns:
           obj: crm_entities.Contact
                
        """          
        
        msg = 'id:{0}'.format(id)
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'read_contact', msg), 
                      self._mh.fromhere())
            
        root = Element(self._ns+'read_contact')
        SubElement(root, 'id').text = str(id)    
            
        res = self._client.send_request('read_contact', body=tostring(root), headers={'SOAPAction': 'read_contact'})
            
        if (self.is_soap_fault(res)):
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
            return None
        else:
                
            roles = []
            if (hasattr(res, 'roles')):                                        
                for role in res.roles[0]:
                    customer = role.customer if (hasattr(role, 'customer')) else None
                    payer = role.payer if (hasattr(role, 'payer')) else None
                    subscriber = role.subscriber if (hasattr(role, 'subscriber')) else None
                    roles.append(ContactRole(role.id, role.title, customer, payer, subscriber))
                
            phone = res.phone if (hasattr(res, 'phone')) else None
            email = res.email if (hasattr(res, 'email')) else None
            contact = Contact(res.id, res.name, phone, email, roles)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_entity_found', 'contact', contact),
                              self._mh.fromhere())           
            return contact   
        
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
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'create_contact', msg), 
                      self._mh.fromhere())      
            
        root = Element(self._ns+'create_contact')
        SubElement(root, 'name').text = name
        if (phone != None):
            SubElement(root, 'phone').text = phone
        if (email != None):
            SubElement(root, 'email').text = email    
            
        res = self._client.send_request('create_contact', body=tostring(root), headers={'SOAPAction': 'create_contact'})
            
        if (self.is_soap_fault(res)):
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
            return None
        else:
            id = res
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_entity_created', 'contact', id), 
                          self._mh.fromhere())           
            return id     
        
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
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'change_contact', msg), 
                      self._mh.fromhere())       
            
        root = Element(self._ns+'change_contact')
        SubElement(root, 'id').text = str(id)
        if (name != None):
            SubElement(root, 'name').text = name
        if (phone != None):
            SubElement(root, 'phone').text = phone
        if (email != None):
            SubElement(root, 'email').text = email    
            
        res = self._client.send_request('change_contact', body=tostring(root), headers={'SOAPAction': 'change_contact'})
            
        if (self.is_soap_fault(res)):
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
            return False
        else:
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_entity_changed', 'contact', id), 
                          self._mh.fromhere())              
            return True
        
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
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'assign_contact_role', msg), 
                      self._mh.fromhere())
         
        root = Element(self._ns+'assign_contact_role')
        SubElement(root, 'id').text = str(id) 
        SubElement(root, 'title').text = role 
        if (customer != None):
            SubElement(root, 'customer').text = str(customer) 
        if (payer != None):
            SubElement(root, 'payer').text = str(payer)
        if (subscriber != None): 
            SubElement(root, 'subscriber').text = str(subscriber) 
            
        res = self._client.send_request('assign_contact_role', body=tostring(root), headers={'SOAPAction': 'assign_contact_role'})
            
        if (self.is_soap_fault(res)):
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
            return False
        else:
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_role_assigned', 'contact'), 
                          self._mh.fromhere())           
            return True   
        
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
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'revoke_contact_role', msg), 
                      self._mh.fromhere())
            
        root = Element(self._ns+'revoke_contact_role')
        SubElement(root, 'id').text = str(id) 
        SubElement(root, 'title').text = role 
        if (customer != None):
            SubElement(root, 'customer').text = str(customer) 
        if (payer != None):
            SubElement(root, 'payer').text = str(payer)
        if (subscriber != None): 
            SubElement(root, 'subscriber').text = str(subscriber)    
            
        res = self._client.send_request('revoke_contact_role', body=tostring(root), headers={'SOAPAction': 'revoke_contact_role'})
            
        if (self.is_soap_fault(res)):
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
            return False
        else:
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_role_revoked', 'contact'), 
                          self._mh.fromhere())                
            return True             
           
    def read_address(self, id):
        """Method reads address
        
        Args:
           id (int): address id         
             
        Returns:
           obj: crm_entities.Address 
                
        """          
        
        msg = 'id:{0}'.format(id)
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'read_address', msg), 
                      self._mh.fromhere())
        
        root = Element(self._ns+'read_address')
        SubElement(root, 'id').text = str(id)
            
        res = self._client.send_request('read_address', body=tostring(root), headers={'SOAPAction': 'read_address'})
            
        if (self.is_soap_fault(res)):
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
            return None
        else:
                
            roles = []
            if (hasattr(res, 'roles')):                                        
                for role in res.roles[0]:
                    contact = role.contact if (hasattr(role, 'contact')) else None
                    customer = role.customer if (hasattr(role, 'customer')) else None
                    payer = role.payer if (hasattr(role, 'payer')) else None
                    subscriber = role.subscriber if (hasattr(role, 'subscriber')) else None
                    roles.append(AddressRole(role.id, role.title, contact, customer, payer, subscriber))                
                
            address = Address(res.id, res.street, res.street_no, res.city, res.zip, roles)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_entity_found', 'address', address),
                          self._mh.fromhere())           
            return address    
        
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
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'create_address', msg), 
                      self._mh.fromhere())  
        
        root = Element(self._ns+'create_address')
        SubElement(root, 'street').text = street
        SubElement(root, 'street_no').text = street_no
        SubElement(root, 'city').text = city
        SubElement(root, 'zip').text = str(zip)
            
        res = self._client.send_request('create_address', body=tostring(root), headers={'SOAPAction': 'create_address'})
            
        if (self.is_soap_fault(res)):
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
            return None
        else:
            id = res
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_entity_created', 'address', id), 
                          self._mh.fromhere())           
            return id 
        
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
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'change_address', msg), 
                      self._mh.fromhere())  
            
        root = Element(self._ns+'change_address')
        SubElement(root, 'id').text = str(id)
        if (street != None):  
            SubElement(root, 'street').text = street
        if (street_no != None):
            SubElement(root, 'street_no').text = street_no
        if (city != None):
            SubElement(root, 'city').text = city
        if (zip != None):
            SubElement(root, 'zip').text = str(zip)    
            
        res = self._client.send_request('change_address', body=tostring(root), headers={'SOAPAction': 'change_address'})
            
        if (self.is_soap_fault(res)):
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
            return False
        else:
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_entity_changed', 'address', id), 
                          self._mh.fromhere())             
            return True         
        
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
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'assign_address_role', msg), 
                      self._mh.fromhere())
         
        root = Element(self._ns+'assign_address_role')
        SubElement(root, 'id').text = str(id) 
        SubElement(root, 'title').text = role 
        if (contact != None):
            SubElement(root, 'contact').text = str(contact) 
        if (customer != None):
            SubElement(root, 'customer').text = str(customer)
        if (payer != None): 
            SubElement(root, 'payer').text = str(payer)
        if (subscriber != None): 
            SubElement(root, 'subscriber').text = str(subscriber) 
            
        res = self._client.send_request('assign_address_role', body=tostring(root), headers={'SOAPAction': 'assign_address_role'})
            
        if (self.is_soap_fault(res)):
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
            return False
        else:
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_role_assigned', 'address'), 
                          self._mh.fromhere())                
            return True  
        
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
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'revoke_address_role', msg), 
                      self._mh.fromhere())
            
        root = Element(self._ns+'revoke_address_role')
        SubElement(root, 'id').text = str(id) 
        SubElement(root, 'title').text = role 
        if (contact != None):
            SubElement(root, 'contact').text = str(contact) 
        if (customer != None):
            SubElement(root, 'customer').text = str(customer)
        if (payer != None): 
            SubElement(root, 'payer').text = str(payer)
        if (subscriber != None): 
            SubElement(root, 'subscriber').text = str(subscriber)     
            
        res = self._client.send_request('revoke_address_role', body=tostring(root), headers={'SOAPAction': 'revoke_address_role'})
            
        if (self.is_soap_fault(res)):
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
            return False
        else:
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_role_revoked', 'address'), 
                          self._mh.fromhere())          
            return True   
        
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
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'read_services', msg), 
                      self._mh.fromhere())
            
        root = Element(self._ns+'read_services')
        if (customer != None):
            SubElement(root, 'customer').text = str(customer)
        if (payer != None):
            SubElement(root, 'payer').text = str(payer)
        if (subscriber != None):    
            SubElement(root, 'subscriber').text = str(subscriber)
        if (service != None):    
            SubElement(root, 'service').text = str(service)        
            
        res = self._client.send_request('read_services', body=tostring(root), headers={'SOAPAction': 'read_services'})
            
        if (self.is_soap_fault(res)):
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
            return False
        else:
                
            services = []
            for service in res.service:
                   
                params = {}
                for param in service.params.entry:
                    params[param.key] = param.value
                
                services.append(Service(service.id, service.name, service.status, params))
            
            for service in services:    
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_entity_found', 'service', service),
                              self._mh.fromhere())
                    
            return services       
        
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
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'create_service', msg), 
                      self._mh.fromhere())
            
        root = Element(self._ns+'create_service')
        SubElement(root, 'service').text = str(service)
        if (customer != None):
            SubElement(root, 'customer').text = str(customer)
        if (payer != None):
            SubElement(root, 'payer').text = str(payer)
        if (subscriber != None):
            SubElement(root, 'subscriber').text = str(subscriber)
        SubElement(root, 'status').text = status    
            
        el_params = SubElement(root, 'params')            
        for key, value in params.items():
            entry = Element('entry')
            SubElement(entry, 'key').text = str(key)
            SubElement(entry, 'value').text = value
            el_params.append(entry)            
            
        res = self._client.send_request('create_service', body=tostring(root), headers={'SOAPAction': 'create_service'})
            
        if (self.is_soap_fault(res)):
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
            return False
        else:
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_entity_created', 'service', service), 
                              self._mh.fromhere())          
            return True           
        
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
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'change_service', msg), 
                      self._mh.fromhere())
            
        root = Element(self._ns+'change_service')
        SubElement(root, 'service').text = str(service)
        if (customer != None):
            SubElement(root, 'customer').text = str(customer)
        if (payer != None):
            SubElement(root, 'payer').text = str(payer)
        if (subscriber != None):
            SubElement(root, 'subscriber').text = str(subscriber)
        if (status != None):
            SubElement(root, 'status').text = status      
            
        el_params = SubElement(root, 'params')            
        for key, value in params.items():
            entry = Element('entry')
            SubElement(entry, 'key').text = str(key)
            SubElement(entry, 'value').text = value
            el_params.append(entry)                          
            
        res = self._client.send_request('change_service', body=tostring(root), headers={'SOAPAction': 'change_service'})
            
        if (self.is_soap_fault(res)):
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
            return False
        else:
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_entity_changed', 'service', service), 
                          self._mh.fromhere())              
            return True
                                                