# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.extensions.testenv.entities.crm_entities
   :platform: Unix
   :synopsis: CRM entities for testenv
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

import lxml.etree as e;
import jsonlib2

class Customer:
    """Customer entity class
        
        Args:
           id - int, mandatory
           name - string, mandatory
           status - string, mandatory
           segment - int, mandatory           
           birth_no - string, optional
           reg_no - string, optional
           tax_no - string, optional              
                
    """     
    
    def __init__(self, id, name, status, segment, birth_no=None, reg_no=None, tax_no=None):
        
        self.id = id;
        self.name = name;
        self.status = status;
        self.segment = segment;
        self.birth_no = birth_no;
        self.reg_no = reg_no;
        self.tax_no = tax_no;
        
    def __str__(self):
        
        s = u'id:{0}|name:{1}|status:{2}|segment:{3}'.format(self.id, self.name, self.status, self.segment) + \
            u'|birth_no:{0}|reg_no:{1}|tax_no:{2}'.format(self.birth_no, self.reg_no, self.tax_no);
        return s;
    
    def toxml(self):
        
        root = e.Element('customer');
        
        e.SubElement(root, 'id').text = str(self.id);
        e.SubElement(root, 'name').text = self.name;
        e.SubElement(root, 'status').text = self.status;
        e.SubElement(root, 'segment').text = str(self.segment);
        if (self.birth_no != None):
            e.SubElement(root, 'birth_no').text = self.birth_no;
        if (self.reg_no != None):
            e.SubElement(root, 'reg_no').text = self.reg_no;
        if (self.tax_no != None):
            e.SubElement(root, 'tax_no').text = self.tax_no;   
        
        return root;
        
    def tojson(self):   
        
        root = {}
        
        root['id'] = self.id;
        root['name'] = self.name;
        root['status'] = self.status;
        root['segment'] = self.segment;
        if (self.birth_no != None):
            root['birth_no'] = self.birth_no;
        if (self.reg_no != None):
            root['reg_no'] = self.reg_no;
        if (self.tax_no != None):
            root['tax_no'] = self.tax_no;

        return jsonlib2.write(root);           
    
class Payer:
    """Payer entity class
        
        Args:
           id - int, mandatory
           name - string, mandatory
           status - string, mandatory
           billcycle - int, mandatory
           bank_account - string, optional
           customer - int, mandatory       
                
    """     
    
    def __init__(self, id, name, status, billcycle, customer, bank_account=None):
        
        self.id = id;
        self.name = name;
        self.status = status;
        self.billcycle = billcycle;
        self.bank_account = bank_account;
        self.customer = customer;
        
    def __str__(self):
        
        s = u'id:{0}|name:{1}|status:{2}|billcycle:{3}'.format(self.id, self.name, self.status, self.billcycle) + \
            u'|bank_account:{0}|customer:{1}'.format(self.bank_account, self.customer);  
        return s;
    
    def toxml(self):
        
        root = e.Element('payer');
        
        e.SubElement(root, 'id').text = str(self.id);
        e.SubElement(root, 'name').text = self.name;
        e.SubElement(root, 'status').text = self.status;
        e.SubElement(root, 'billcycle').text = str(self.billcycle);
        if (self.bank_account != None):
            e.SubElement(root, 'bank_account').text = self.bank_account;
        e.SubElement(root, 'customer').text = str(self.customer);
        
        return root;
        
    def tojson(self):   
        
        root = {}
        
        root['id'] = self.id;
        root['name'] = self.name;
        root['status'] = self.status;
        root['billcycle'] = self.billcycle;
        if (self.bank_account != None):
            root['bank_account'] = self.bank_account;
        root['customer'] = self.customer;

        return jsonlib2.write(root);            
            
