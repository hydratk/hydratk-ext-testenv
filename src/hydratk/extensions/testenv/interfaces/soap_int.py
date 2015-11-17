# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.extensions.testenv.interfaces.soap_int
   :platform: Unix
   :synopsis: SOAP interface for testenv
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.core.masterhead import MasterHead
import hydratk.extensions.testenv.entities.crm_entities as crm
import suds
import logging

logging.getLogger('suds.client').setLevel(logging.CRITICAL)

class SOAP_INT():
    
    _mh = None
    _wsdl = None
    
    def __init__(self):
        
        self._mh = MasterHead.get_head()
        ip = self._mh.cfg['Extensions']['TestEnv']['server_ip']
        port = self._mh.cfg['Extensions']['TestEnv']['server_port'] 
        self._wsdl = 'http://{0}:{1}/ws/crm?wsdl'.format(ip, port)      
        self._client = suds.client.Client(self._wsdl)
        
    def is_soap_fault(self, res):
        
        return isinstance(res, unicode)        
    
    def read_customer(self, id):
        """Method reads customer
        
        Args:
           id - int, mandatory            
             
        Returns:
           customer - crm_entities.Customer
                
        """          
        
        try:
            
            msg = 'id:{0}'.format(id)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'read_customer', msg), 
                          self._mh.fromhere())
            
            self._client.set_options(headers={'SOAPAction': 'read_customer'})
            res = self._client.service.read_customer(id)
            
            if (self.is_soap_fault(res)):
                self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
                return None
            else:
                birth_no = res.birth_no if (hasattr(res, 'birth_no')) else None
                reg_no = res.reg_no if (hasattr(res, 'reg_no')) else None
                tax_no = res.tax_no if (hasattr(res, 'tax_no')) else None                
                customer = crm.Customer(res.id, res.name, res.status, res.segment, birth_no, reg_no, tax_no)
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_entity_found', 'customer', customer),
                              self._mh.fromhere())                           
                return customer
            
        except suds.WebFault as ex:
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(ex), self._mh.fromhere())
            return None      
        
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
        
        try:
            
            msg = 'name:{0}, status:{1}, segment:{2}, birth_no:{3}, reg_no:{4}, tax_no:{5}'.format(
                   name, status, segment, birth_no, reg_no, tax_no)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'create_customer', msg), 
                          self._mh.fromhere()) 
            
            self._client.set_options(headers={'SOAPAction': 'create_customer'})
            res = self._client.service.create_customer(name, status, segment, birth_no, reg_no, tax_no)
            
            if (self.is_soap_fault(res)):
                self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
                return None
            else:
                id = res
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_entity_created', 'customer', id), 
                              self._mh.fromhere())           
                return id
            
        except suds.WebFault as ex:
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(ex), self._mh.fromhere())
            return None      
        
    def change_customer(self, id, name=None, status=None, segment=None, birth_no=None, reg_no=None, tax_no=None):
        """Method changes customer
        
        Args:
           id - int, mandatory
           name - string, optional
           status - string, optional, lov_status.title,           
           segment - int, optional, lov_segment.id           
           birth_no - string, optional
           reg_no - string, optional
           tax_no - string, optional             
             
        Returns:
           result - bool
                
        """          
        
        try:
            
            msg = 'id:{0}, name:{1}, status:{2}, segment:{3}, birth_no:{4}, reg_no:{5}, tax_no:{6}'. format(
                   id, name, status, segment, birth_no, reg_no, tax_no)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'change_customer', msg), 
                          self._mh.fromhere())
            
            self._client.set_options(headers={'SOAPAction': 'change_customer'})
            res = self._client.service.change_customer(id, name, status, segment, birth_no, reg_no, tax_no)
            
            if (self.is_soap_fault(res)):
                self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
                return False
            else:
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_entity_changed', 'customer', id), 
                              self._mh.fromhere())                
                return True
            
        except suds.WebFault as ex:
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(ex), self._mh.fromhere())
            return False              
        
    def read_payer(self, id):
        """Method reads payer
        
        Args:
           id - int, mandatory            
             
        Returns:
           payer - crm_entities.Payer
                
        """          
        
        try:
            
            msg = 'id:{0}'.format(id)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'read_Payer', msg), 
                          self._mh.fromhere()) 
            
            self._client.set_options(headers={'SOAPAction': 'read_payer'})
            res = self._client.service.read_payer(id)
            
            if (self.is_soap_fault(res)):
                self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
                return None
            else:
                bank_account = res.bank_account if (hasattr(res, 'bank_account')) else None
                payer = crm.Payer(res.id, res.name, res.status, res.billcycle, res.customer, bank_account)
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_entity_found', 'payer', payer),
                              self._mh.fromhere())         
                return payer
            
        except suds.WebFault as ex:
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(ex), self._mh.fromhere())
            return None      
        
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
        
        try:
            
            msg = 'name:{0}, status:{1}, billcycle:{2}, bank_account:{3}, customer:{4}'.format(
                   name, status, billcycle, bank_account, customer)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'create_payer', msg), 
                          self._mh.fromhere())
            
            self._client.set_options(headers={'SOAPAction': 'create_payer'})
            res = self._client.service.create_payer(name, status, billcycle, bank_account, customer)
            
            if (self.is_soap_fault(res)):
                self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
                return None
            else:
                id = res
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_entity_created', 'payer', id), 
                              self._mh.fromhere())        
                return id
            
        except suds.WebFault as ex:
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(ex), self._mh.fromhere())
            return None      
        
    def change_payer(self, id, name=None, status=None, billcycle=None, bank_account=None, customer=None):
        """Method changes payer
        
        Args:
           id - int, mandatory
           name - string, optional
           status - string, optional, lov_status.title,           
           billcycle - int, optional, lov_billcycle.id        
           bank_account - string, optional
           customer - int, optional             
             
        Returns:
           result - bool
                
        """          
        
        try:
            
            msg = 'id:{0}, name:{1}, status:{2}, billcycle:{3}, bank_account:{4}, customer:{5}'.format(
                   id, name, status, billcycle, bank_account, customer)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'change_payer', msg), 
                          self._mh.fromhere())  
            
            self._client.set_options(headers={'SOAPAction': 'change_payer'})
            res = self._client.service.change_payer(id, name, status, billcycle, bank_account, customer)
            
            if (self.is_soap_fault(res)):
                self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
                return False
            else:
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_entity_changed', 'payer', id), 
                              self._mh.fromhere())              
                return True
            
        except suds.WebFault as ex:
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(ex), self._mh.fromhere())
            return False    
        
    def read_subscriber(self, id):
        """Method reads subscriber
        
        Args:
           id - int, mandatory            
             
        Returns:
           subscriber - crm_entities.Subscriber
                
        """          
        
        try:
            
            msg = 'id:{0}'.format(id)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'read_subscriber', msg), 
                          self._mh.fromhere())
            
            self._client.set_options(headers={'SOAPAction': 'read_subscriber'})
            res = self._client.service.read_subscriber(id)
            
            if (self.is_soap_fault(res)):
                self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
                return None
            else:
                subscriber = crm.Subscriber(res.id, res.name, res.msisdn, res.status, res.market, res.tariff,
                                            res.customer, res.payer)
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_entity_found', 'subscriber', subscriber),
                              self._mh.fromhere())           
                return subscriber
            
        except suds.WebFault as ex:
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(ex), self._mh.fromhere())
            return None      
        
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
        
        try:
            
            msg = 'name:{0}, msisdn:{1}, status:{2}, market:{3}, tariff:{4}, customer:{5}, payer:{6}'.format(
                   name, msisdn, status, market, tariff, customer, payer)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'create_subscriber', msg), 
                          self._mh.fromhere())    
            
            self._client.set_options(headers={'SOAPAction': 'create_subscriber'})
            res = self._client.service.create_subscriber(name, msisdn, status, market, tariff, customer, payer)
            
            if (self.is_soap_fault(res)):
                self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
                return None
            else:
                id = res
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_entity_created', 'subscriber', id), 
                              self._mh.fromhere())           
                return id
            
        except suds.WebFault as ex:
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(ex), self._mh.fromhere())
            return None      
        
    def change_subscriber(self, id, name=None, msisdn=None, status=None, market=None, tariff=None, customer=None, payer=None):
        """Method changes subscriber
        
        Args:
           id - int, mandatory
           name - string, optional
           status - string, optional, lov_status.title,           
           market - int, optional, lov_market.id           
           tariff - int, optional, lov_tariff.id
           customer - int, optional
           payer - int, optional             
             
        Returns:
           result - bool
                
        """          
        
        try:
            
            msg = 'id:{0}, name:{1}, msisdn:{2}, status:{3}, market:{4}, tariff:{5}, customer:{6}, payer:{7}'.format(
                   id, name, msisdn, status, market, tariff, customer, payer)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'change_subscriber', msg), 
                          self._mh.fromhere())
            
            self._client.set_options(headers={'SOAPAction': 'change_subscriber'})
            res = self._client.service.change_subscriber(id, name, msisdn, status, market, tariff, customer, payer)
            
            if (self.is_soap_fault(res)):
                self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
                return False
            else:
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_entity_changed', 'subscriber', id), 
                              self._mh.fromhere())              
                return True
            
        except suds.WebFault as ex:
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(ex), self._mh.fromhere())
            return False            
        
    def read_contact(self, id):
        """Method reads contact
        
        Args:
           id - int, mandatory            
             
        Returns:
           contact - crm_entities.Contact
                
        """          
        
        try:
            
            msg = 'id:{0}'.format(id)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'read_contact', msg), 
                          self._mh.fromhere())
            
            self._client.set_options(headers={'SOAPAction': 'read_contact'})
            res = self._client.service.read_contact(id)
            
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
                        roles.append(crm.ContactRole(role.id, role.title, customer, payer, subscriber))
                
                phone = res.phone if (hasattr(res, 'phone')) else None
                email = res.email if (hasattr(res, 'email')) else None
                contact = crm.Contact(res.id, res.name, phone, email, roles)
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_entity_found', 'contact', contact),
                              self._mh.fromhere())           
                return contact
            
        except suds.WebFault as ex:
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(ex), self._mh.fromhere())
            return None      
        
    def create_contact(self, name, phone=None, email=None):
        """Method creates contact
        
        Args:
           name - string, mandatory
           phone - string, optional
           email - string, optional           
             
        Returns:
           id - int
                
        """          
        
        try:
            
            msg = 'name:{0}, phone:{1}, email:{2}'.format(name, phone, email)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'create_contact', msg), 
                          self._mh.fromhere())      
            
            self._client.set_options(headers={'SOAPAction': 'create_contact'})
            res = self._client.service.create_contact(name, phone, email)
            
            if (self.is_soap_fault(res)):
                self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
                return None
            else:
                id = res
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_entity_created', 'contact', id), 
                              self._mh.fromhere())           
                return id
            
        except suds.WebFault as ex:
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(ex), self._mh.fromhere())
            return None      
        
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
        
        try:
            
            msg = 'id:{0}, name:{1}, phone:{2}, email:{3}'.format(id, name, phone, email)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'change_contact', msg), 
                          self._mh.fromhere())       
            
            self._client.set_options(headers={'SOAPAction': 'change_contact'})
            res = self._client.service.change_contact(id, name, phone, email)
            
            if (self.is_soap_fault(res)):
                self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
                return False
            else:
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_entity_changed', 'contact', id), 
                              self._mh.fromhere())              
                return True
            
        except suds.WebFault as ex:
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(ex), self._mh.fromhere())
            return False 
        
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
        
        try:
            
            msg = 'id:{0}, role:{1}, customer:{2}, payer:{3}, subscriber:{4}'.format(
                   id, role, customer, payer, subscriber)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'assign_contact_role', msg), 
                          self._mh.fromhere())
            
            self._client.set_options(headers={'SOAPAction': 'assign_contact_role'})
            res = self._client.service.assign_contact_role(id, role, customer, payer, subscriber)
            
            if (self.is_soap_fault(res)):
                self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
                return False
            else:
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_role_assigned', 'contact'), 
                              self._mh.fromhere())           
                return True
            
        except suds.WebFault as ex:
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(ex), self._mh.fromhere())
            return False     
        
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
        
        try:
            
            msg = 'id:{0}, role:{1}, customer:{2}, payer:{3}, subscriber:{4}'.format(
                   id, role, customer, payer, subscriber)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'revoke_contact_role', msg), 
                          self._mh.fromhere())
            
            self._client.set_options(headers={'SOAPAction': 'revoke_contact_role'})
            res = self._client.service.revoke_contact_role(id, role, customer, payer, subscriber)
            
            if (self.is_soap_fault(res)):
                self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
                return False
            else:
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_role_revoked', 'contact'), 
                              self._mh.fromhere())                
                return True
            
        except suds.WebFault as ex:
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(ex), self._mh.fromhere())
            return False               
           
    def read_address(self, id):
        """Method reads address
        
        Args:
           id - int, mandatory            
             
        Returns:
           address - crm_entities.Address
                
        """          
        
        try:
            
            msg = 'id:{0}'.format(id)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'read_address', msg), 
                          self._mh.fromhere())
            
            self._client.set_options(headers={'SOAPAction': 'read_address'})
            res = self._client.service.read_address(id)
            
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
                        roles.append(crm.AddressRole(role.id, role.title, contact, customer, payer, subscriber))                
                
                address = crm.Address(res.id, res.street, res.street_no, res.city, res.zip, roles)
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_entity_found', 'address', address),
                              self._mh.fromhere())           
                return address
            
        except suds.WebFault as ex:
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(ex), self._mh.fromhere())
            return None      
        
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
        
        try:
            
            msg = 'street:{0}, street_no:{1}, city:{2}, zip:{3}'.format(street, street_no, city, zip)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'create_address', msg), 
                          self._mh.fromhere())  
            
            self._client.set_options(headers={'SOAPAction': 'create_address'})
            res = self._client.service.create_address(street, street_no, city, zip)
            
            if (self.is_soap_fault(res)):
                self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
                return None
            else:
                id = res
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_entity_created', 'address', id), 
                              self._mh.fromhere())           
                return id
            
        except suds.WebFault as ex:
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(ex), self._mh.fromhere())
            return None      
        
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
        
        try:
            
            msg = 'id:{0}, street:{1}, street_no:{2}, city:{3}, zip:{4}'.format(id, street, street_no, city, zip)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'change_address', msg), 
                          self._mh.fromhere())  
            
            self._client.set_options(headers={'SOAPAction': 'change_address'})
            res = self._client.service.change_address(id, street, street_no, city, zip)
            
            if (self.is_soap_fault(res)):
                self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
                return False
            else:
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_entity_changed', 'address', id), 
                              self._mh.fromhere())             
                return True
            
        except suds.WebFault as ex:
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(ex), self._mh.fromhere())
            return False          
        
    def assign_address_role(self, id, role, contact=None, customer=None, payer=None, subscriber=None):
        """Method assigns address role
        
        Args:
           id - int, mandatory
           role - string, mandatory, lov_address_role.title
           contact - int, madantory
           customer - int, optional
           payer - int, optional
           subscriber - int, optional          
             
        Returns:
           result - bool
                
        """          
        
        try:
            
            msg = 'id:{0}, role:{1}, contact:{2}, customer:{3}, payer:{4}, subscriber:{5}'.format(
                   id, role, contact, customer, payer, subscriber)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'assign_address_role', msg), 
                          self._mh.fromhere())
            
            self._client.set_options(headers={'SOAPAction': 'assign_address_role'})
            res = self._client.service.assign_address_role(id, role, contact, customer, payer, subscriber)
            
            if (self.is_soap_fault(res)):
                self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
                return False
            else:
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_role_assigned', 'address'), 
                              self._mh.fromhere())                
                return True
            
        except suds.WebFault as ex:
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(ex), self._mh.fromhere())
            return False     
        
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
        
        try:
            
            msg = 'id:{0}, role:{1}, contact:{2}, customer:{3}, payer:{4}, subscriber:{5}'.format(
                   id, role, contact, customer, payer, subscriber)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'revoke_address_role', msg), 
                          self._mh.fromhere())
            
            self._client.set_options(headers={'SOAPAction': 'revoke_address_role'})
            res = self._client.service.revoke_address_role(id, role, contact, customer, payer, subscriber)
            
            if (self.is_soap_fault(res)):
                self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
                return False
            else:
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_role_revoked', 'address'), 
                              self._mh.fromhere())          
                return True
            
        except suds.WebFault as ex:
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(ex), self._mh.fromhere())
            return False    
        
    def read_services(self, customer=None, payer=None, subscriber=None, service=None):
        """Method reads services
        
        Args:
           customer - int, optional
           payer - int, optional
           subscriber - int, optional
           service - int, optional, lov_service.id, default read all services for entity     
             
        Returns:
           services - list of crm_entities.Service
                
        """          
        
        try:
            
            msg = 'customer:{0}, payer:{1}, subscriber:{2}, service:{3}'.format(
                   customer, payer, subscriber, service)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'read_services', msg), 
                          self._mh.fromhere())
            
            self._client.set_options(headers={'SOAPAction': 'read_services'})
            res = self._client.service.read_services(customer, payer, subscriber, service)
            
            if (self.is_soap_fault(res)):
                self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
                return False
            else:
                
                services = []
                for service in res.service:
                   
                    params = {}
                    for param in service.params.entry:
                        params[param.key] = param.value
                
                    services.append(crm.Service(service.id, service.name, service.status, params))
            
                for service in services:    
                    self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_entity_found', 'service', service),
                                  self._mh.fromhere())
                    
            return services  
            
        except suds.WebFault as ex:
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(ex), self._mh.fromhere())
            return False       
        
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
        
        try:
            
            msg = 'service:{0}, customer:{1}, payer:{2}, subscriber:{3}, status:{4}, params:{5}'.format(
                   service, customer, payer, subscriber, status, params)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'create_service', msg), 
                          self._mh.fromhere())
            
            el_params = self._client.factory.create('params')            
            for key, value in params.items():
                entry = self._client.factory.create('entry')
                entry.key = key
                entry.value = value
                el_params.entry.append(entry)            
            
            self._client.set_options(headers={'SOAPAction': 'create_service'})
            res = self._client.service.create_service(service, customer, payer, subscriber, status, el_params)
            
            if (self.is_soap_fault(res)):
                self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
                return False
            else:
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_entity_created', 'service', service), 
                              self._mh.fromhere())          
                return True
            
        except suds.WebFault as ex:
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(ex), self._mh.fromhere())
            return False            
        
    def change_service(self, service, customer=None, payer=None, subscriber=None, status=None, params={}):
        """Method creates service
        
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
        
        try:
            
            msg = 'service:{0}, customer:{1}, payer:{2}, subscriber:{3}, status:{4}, params:{5}'.format(
                   service, customer, payer, subscriber, status, params)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_func', 'change_service', msg), 
                          self._mh.fromhere())
            
            el_params = self._client.factory.create('params')            
            for key, value in params.items():
                entry = self._client.factory.create('entry')
                entry.key = key
                entry.value = value
                el_params.entry.append(entry)                          
            
            self._client.set_options(headers={'SOAPAction': 'change_service'})
            res = self._client.service.change_service(service, customer, payer, subscriber, status, el_params)
            
            if (self.is_soap_fault(res)):
                self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(res), self._mh.fromhere())
                return False
            else:
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_entity_changed', 'service', service), 
                              self._mh.fromhere())              
                return True
            
        except suds.WebFault as ex:
            self._mh.dmsg('htk_on_extension_error', 'SOAP fault {0}'.format(ex), self._mh.fromhere())
            return False                                                    