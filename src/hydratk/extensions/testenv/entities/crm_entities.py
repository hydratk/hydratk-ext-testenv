# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.extensions.testenv.entities.crm_entities
   :platform: Unix
   :synopsis: CRM entities for testenv
.. moduleauthor:: Petr Rašek <pr@hydratk.org>

"""

import lxml.etree
import jsonlib2

class Customer:
    
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
    
    def toxml(self, declaration=False):
        
        root = lxml.etree.Element('customer');
        
        if (self.id != None):
            elem = lxml.etree.SubElement(root, 'id');
            elem.text = str(self.id);
        if (self.name != None):
            elem = lxml.etree.SubElement(root, 'name');
            elem.text = self.name;
        if (self.status != None):
            elem = lxml.etree.SubElement(root, 'status');
            elem.text = self.status;
        if (self.segment != None):
            elem = lxml.etree.SubElement(root, 'segment');
            elem.text = str(self.segment);
        if (self.birth_no != None):
            elem = lxml.etree.SubElement(root, 'birth_no');
            elem.text = self.birth_no;
        if (self.reg_no != None):
            elem = lxml.etree.SubElement(root, 'reg_no');
            elem.text = self.reg_no;
        if (self.tax_no != None):
            elem = lxml.etree.SubElement(root, 'tax_no');
            elem.text = self.tax_no;   
        
        if (declaration):    
            return lxml.etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True); 
        else:
            return lxml.etree.tostring(root);
        
    def tojson(self):   
        
        root = {}
        
        if (self.id != None):
            root['id'] = self.id;
        if (self.name != None):
            root['name'] = self.name;
        if (self.status != None):
            root['status'] = self.status;
        if (self.segment != None):
            root['segment'] = self.segment;
        if (self.birth_no != None):
            root['birth_no'] = self.birth_no;
        if (self.reg_no != None):
            root['reg_no'] = self.reg_no;
        if (self.tax_no != None):
            root['tax_no'] = self.tax_no;

        return jsonlib2.write(root);           
    
class Payer:
    
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
    
    def toxml(self, declaration=False):
        
        root = lxml.etree.Element('payer');
        
        if (self.id != None):
            elem = lxml.etree.SubElement(root, 'id');
            elem.text = str(self.id);
        if (self.name != None):
            elem = lxml.etree.SubElement(root, 'name');
            elem.text = self.name;
        if (self.status != None):
            elem = lxml.etree.SubElement(root, 'status');
            elem.text = self.status;
        if (self.billcycle != None):
            elem = lxml.etree.SubElement(root, 'billcycle');
            elem.text = str(self.billcycle);
        if (self.bank_account != None):
            elem = lxml.etree.SubElement(root, 'bank_account');
            elem.text = self.bank_account;
        if (self.customer != None):
            elem = lxml.etree.SubElement(root, 'customer');
            elem.text = str(self.customer);
        
        if (declaration):    
            return lxml.etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True); 
        else:
            return lxml.etree.tostring(root); 
        
    def tojson(self):   
        
        root = {}
        
        if (self.id != None):
            root['id'] = self.id;
        if (self.name != None):
            root['name'] = self.name;
        if (self.status != None):
            root['status'] = self.status;
        if (self.billcycle != None):
            root['billcycle'] = self.billcycle;
        if (self.bankAccount != None):
            root['bank_account'] = self.bank_account;
        if (self.customer != None):
            root['customer'] = self.customer;

        return jsonlib2.write(root);            
            
class Subscriber:
    
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
    
    def toxml(self, declaration=False):
        
        root = lxml.etree.Element('subscriber')
        
        if (self.id != None):
            elem = lxml.etree.SubElement(root, 'id');
            elem.text = str(self.id);
        if (self.name != None):
            elem = lxml.etree.SubElement(root, 'name');
            elem.text = self.name;
        if (self.msisdn != None):
            elem = lxml.etree.SubElement(root, 'msisdn');
            elem.text = self.msisdn;
        if (self.status != None):
            elem = lxml.etree.SubElement(root, 'status');
            elem.text = self.status;
        if (self.market != None):
            elem = lxml.etree.SubElement(root, 'market');
            elem.text = str(self.market);
        if (self.tariff != None):
            elem = lxml.etree.SubElement(root, 'tariff');
            elem.text = str(self.tariff);
        if (self.customer != None):
            elem = lxml.etree.SubElement(root, 'customer');
            elem.text = str(self.customer);
        if (self.payer != None):
            elem = lxml.etree.SubElement(root, 'payer');
            elem.text = str(self.payer);
        
        if (declaration):    
            return lxml.etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True);
        else:
            return lxml.etree.tostring(root);
        
    def tojson(self):   
        
        root = {}
        
        if (self.id != None):
            root['id'] = self.id;
        if (self.name != None):
            root['name'] = self.name;
        if (self.msisdn != None):
            root['msisdn'] = self.msisdn;           
        if (self.status != None):
            root['status'] = self.status;
        if (self.market != None):
            root['market'] = self.market;
        if (self.tariff != None):
            root['tariff'] = self.tariff;
        if (self.customer != None):
            root['customer'] = self.customer;
        if (self.payer != None):
            root['payer'] = self.payer;

        return jsonlib2.write(root);    
            
class Contact:
    
    def __init__(self, id, name, phone=None, email=None, roles={}):
        
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
    
    def toxml(self, declaration=False):
        
        root = lxml.etree.Element('contact')
        
        if (self.id != None):
            elem = lxml.etree.SubElement(root, 'id');
            elem.text = str(self.id);
        if (self.name != None):
            elem = lxml.etree.SubElement(root, 'name');
            elem.text = self.name;
        if (self.phone != None):
            elem = lxml.etree.SubElement(root, 'phone');
            elem.text = self.phone;
        if (self.email != None):
            elem = lxml.etree.SubElement(root, 'email');
            elem.text = self.email;
                                  
        if (declaration):    
            return lxml.etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True);
        else:
            return lxml.etree.tostring(root); 
        
    def tojson(self):   
        
        root = {}
        
        if (self.id != None):
            root['id'] = self.id;
        if (self.name != None):
            root['name'] = self.name;
        if (self.phone != None):
            root['phone'] = self.phone;
        if (self.email != None):
            root['email'] = self.email;       

        return jsonlib2.write(root);      
        
class ContactRole:
    
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
    
    def toxml(self, declaration=False):
        
        root = lxml.etree.Element('role');
        
        if (self.id != None):
            elem = lxml.etree.SubElement(root, 'id');
            elem.text = str(self.id);
        if (self.title != None):
            elem = lxml.etree.SubElement(root, 'title');
            elem.text = self.title;
        if (self.customer != None):
            elem = lxml.etree.SubElement(root, 'customer');
            elem.text = str(self.customer);
        if (self.payer != None):
            elem = lxml.etree.SubElement(root, 'payer');
            elem.text = str(self.payer);
        if (self.subscriber != None):
            elem = lxml.etree.SubElement(root, 'subscriber');
            elem.text = str(self.subscriber);
        
        if (declaration):    
            return lxml.etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True); 
        else:
            return lxml.etree.tostring(root); 
        
    def tojson(self):   
        
        root = {}
        
        if (self.id != None):
            root['id'] = self.id;
        if (self.title != None):
            root['title'] = self.title;
        if (self.customer != None):
            root['customer'] = self.customer;
        if (self.payer != None):
            root['payer'] = self.payer;
        if (self.subscriber != None):
            root['subscriber'] = self.subscriber;

        return jsonlib2.write(root);               
        
class Address:
    
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
    
    def toxml(self, declaration=False):
        
        root = lxml.etree.Element('address')
        
        if (self.id != None):
            elem = lxml.etree.SubElement(root, 'id');
            elem.text = str(self.id);
        if (self.street != None):
            elem = lxml.etree.SubElement(root, 'street');
            elem.text = self.street;
        if (self.street_no != None):
            elem = lxml.etree.SubElement(root, 'street_no');
            elem.text = self.street_no;
        if (self.city != None):
            elem = lxml.etree.SubElement(root, 'city');
            elem.text = self.city;
        if (self.zip != None):
            elem = lxml.etree.SubElement(root, 'zip');
            elem.text = str(self.zip);           
                                  
        if (declaration):    
            return lxml.etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True); 
        else:
            return lxml.etree.tostring(root); 
        
    def tojson(self):   
        
        root = {}
        
        if (self.id != None):
            root['id'] = self.id;
        if (self.street != None):
            root['street'] = self.street;
        if (self.streetNo != None):
            root['street_no'] = self.street_no;
        if (self.city != None):
            root['city'] = self.city;
        if (self.zip != None):
            root['zip'] = self.zip;            

        return jsonlib2.write(root);     
            
class AddressRole:
    
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
    
    def toxml(self, declaration=False):
        
        root = lxml.etree.Element('role')
        
        if (self.id != None):
            elem = lxml.etree.SubElement(root, 'id');
            elem.text = str(self.id);
        if (self.title != None):
            elem = lxml.etree.SubElement(root, 'title');
            elem.text = self.title;
        if (self.contact != None):
            elem = lxml.etree.SubElement(root, 'contact');
            elem.text = str(self.contact);
        if (self.customer != None):
            elem = lxml.etree.SubElement(root, 'customer');
            elem.text = str(self.customer);
        if (self.payer != None):
            elem = lxml.etree.SubElement(root, 'payer');
            elem.text = str(self.payer);
        if (self.subscriber != None):
            elem = lxml.etree.SubElement(root, 'subscriber');
            elem.text = str(self.subscriber);
        
        if (declaration):    
            return lxml.etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True); 
        else:
            return lxml.etree.tostring(root); 
        
    def tojson(self):   
        
        root = {}
        
        if (self.id != None):
            root['id'] = self.id;
        if (self.title != None):
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
    
class ServiceOperation:
    
    def __init__(self, customer, payer, subscriber, service, status, params):
        
        self.customer = customer;
        self.payer = payer;
        self.subscriber = subscriber;
        self.service = service;
        self.status = status;
        self.params = params;  
        
    def __str__(self):
        
        s = u'customer:{0}|payer:{1}|subscriber:{2}'.format(self.customer, self.payer, self.subscriber) + \
            u'|service:{0}|status:{1}|params#'.format(self.service, self.status);
        
        if (len(self.params) > 0):
            
            for key, value in self.params.items():
                s += '{0}:{1}#'.format(key, value);
                
        return s; 
    
    def toxml(self, declaration=False):
        
        root = lxml.etree.Element('operation');
        
        if (self.customer != None):
            elem = lxml.etree.SubElement(root, 'customer');
            elem.text = str(self.customer);
        if (self.payer != None):
            elem = lxml.etree.SubElement(root, 'payer');
            elem.text = str(self.payer);
        if (self.subscriber != None):
            elem = lxml.etree.SubElement(root, 'subscriber');
            elem.text = str(self.subscriber);
        if (self.service != None):
            elem = lxml.etree.SubElement(root, 'service');
            elem.text = str(self.service);
        if (self.status != None):
            elem = lxml.etree.SubElement(root, 'status');
            elem.text = self.status;  
             
        elParams = lxml.etree.SubElement(root, 'params');
            
        for key, value in self.params.items():
            elParam = lxml.etree.SubElement(elParams, 'entry');
            elem = lxml.etree.SubElement(elParam, 'key');
            elem.text = str(key);    
            elem = lxml.etree.SubElement(elParam, 'value');
            elem.text = str(value);  
            
        if (declaration):
            return lxml.etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True);    
        else:
            return lxml.etree.tostring(root);
        
    def tojson(self):
        
        root = {}
        
        if (self.customer != None):
            root['customer'] = self.customer;
        if (self.payer != None):
            root['payer'] = self.payer;
        if (self.subscriber != None):
            root['subscriber'] = self.subscriber;
        if (self.service != None):
            root['service'] = self.service;
        if (self.status != None):
            root['status'] = self.status;  
                
        elParams = [];             
        for key, value in self.params.items():  
            param = {}; 
            param['key'] = key;
            param['value'] = value;
            elParams.append(param);           
  
        root['params'] = {'entry' : elParams}; 
        
        return jsonlib2.write(root);                                          