class Subscriber:
    """Subscriber entity class
        
        Args:
           id - int, mandatory
           name - string, mandatory
           msisdn - string, mandatory
           status - string, mandatory
           market - int, mandatory
           tariff - int, mandatory
           customer - int, mandatory
           payer - int, mandatory       
                
    """        
    
    def __init__(self, id, name, msisdn, status, market, tariff, customer, payer):
        
        self.id = id;
        self.name = name;
        self.msisdn = msisdn;
        self.status = status;
        self.market = market;
        self.tariff = tariff;
        self.customer = customer;
        self.payer = payer;
        
    def __str__(self):
        
        s = u'id:{0}|name:{1}|msisdn:{2}|status:{3}'.format(self.id, self.name, self.msisdn, self.status) + \
            u'|market:{0}|tariff:{1}|customer:{2}|payer:{3}'.format(self.market, self.tariff, self.customer, self.payer);
        return s;
    
    def toxml(self):
        
        root = e.Element('subscriber')
        
        e.SubElement(root, 'id').text = str(self.id);
        e.SubElement(root, 'name').text = self.name;
        e.SubElement(root, 'msisdn').text = self.msisdn;
        e.SubElement(root, 'status').text = self.status;
        e.SubElement(root, 'market').text = str(self.market);
        e.SubElement(root, 'tariff').text = str(self.tariff);
        e.SubElement(root, 'customer').text = str(self.customer);
        e.SubElement(root, 'payer').text = str(self.payer);
        
        return root;
        
    def tojson(self):   
        
        root = {}
        
        root['id'] = self.id;
        root['name'] = self.name;
        root['msisdn'] = self.msisdn;           
        root['status'] = self.status;
        root['market'] = self.market;
        root['tariff'] = self.tariff;
        root['customer'] = self.customer;
        root['payer'] = self.payer;

        return jsonlib2.write(root);    
            
class Contact:
    """Contact entity class
        
        Args:
           id - int, mandatory
           name - string, mandatory
           phone - string, optional
           email - string, optional
           roles - list of ContactRole, optional     
                
    """        
    
    def __init__(self, id, name, phone=None, email=None, roles=[]):
        
        self.id = id;
        self.name = name;
        self.phone = phone;
        self.email = email;
        self.roles = roles;
    
    def __str__(self):
        
        s = u'id:{0}|name:{1}|phone:{2}|email:{3}|roles#'.format(self.id, self.name, self.phone, self.email);
        
        if (len(self.roles) > 0):
            
            for role in self.roles:
                s += '{0}#'.format(role);        
        
        return s;
    
    def toxml(self):
        
        root = e.Element('contact')
        
        e.SubElement(root, 'id').text = str(self.id);
        e.SubElement(root, 'name').text = self.name;
        if (self.phone != None):
            e.SubElement(root, 'phone').text = self.phone;
        if (self.email != None):
            e.SubElement(root, 'email').text = self.email;
            
        if (len(self.roles) > 0):
            elem = e.SubElement(root, 'roles');
            
            for role in self.roles:
                elem.append(role.toxml());
                                  
        return root; 
        
    def tojson(self):   
        
        root = {}
        
        root['id'] = self.id;
        root['name'] = self.name;
        if (self.phone != None):
            root['phone'] = self.phone;
        if (self.email != None):
            root['email'] = self.email; 
                      
        if (len(self.roles) > 0): 
            el_roles = [];
                                               
            for role in self.roles:  
                el_role = {'id': role.id, 'title': role.title,
                           'customer': role.customer, 'payer': role.payer,
                           'subscriber': role.subscriber};
                el_roles.append(el_role);           
  
            root['roles'] = {'role' : el_roles};              

        return jsonlib2.write(root);      
        
class ContactRole:
    """ContactRole entity class
        
        Args:
           id - int, mandatory
           title - string, mandatory
           customer - int, optional
           payer - int, optional
           subscriber - int, optional     
                
    """        
    
    def __init__(self, id, title, customer=None, payer=None, subscriber=None):
        
        self.id = id;
        self.title = title;
        self.customer = customer;
        self.payer = payer;
        self.subscriber = subscriber;
        
    def __str__(self):
        
        s = u'id:{0}|title:{1}|customer:{2}|payer:{3}'.format(self.id, self.title, self.customer, self.payer) + \
            u'|subscriber:{0}'.format(self.subscriber);
        return s;
    
    def toxml(self):
        
        root = e.Element('role');
        
        e.SubElement(root, 'id').text = str(self.id);
        e.SubElement(root, 'title').text = self.title;
        if (self.customer != None):
            e.SubElement(root, 'customer').text = str(self.customer);
        if (self.payer != None):
            e.SubElement(root, 'payer').text = str(self.payer);
        if (self.subscriber != None):
            e.SubElement(root, 'subscriber').text = str(self.subscriber);
        
        return root;
        
    def tojson(self):   
        
        root = {}
        
        root['id'] = self.id;
        root['title'] = self.title;
        if (self.customer != None):
            root['customer'] = self.customer;
        if (self.payer != None):
            root['payer'] = self.payer;
        if (self.subscriber != None):
            root['subscriber'] = self.subscriber;

        return jsonlib2.write(root);               
        
