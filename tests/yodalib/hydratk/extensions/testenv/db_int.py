# -*- coding: utf-8 -*-
"""DB interface methods to be used in helpers

.. module:: yodalib.testenv.db_int
   :platform: Unix
   :synopsis: DB interface methods
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.extensions.testenv.db_handler import DbHandler
from hydratk.extensions.testenv.entities import Customer, Payer, Subscriber, Service
from hydratk.extensions.testenv.entities import Contact, ContactRole, Address, AddressRole

class DB_INT(object):
    
    _db = None
    
    def __init__(self):         
        
        self._db = DbHandler()  
        
    def connect(self):
        
        return self._db.connect()
    
    def disconnect(self):
        
        return self._db.disconnect() 
    
    def read_customer(self, id):
        
        return self._db.read_customer(id)
    
    def create_customer(self, name, segment, status='active', birth_no=None, reg_no=None, tax_no=None):
        
        return self._db.create_customer(name, segment, status, birth_no, reg_no, tax_no)
    
    def change_customer(self, id, name=None, status=None, segment=None, birth_no=None, reg_no=None, tax_no=None):
        
        return self._db.change_customer(id, name, status, segment, birth_no, reg_no, tax_no)  
    
    def read_payer(self, id):
        
        return self._db.read_payer(id)     
    
    def create_payer(self, name, billcycle, customer, status='active', bank_account=None):
        
        return self._db.create_payer(name, billcycle, customer, status, bank_account)
    
    def change_payer(self, id, name=None, status=None, billcycle=None, bank_account=None, customer=None):
        
        return self._db.change_payer(id, name, status, billcycle, bank_account, customer) 
    
    def read_subscriber(self, id):
        
        return self._db.read_subscriber(id)  
    
    def create_subscriber(self, name, msisdn, market, tariff, customer, payer, status='active'):
        
        return self._db.create_subscriber(name, msisdn, market, tariff, customer, payer, status)
    
    def change_subscriber(self, id, name=None, msisdn=None, status=None, market=None, tariff=None, customer=None, payer=None):
        
        return self._db.change_subscriber(id, name, msisdn, status, market, tariff, customer, payer)      
    
    def read_contact(self, id):
        
        return self._db.read_contact(id) 
    
    def create_contact(self, name, phone=None, email=None):
        
        return self._db.create_contact(name, phone, email)
    
    def change_contact(self, id, name=None, phone=None, email=None):
        
        return self._db.change_contact(id, name, phone, email)
    
    def assign_contact_role(self, id, role, customer=None, payer=None, subscriber=None):
        
        return self._db.assign_contact_role(id, role, customer, payer, subscriber)    
    
    def revoke_contact_role(self, id, role, customer=None, payer=None, subscriber=None):
        
        return self._db.revoke_contact_role(id, role, customer, payer, subscriber)   
    
    def read_address(self, id):
        
        return self._db.read_address(id) 
    
    def create_address(self, street, street_no, city, zip):
        
        return self._db.create_address(street, street_no, city, zip)
    
    def change_address(self, id, street=None, street_no=None, city=None, zip=None):
        
        return self._db.change_address(id, street, street_no, city, zip)
    
    def assign_address_role(self, id, role, contact=None, customer=None, payer=None, subscriber=None):
        
        return self._db.assign_address_role(id, role, contact, customer, payer, subscriber)    
    
    def revoke_address_role(self, id, role, contact=None, customer=None, payer=None, subscriber=None):
        
        return self._db.revoke_address_role(id, role, contact, customer, payer, subscriber)    
    
    def read_services(self, customer=None, payer=None, subscriber=None, service=None):    
        
        return self._db.read_services(customer, payer, subscriber, service)
    
    def create_service(self, service, customer=None, payer=None, subscriber=None, status='active', params={}):
        
        return self._db.create_service(service, customer, payer, subscriber, status, params)
    
    def change_service(self, service, customer=None, payer=None, subscriber=None, status=None, params={}):
        
        return self._db.change_service(service, customer, payer, subscriber, status, params)                       