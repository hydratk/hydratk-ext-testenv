# -*- coding: utf-8 -*-
"""CRM entity classes

.. module:: testenv.entities.crm_entities
   :platform: Unix
   :synopsis: CRM entity classes
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from lxml.etree import Element, SubElement
from simplejson import dumps

class Customer(object):   
    """Class Customer
    """
    
    def __init__(self, id, name, status, segment, birth_no=None, reg_no=None, tax_no=None):
        """Class constructor
    
        Customer entity   
    
        Args:
           id (int): customer id
           name (str): name
           status (str): status, active|deactive|suspend
           segment (int): segment id, 2|3|4|5 RES|VSE|SME|LE
           birth_no (str): birth number
           reg_no (str): registration number
           tax_no (str): tax identification number
           
        """                     
        
        self.id = id
        self.name = name
        self.status = status
        self.segment = segment
        self.birth_no = birth_no
        self.reg_no = reg_no
        self.tax_no = tax_no
        
    def __str__(self):
        """Method overrides __str__         
        """          
        
        s = u'id:{0}|name:{1}|status:{2}|segment:{3}'.format(self.id, self.name, self.status, self.segment) + \
            u'|birth_no:{0}|reg_no:{1}|tax_no:{2}'.format(self.birth_no, self.reg_no, self.tax_no)
        return s
    
    def toxml(self):
        """Method serializes customer to XML           
        """         
        
        root = Element('customer')
        
        SubElement(root, 'id').text = str(self.id)
        SubElement(root, 'name').text = self.name
        SubElement(root, 'status').text = self.status
        SubElement(root, 'segment').text = str(self.segment)
        if (self.birth_no != None):
            SubElement(root, 'birth_no').text = self.birth_no
        if (self.reg_no != None):
            SubElement(root, 'reg_no').text = self.reg_no
        if (self.tax_no != None):
            SubElement(root, 'tax_no').text = self.tax_no   
        
        return root
        
    def tojson(self): 
        """Method serializes customer to JSON           
        """            
        
        root = {}
        
        root['id'] = self.id
        root['name'] = self.name
        root['status'] = self.status
        root['segment'] = self.segment
        if (self.birth_no != None):
            root['birth_no'] = self.birth_no
        if (self.reg_no != None):
            root['reg_no'] = self.reg_no
        if (self.tax_no != None):
            root['tax_no'] = self.tax_no

        return dumps(root)           
    
class Payer(object):  
    """Class Payer
    """   
    
    def __init__(self, id, name, status, billcycle, customer, bank_account=None):
        """Class constructor
    
        Payer entity   
    
        Args:
           id (int): payer id
           name (str): name
           status (str): status, active|deactive|suspend
           billcycle (int): billcycle id, 1|2|3|4 51|52|53|54        
           bank_account (str): banking account
           customer (id): assigned customer id           
           
        """         
        
        self.id = id
        self.name = name
        self.status = status
        self.billcycle = billcycle
        self.bank_account = bank_account
        self.customer = customer
        
    def __str__(self):
        """Method overrides __str__         
        """         
        
        s = u'id:{0}|name:{1}|status:{2}|billcycle:{3}'.format(self.id, self.name, self.status, self.billcycle) + \
            u'|bank_account:{0}|customer:{1}'.format(self.bank_account, self.customer)  
        return s
    
    def toxml(self):
        """Method serializes payer to XML           
        """         
        
        root = Element('payer')
        
        SubElement(root, 'id').text = str(self.id)
        SubElement(root, 'name').text = self.name
        SubElement(root, 'status').text = self.status
        SubElement(root, 'billcycle').text = str(self.billcycle)
        if (self.bank_account != None):
            SubElement(root, 'bank_account').text = self.bank_account
        SubElement(root, 'customer').text = str(self.customer)
        
        return root
        
    def tojson(self):   
        """Method serializes payer to JSON           
        """         
        
        root = {}
        
        root['id'] = self.id
        root['name'] = self.name
        root['status'] = self.status
        root['billcycle'] = self.billcycle
        if (self.bank_account != None):
            root['bank_account'] = self.bank_account
        root['customer'] = self.customer

        return dumps(root)            
            
class Subscriber(object): 
    """Class Subscriber
    """     
    
    def __init__(self, id, name, msisdn, status, market, tariff, customer, payer):
        """Class constructor
    
        Subscriber entity   
    
        Args:
           id (int): subscriber id           
           name (str): name
           msisdn (str): MSISDN
           status (str): status, active|deactive|suspend
           market (int): market id, 1|2|3 GSM|DSL|FIX
           tariff (int): tariff id, 433|459|434|460
           customer (int): assigned customer id    
           payer (int): assigned payer id       
           
        """         
        
        self.id = id
        self.name = name
        self.msisdn = msisdn
        self.status = status
        self.market = market
        self.tariff = tariff
        self.customer = customer
        self.payer = payer
        
    def __str__(self):
        """Method overrides __str__         
        """         
        
        s = u'id:{0}|name:{1}|msisdn:{2}|status:{3}'.format(self.id, self.name, self.msisdn, self.status) + \
            u'|market:{0}|tariff:{1}|customer:{2}|payer:{3}'.format(self.market, self.tariff, self.customer, self.payer)
        return s
    
    def toxml(self):
        """Method serializes subscriber to XML           
        """          
        
        root = Element('subscriber')
        
        SubElement(root, 'id').text = str(self.id)
        SubElement(root, 'name').text = self.name
        SubElement(root, 'msisdn').text = self.msisdn
        SubElement(root, 'status').text = self.status
        SubElement(root, 'market').text = str(self.market)
        SubElement(root, 'tariff').text = str(self.tariff)
        SubElement(root, 'customer').text = str(self.customer)
        SubElement(root, 'payer').text = str(self.payer)
        
        return root
        
    def tojson(self):  
        """Method serializes subscriber to JSON           
        """           
        
        root = {}
        
        root['id'] = self.id
        root['name'] = self.name
        root['msisdn'] = self.msisdn           
        root['status'] = self.status
        root['market'] = self.market
        root['tariff'] = self.tariff
        root['customer'] = self.customer
        root['payer'] = self.payer

        return dumps(root)    
            
class Contact(object):    
    """Class Contact
    """ 
    
    def __init__(self, id, name, phone=None, email=None, roles=[]):
        """Class constructor
    
        Contact entity   
    
        Args:
           id (int): contact id           
           name (str): name 
           phone (str): phone number
           email (str): email
           roles (list): contact roles   
           
        """          
        
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email
        self.roles = roles
    
    def __str__(self):
        """Method overrides __str__         
        """         
        
        s = u'id:{0}|name:{1}|phone:{2}|email:{3}|roles#'.format(self.id, self.name, self.phone, self.email)
        
        if (len(self.roles) > 0):
            
            for role in self.roles:
                s += '{0}#'.format(role)        
        
        return s
    
    def toxml(self):
        """Method serializes contact to XML           
        """           
        
        root = Element('contact')
        
        SubElement(root, 'id').text = str(self.id)
        SubElement(root, 'name').text = self.name
        if (self.phone != None):
            SubElement(root, 'phone').text = self.phone
        if (self.email != None):
            SubElement(root, 'email').text = self.email
            
        if (len(self.roles) > 0):
            elem = SubElement(root, 'roles')
            
            for role in self.roles:
                elem.append(role.toxml())
                                  
        return root 
        
    def tojson(self):  
        """Method serializes contact to JSON           
        """            
        
        root = {}
        
        root['id'] = self.id
        root['name'] = self.name
        if (self.phone != None):
            root['phone'] = self.phone
        if (self.email != None):
            root['email'] = self.email 
                      
        if (len(self.roles) > 0): 
            el_roles = []
                                               
            for role in self.roles:  
                el_role = {'id': role.id, 'title': role.title,
                           'customer': role.customer, 'payer': role.payer,
                           'subscriber': role.subscriber}
                el_roles.append(el_role)           
  
            root['roles'] = {'role' : el_roles}              

        return dumps(root)      
        
class ContactRole(object):  
    """Class ContactRole
    """    
    
    def __init__(self, id, title, customer=None, payer=None, subscriber=None):
        """Class constructor
    
        Contact role entity   
    
        Args:
           id (int): contact id           
           title (str): role title, contract|contact|invoicing
           customer (int): assigned customer id
           payer (int): assigned payer id
           subscriber (int): assigned subscriber id 
           
        """         
        
        self.id = id
        self.title = title
        self.customer = customer
        self.payer = payer
        self.subscriber = subscriber
        
    def __str__(self):
        """Method overrides __str__         
        """         
        
        s = u'id:{0}|title:{1}|customer:{2}|payer:{3}'.format(self.id, self.title, self.customer, self.payer) + \
            u'|subscriber:{0}'.format(self.subscriber)
        return s
    
    def toxml(self):
        """Method serializes contact role to XML           
        """         
        
        root = Element('role')
        
        SubElement(root, 'id').text = str(self.id)
        SubElement(root, 'title').text = self.title
        if (self.customer != None):
            SubElement(root, 'customer').text = str(self.customer)
        if (self.payer != None):
            SubElement(root, 'payer').text = str(self.payer)
        if (self.subscriber != None):
            SubElement(root, 'subscriber').text = str(self.subscriber)
        
        return root
        
    def tojson(self): 
        """Method serializes contact role to JSON           
        """           
        
        root = {}
        
        root['id'] = self.id
        root['title'] = self.title
        if (self.customer != None):
            root['customer'] = self.customer
        if (self.payer != None):
            root['payer'] = self.payer
        if (self.subscriber != None):
            root['subscriber'] = self.subscriber

        return dumps(root)               
        
class Address(object):      
    """Class Address
    """ 
    
    def __init__(self, id, street, street_no, city, zip, roles={}):
        """Class constructor
    
        Address role entity   
    
        Args:
           id (int): address id           
           street (str): street
           street_no (str): street number
           city (str): city
           zip (int): zip code
           roles (list): address roles
           
        """         
        
        self.id = id
        self.street = street
        self.street_no = street_no
        self.city = city
        self.zip = zip
        self.roles = roles
        
    def __str__(self):
        """Method overrides __str__         
        """         
        
        s = u'id:{0}|street:{1}|street_no:{2}|city:{3}'.format(self.id, self.street, self.street_no, self.city) + \
            u'|zip:{0}|roles#'.format(self.zip)
            
        if (len(self.roles) > 0):
            
            for role in self.roles:
                s += '{0}#'.format(role)             
            
        return s
    
    def toxml(self):
        """Method serializes address to XML           
        """        
        
        root = Element('address')
        
        SubElement(root, 'id').text = str(self.id)
        SubElement(root, 'street').text = self.street
        SubElement(root, 'street_no').text = self.street_no
        SubElement(root, 'city').text = self.city
        SubElement(root, 'zip').text = str(self.zip) 
        
        if (len(self.roles) > 0):
            elem = SubElement(root, 'roles')
            
            for role in self.roles:
                elem.append(role.toxml())                 
                                  
        return root
        
    def tojson(self):   
        """Method serializes address to JSON           
        """        
        
        root = {}
        
        root['id'] = self.id
        root['street'] = self.street
        root['street_no'] = self.street_no
        root['city'] = self.city
        root['zip'] = self.zip      
            
        if (len(self.roles) > 0): 
            el_roles = []
                                               
            for role in self.roles:  
                el_role = {'id': role.id, 'title': role.title,
                           'contact': role.contact, 'customer': role.customer, 
                           'payer': role.payer, 'subscriber': role.subscriber}
                el_roles.append(el_role)                
  
            root['roles'] = {'role' : el_roles}                   

        return dumps(root)     
            
class AddressRole(object): 
    """Class AddressRole
    """
    
    def __init__(self, id, title, contact=None, customer=None, payer=None, subscriber=None):
        """Class constructor
    
        Address role entity   
    
        Args:
           id (int): address id           
           title (str): role title, contract|contact|invoicing|delivery
           contact (int): assigned contact id
           customer (int): assigned customer id
           payer (int): assigned payer id
           subscriber (int): assigned subscriber id 
           
        """          
        
        self.id = id
        self.title = title
        self.contact = contact
        self.customer = customer
        self.payer = payer
        self.subscriber = subscriber

    def __str__(self):
        """Method overrides __str__         
        """         
        
        s = u'id:{0}|title:{1}|contact:{2}|customer:{3}'.format(self.id, self.title, self.contact, self.customer) + \
            u'|payer:{0}|subscriber:{1}'.format(self.payer, self.subscriber)
        return s
    
    def toxml(self):
        """Method serializes address role to XML           
        """         
        
        root = Element('role')
        
        SubElement(root, 'id').text = str(self.id)
        SubElement(root, 'title').text = self.title
        if (self.contact != None):
            SubElement(root, 'contact').text = str(self.contact)
        if (self.customer != None):
            SubElement(root, 'customer').text = str(self.customer)
        if (self.payer != None):
            SubElement(root, 'payer').text = str(self.payer)
        if (self.subscriber != None):
            SubElement(root, 'subscriber').text = str(self.subscriber)
        
        return root 
        
    def tojson(self):   
        """Method serializes address role to JSON           
        """         
        
        root = {}
        
        root['id'] = self.id
        root['title'] = self.title
        if (self.contact != None):
            root['contact'] = self.contact           
        if (self.customer != None):
            root['customer'] = self.customer
        if (self.payer != None):
            root['payer'] = self.payer
        if (self.subscriber != None):
            root['subscriber'] = self.subscriber

        return dumps(root)         
    
class Service(object):   
    """Class Service
    """   
    
    def __init__(self, id, name, status, params={}):
        """Class constructor
    
        Service entity   
    
        Args:
           id (int): service id           
           name (str): name
           status (str): status, active|deactive|suspend
           params (dict): parameters
           
        """           
        
        self.id = id
        self.name = name
        self.status = status
        self.params = params
    
    def __str__(self):
        """Method overrides __str__         
        """         
        
        s = u'id:{0}|name:{1}|status:{2}|params#'.format(self.id, self.name, self.status)
        
        if (len(self.params) > 0):
            
            for key, value in self.params.items():
                s += '{0}:{1}#'.format(key, value)
                
        return s
    
    def toxml(self):
        """Method serializes service to XML           
        """           
        
        root = Element('service')
        
        SubElement(root, 'id').text = str(self.id)
        SubElement(root, 'name').text = self.name
        SubElement(root, 'status').text = self.status
        
        elem = SubElement(root, 'params')
        for key, value in self.params.items():
            el_param = Element('entry')
            SubElement(el_param, 'key').text = str(key)
            SubElement(el_param, 'value').text = value
            elem.append(el_param)
        
        return root
    
    def tojson(self):
        """Method serializes service to JSON           
        """           
        
        root = {}
        
        root['id'] = self.id
        root['name'] = self.name
        root['status'] = self.status
                
        el_params = []             
        for key, value in self.params.items():  
            param = {} 
            param['key'] = key
            param['value'] = value
            el_params.append(param)           
  
        root['params'] = {'entry' : el_params} 
        
        return dumps(root)        
    
class ServiceOperation(object): 
    """Class ServiceOperation
    """    
    
    def __init__(self, service, customer=None, payer=None, subscriber=None, status=None, params={}):
        """Class constructor
    
        Service operation entity   
    
        Args:
           service (int): service id
           customer (int): assigned customer id
           payer (int): assigned payer id
           subscriber (int): assigned subscriber id
           status (str): service status, active|deactive|suspend
           params (dict): service parameters
           
        """          
        
        self.service = service
        self.customer = customer
        self.payer = payer
        self.subscriber = subscriber        
        self.status = status
        self.params = params  
        
    def __str__(self):
        """Method overrides __str__         
        """         
        
        s = u'service:{0}|customer:{1}|payer:{2}'.format(self.service, self.customer, self.payer) + \
            u'|subscriber:{0}|status:{1}|params#'.format(self.subscriber, self.status)
        
        if (len(self.params) > 0):
            
            for key, value in self.params.items():
                s += '{0}:{1}#'.format(key, value)
                
        return s 
    
    def toxml(self):
        """Method serializes service operation to XML           
        """           
        
        root = Element('operation')
        
        SubElement(root, 'service').text = str(self.service)
        if (self.customer != None):
            SubElement(root, 'customer').text = str(self.customer)
        if (self.payer != None):
            SubElement(root, 'payer').text = str(self.payer)
        if (self.subscriber != None):
            SubElement(root, 'subscriber').text = str(self.subscriber)
        if (self.status != None):
            SubElement(root, 'status').text = self.status  
             
        elParams = SubElement(root, 'params')
            
        for key, value in self.params.items():
            elParam = SubElement(elParams, 'entry')
            elem = SubElement(elParam, 'key')
            elem.text = str(key)    
            elem = SubElement(elParam, 'value')
            elem.text = str(value)  
            
        return root
        
    def tojson(self):
        """Method serializes service operation to JSON           
        """           
        
        root = {}
        
        root['service'] = self.service
        if (self.customer != None):
            root['customer'] = self.customer
        if (self.payer != None):
            root['payer'] = self.payer
        if (self.subscriber != None):
            root['subscriber'] = self.subscriber
        if (self.status != None):
            root['status'] = self.status  
                
        el_params = []             
        for key, value in self.params.items():  
            param = {} 
            param['key'] = key
            param['value'] = value
            el_params.append(param)           
  
        root['params'] = {'entry' : el_params} 
        
        return dumps(root)                                          