class Address:
    """Address entity class
        
        Args:
           id - int, mandatory
           street - string, mandatory
           street_no - string, mandatory
           city - string, mandatory
           zip - int, mandatory
           roles - list of AddressRole, optional      
                
    """        
    
    def __init__(self, id, street, street_no, city, zip, roles={}):
        
        self.id = id;
        self.street = street;
        self.street_no = street_no;
        self.city = city;
        self.zip = zip;
        self.roles = roles;
        
    def __str__(self):
        
        s = u'id:{0}|street:{1}|street_no:{2}|city:{3}'.format(self.id, self.street, self.street_no, self.city) + \
            u'|zip:{0}|roles#'.format(self.zip);
            
        if (len(self.roles) > 0):
            
            for role in self.roles:
                s += '{0}#'.format(role);             
            
        return s;
    
    def toxml(self):
        
        root = e.Element('address')
        
        e.SubElement(root, 'id').text = str(self.id);
        e.SubElement(root, 'street').text = self.street;
        e.SubElement(root, 'street_no').text = self.street_no;
        e.SubElement(root, 'city').text = self.city;
        e.SubElement(root, 'zip').text = str(self.zip); 
        
        if (len(self.roles) > 0):
            elem = e.SubElement(root, 'roles');
            
            for role in self.roles:
                elem.append(role.toxml());                 
                                  
        return root;
        
    def tojson(self):   
        
        root = {}
        
        root['id'] = self.id;
        root['street'] = self.street;
        root['street_no'] = self.street_no;
        root['city'] = self.city;
        root['zip'] = self.zip;      
            
        if (len(self.roles) > 0): 
            el_roles = [];
                                               
            for role in self.roles:  
                el_role = {'id': role.id, 'title': role.title,
                           'contact': role.contact, 'customer': role.customer, 
                           'payer': role.payer, 'subscriber': role.subscriber};
                el_roles.append(el_role);                
  
            root['roles'] = {'role' : el_roles};                   

        return jsonlib2.write(root);     
            
class AddressRole:
    """AddressRole entity class
        
        Args:
           id - int, mandatory
           title - string, mandatory
           contact - int, optional
           customer - int, optional
           payer - int, optional
           subscriber - int, optional     
                
    """        
    
    def __init__(self, id, title, contact=None, customer=None, payer=None, subscriber=None):
        
        self.id = id;
        self.title = title;
        self.contact = contact;
        self.customer = customer;
        self.payer = payer;
        self.subscriber = subscriber;

    def __str__(self):
        
        s = u'id:{0}|title:{1}|contact:{2}|customer:{3}'.format(self.id, self.title, self.contact, self.customer) + \
            u'|payer:{0}|subscriber:{1}'.format(self.payer, self.subscriber);
        return s;
    
    def toxml(self):
        
        root = e.Element('role')
        
        e.SubElement(root, 'id').text = str(self.id);
        e.SubElement(root, 'title').text = self.title;
        if (self.contact != None):
            e.SubElement(root, 'contact').text = str(self.contact);
        if (self.customer != None):
            e.SubElement(root, 'customer').text = str(self.customer);
        if (self.payer != None):
            e.SubElement(root, 'payer').text = str(self.payer);
        if (self.subscriber != None):
            e.SubElement(root, 'subscriber').text = str(self.subscriber);
        
        return root; 
        
    def tojson(self):   
        
        root = {}
        
        root['id'] = self.id;
        root['title'] = self.title;
        if (self.contact != None):
            root['contact'] = self.contact;           
        if (self.customer != None):
            root['customer'] = self.customer;
        if (self.payer != None):
            root['payer'] = self.payer;
        if (self.subscriber != None):
            root['subscriber'] = self.subscriber;

        return jsonlib2.write(root);         
    
class Service:
    """Service entity class
        
        Args:
           id - int, mandatory
           name - string, mandatory
           status - string, mandatory
           params - dictionary key:value, optional      
                
    """        
    
    def __init__(self, id, name, status, params={}):
        
        self.id = id;
        self.name = name;
        self.status = status;
        self.params = params;
    
    def __str__(self):
        
        s = u'id:{0}|name:{1}|status:{2}|params#'.format(self.id, self.name, self.status);
        
        if (len(self.params) > 0):
            
            for key, value in self.params.items():
                s += '{0}:{1}#'.format(key, value);
                
        return s;
    
    def toxml(self):
        
        root = e.Element('service');
        
        e.SubElement(root, 'id').text = str(self.id);
        e.SubElement(root, 'name').text = self.name;
        e.SubElement(root, 'status').text = self.status;
        
        elem = e.SubElement(root, 'params');
        for key, value in self.params.items():
            el_param = e.Element('entry');
            e.SubElement(el_param, 'key').text = str(key);
            e.SubElement(el_param, 'value').text = value;
            elem.append(el_param);
        
        return root;
    
    def tojson(self):
        
        root = {}
        
        root['id'] = self.id;
        root['name'] = self.name;
        root['status'] = self.status;
                
        el_params = [];             
        for key, value in self.params.items():  
            param = {}; 
            param['key'] = key;
            param['value'] = value;
            el_params.append(param);           
  
        root['params'] = {'entry' : el_params}; 
        
        return jsonlib2.write(root);        
    
class ServiceOperation:
    """ServiceOperation entity class
        
        Args:
           service - int, mandatory
           customer - int, optional
           payer - int, optional
           subscriber - int, optional
           status - string, optional
           params - dictionary key:value, optional      
                
    """        
    
    def __init__(self, service, customer=None, payer=None, subscriber=None, status=None, params={}):
        
        self.service = service;
        self.customer = customer;
        self.payer = payer;
        self.subscriber = subscriber;        
        self.status = status;
        self.params = params;  
        
    def __str__(self):
        
        s = u'service:{0}|customer:{1}|payer:{2}'.format(self.service, self.customer, self.payer) + \
            u'|subscriber:{0}|status:{1}|params#'.format(self.subscriber, self.status);
        
        if (len(self.params) > 0):
            
            for key, value in self.params.items():
                s += '{0}:{1}#'.format(key, value);
                
        return s; 
    
    def toxml(self):
        
        root = e.Element('operation');
        
        e.SubElement(root, 'service').text = str(self.service);
        if (self.customer != None):
            e.SubElement(root, 'customer').text = str(self.customer);
        if (self.payer != None):
            e.SubElement(root, 'payer').text = str(self.payer);
        if (self.subscriber != None):
            e.SubElement(root, 'subscriber').text = str(self.subscriber);
        if (self.status != None):
            e.SubElement(root, 'status').text = self.status;  
             
        elParams = e.SubElement(root, 'params');
            
        for key, value in self.params.items():
            elParam = e.SubElement(elParams, 'entry');
            elem = e.SubElement(elParam, 'key');
            elem.text = str(key);    
            elem = e.SubElement(elParam, 'value');
            elem.text = str(value);  
            
        return root;
        
    def tojson(self):
        
        root = {}
        
        root['service'] = self.service;
        if (self.customer != None):
            root['customer'] = self.customer;
        if (self.payer != None):
            root['payer'] = self.payer;
        if (self.subscriber != None):
            root['subscriber'] = self.subscriber;
        if (self.status != None):
            root['status'] = self.status;  
                
        el_params = [];             
        for key, value in self.params.items():  
            param = {}; 
            param['key'] = key;
            param['value'] = value;
            el_params.append(param);           
  
        root['params'] = {'entry' : el_params}; 
        
        return jsonlib2.write(root);                                          