# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.extensions.testenv.application.soap_handler
   :platform: Unix
   :synopsis: Handles SOAP operations
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.core.masterhead import MasterHead
import hydratk.extensions.testenv.interfaces.db_int as db_int 
import web
import lxml.etree as e
import lxml.objectify

class SoapHandler():

    _mh = None
    nsmap = None
    ns0 = None
    ns1 = None
    
    def __init__(self):
        
        self._mh = MasterHead.get_head()
        self.nsmap = {'soapenv': 'http://www.w3.org/2003/05/soap-envelope/',
                      'ns0': 'http://hydratk.org/'}
        self.ns0 = '{%s}' % self.nsmap['soapenv']
        self.ns1 = '{%s}' % self.nsmap['ns0']        

    def _get_db(self):    
    
        db = db_int.DB_INT()
        db.connect()
        return db
    
    def fault(self, message):
        
        root = e.Element(self.ns0+'Envelope', nsmap=self.nsmap)
        
        e.SubElement(root, self.ns0+'Header')
        body = e.SubElement(root, self.ns0+'Body')
        fault = e.SubElement(body, self.ns0+'Fault')
        e.SubElement(fault, self.ns1+'message').text = str(message)
        
        return e.tostring(root, pretty_print=True) 
    
    def response(self, method, content):        
        
        root = e.Element(self.ns0+'Envelope', nsmap=self.nsmap)
        
        e.SubElement(root, self.ns0+'Header')
        body = e.SubElement(root, self.ns0+'Body')
        response = e.SubElement(body, self.ns1+method+'_response')
        response.append(content)
        
        return e.tostring(root, pretty_print=True)         
    
    def dispatcher(self, headers, data):
        
        try:
            
            action = headers['HTTP_SOAPACTION'] if headers.has_key('HTTP_SOAPACTION') else None
            doc = lxml.objectify.fromstring(data)
            el_action = self.ns1+action
            
            if (action == None):
                return self.fault('Missing SOAPAction')
            elif (action == 'read_customer'):
                return self.read_customer(doc.Body[el_action])
            elif (action == 'create_customer'):
                return self.create_customer(doc.Body[el_action])
            elif (action == 'change_customer'):
                return self.change_customer(doc.Body[el_action])                        
            elif (action == 'read_payer'):
                return self.read_payer(doc.Body[el_action])
            elif (action == 'create_payer'):
                return self.create_payer(doc.Body[el_action])
            elif (action == 'change_payer'):
                return self.change_payer(doc.Body[el_action]) 
            elif (action == 'read_subscriber'):
                return self.read_subscriber(doc.Body[el_action])
            elif (action == 'create_subscriber'):
                return self.create_subscriber(doc.Body[el_action])
            elif (action == 'change_subscriber'):
                return self.change_subscriber(doc.Body[el_action]) 
            elif (action == 'read_contact'):
                return self.read_contact(doc.Body[el_action])
            elif (action == 'create_contact'):
                return self.create_contact(doc.Body[el_action])
            elif (action == 'change_contact'):
                return self.change_contact(doc.Body[el_action])
            elif (action == 'assign_contact_role'):
                return self.assign_contact_role(doc.Body[el_action]) 
            elif (action == 'revoke_contact_role'):
                return self.revoke_contact_role(doc.Body[el_action])             
            elif (action == 'read_address'):
                return self.read_address(doc.Body[el_action])
            elif (action == 'create_address'):
                return self.create_address(doc.Body[el_action])
            elif (action == 'change_address'):
                return self.change_address(doc.Body[el_action]) 
            elif (action == 'assign_address_role'):
                return self.assign_address_role(doc.Body[el_action]) 
            elif (action == 'revoke_address_role'):
                return self.revoke_address_role(doc.Body[el_action])             
            elif (action == 'read_services'):
                return self.read_services(doc.Body[el_action])
            elif (action == 'create_service'):
                return self.create_service(doc.Body[el_action])
            elif (action == 'change_service'):
                return self.change_service(doc.Body[el_action])                                                                    
            else:
                return self.fault('Invalid SOAPAction {0}'.format(action))
            
        except e.XMLSyntaxError, ex:
            self._mh.dmsg('htk_on_extension_error', 'XML error: {0}'.format(ex), self._mh.fromhere())
            return self.fault('Invalid XML - ' + ex)
        
    def read_customer(self, doc):
        """Method handles read_customer request         
           
        Args:
           id - int 
             
        Returns:
           read_customer_response with crm_entities.Customer in XML
           SOAP fault when customer not found            
                
        """ 
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'read_customer', e.tostring(doc)), 
                      self._mh.fromhere())                  

        id = doc.find('id').text if doc.find('id') else None
        
        db = self._get_db()            
        customer = db.read_customer(id)
        db.disconnect()
        
        if (customer != None):
            return self.response('read_customer', customer.toxml())
        else:
            return self.fault('Customer {0} not found'.format(id))  
        
    def create_customer(self, doc):
        """Method handles create_customer request         
           
        Args:
           customer - crm_entities.Customer in XML
           <create_customer>
             <name>Charlie Bowman</name>
             <status>active</status>
             <segment>2</segment>
             <birth_no>700101/0001</birth_no>
             <reg_no>123456</reg_no>
             <tax_no>CZ123456</tax_no>
           </create_customer>   
             
        Returns:
           create_customer_response with id of created customer
           SOAP fault when customer not created           
                
        """  
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'create_customer', e.tostring(doc)), 
                      self._mh.fromhere())                      
        
        name = doc.find('name').text if doc.find('name') else None
        status = doc.find('status').text if doc.find('status') else None
        segment = doc.find('segment').text if doc.find('segment') else None
        birth_no = doc.find('birth_no').text if doc.find('birth_no') else None
        reg_no = doc.find('reg_no').text if doc.find('reg_no') else None
        tax_no = doc.find('tax_no').text if doc.find('tax_no') else None  
        
        db = self._get_db()
        id = db.create_customer(name, segment, status, birth_no, reg_no, tax_no)
        db.disconnect()
        
        if (id != None):
            elem = e.Element('id')
            elem.text = str(id)
            return self.response('create_customer', elem)
        else:
            return self.fault('Customer not created')     
        
    def change_customer(self, doc):
        """Method handles change_customer request         
           
        Args:
           customer - crm_entities.Customer in XML
             
        Returns:
           change_customer_response with result true when customer changed
           SOAP fault when customer not changed           
                
        """     
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'change_customer', e.tostring(doc)), 
                      self._mh.fromhere())              
        
        id = doc.find('id').text if doc.find('id') else None
        name = doc.find('name').text if doc.find('name') else None
        status = doc.find('status').text if doc.find('status') else None
        segment = doc.find('segment').text if doc.find('segment') else None
        birth_no = doc.find('birth_no').text if doc.find('birth_no') else None
        reg_no = doc.find('reg_no').text if doc.find('reg_no') else None
        tax_no = doc.find('tax_no').text if doc.find('tax_no') else None  
        
        db = self._get_db()
        res = db.change_customer(id, name, status, segment, birth_no, reg_no, tax_no)
        db.disconnect()
        
        if (res):
            elem = e.Element('result')
            elem.text = 'true'
            return self.response('change_customer', elem)
        else:
            return self.fault('Customer not changed')                   
        
    def read_payer(self, doc):
        """Method handles read_payer request         
           
        Args:
           id - int 
             
        Returns:
           read_payer_response with crm_entities.Payer in XML
           SOAP fault when payer not found            
                
        """       
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'read_payer', e.tostring(doc)), 
                      self._mh.fromhere())               

        id = doc.find('id').text if doc.find('id') else None
        
        db = self._get_db()            
        payer = db.read_payer(id)
        db.disconnect()
        
        if (payer != None):
            return self.response('read_payer', payer.toxml())
        else:
            return self.fault('Payer {0} not found'.format(id))  
        
    def create_payer(self, doc):
        """Method handles create_payer request         
           
        Args:
           payer - crm_entities.Payer in XML
           <create_payer>
             <name>Charlie Bowman</name>
             <status>active</status>
             <billcycle>1</billcycle>
             <bank_account>12345/0100</bank_account>
             <customer>1</customer>
           </create_payer>   
             
        Returns:
           create_payer_response with id of created payer
           SOAP fault when payer not created           
                
        """    
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'create_payer', e.tostring(doc)), 
                      self._mh.fromhere())                    
        
        name = doc.find('name').text if doc.find('name') else None
        status = doc.find('status').text if doc.find('status') else None
        billcycle = doc.find('billcycle').text if doc.find('billcycle') else None
        bank_account = doc.find('bank_account').text if doc.find('bank_account') else None
        customer = doc.find('customer').text if doc.find('customer') else None
        
        db = self._get_db()
        id = db.create_payer(name, billcycle, customer, status, bank_account)
        db.disconnect()
        
        if (id != None):
            elem = e.Element('id')
            elem.text = str(id)
            return self.response('create_payer', elem)
        else:
            return self.fault('Payer not created')     
        
    def change_payer(self, doc):
        """Method handles change_payer request         
           
        Args:
           payer - crm_entities.Payer in XML
             
        Returns:
           change_payer_response with result true when payer changed
           SOAP fault when payer not changed           
                
        """ 
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'change_payer', e.tostring(doc)), 
                      self._mh.fromhere())                  
        
        id = doc.find('id').text if doc.find('id') else None
        name = doc.find('name').text if doc.find('name') else None
        status = doc.find('status').text if doc.find('status') else None
        billcycle = doc.find('billcycle').text if doc.find('billcycle') else None
        bank_account = doc.find('bank_account').text if doc.find('bank_account') else None
        customer = doc.find('customer').text if doc.find('customer') else None
        
        db = self._get_db()
        res = db.change_payer(id, name, status, billcycle, bank_account, customer)
        db.disconnect()
        
        if (res):
            elem = e.Element('result')
            elem.text = 'true'
            return self.response('change_payer', elem)
        else:
            return self.fault('Payer not changed')        
        
    def read_subscriber(self, doc):
        """Method handles read_csubscriber request         
           
        Args:
           id - int 
             
        Returns:
           read_subscriber_response with crm_entities.Subscriber in XML
           SOAP fault when subscriber not found            
                
        """           
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'read_subscriber', e.tostring(doc)), 
                      self._mh.fromhere())           

        id = doc.find('id').text if doc.find('id') else None
        
        db = self._get_db()            
        subscriber = db.read_subscriber(id)
        db.disconnect()
        
        if (subscriber != None):
            return self.response('read_subscriber', subscriber.toxml())
        else:
            return self.fault('Subscriber {0} not found'.format(id))  
        
    def create_subscriber(self, doc):
        """Method handles create_subscriber request         
           
        Args:
           subscriber - crm_entities.Subscriber in XML
           <create_subscriber>
             <name>Charlie Bowman</name>
             <msisdn>12345</msisdn>
             <status>active</status>
             <market>1</market>
             <tariff>433</tariff>
             <customer>1</customer>
             <payer>1</payer>
           </create_subscriber>   
             
        Returns:
           create_subscriber_response with id of created subscriber
           SOAP fault when subscriber not created           
                
        """             
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'create_subscriber', e.tostring(doc)), 
                      self._mh.fromhere())           
        
        name = doc.find('name').text if doc.find('name') else None
        msisdn = doc.find('msisdn').text if doc.find('msisdn') else None
        status = doc.find('status').text if doc.find('status') else None
        market = doc.find('market').text if doc.find('market') else None
        tariff = doc.find('tariff').text if doc.find('tariff') else None
        customer = doc.find('customer').text if doc.find('customer') else None
        payer = doc.find('payer').text if doc.find('payer') else None  
        
        db = self._get_db()
        id = db.create_subscriber(name, msisdn, market, tariff, customer, payer, status)
        db.disconnect()
        
        if (id != None):
            elem = e.Element('id')
            elem.text = str(id)
            return self.response('create_subscriber', elem)
        else:
            return self.fault('Subscriber not created')     
        
    def change_subscriber(self, doc):
        """Method handles change_subscriber request         
           
        Args:
           subscriber - crm_entities.Subscriber in XML
             
        Returns:
           change_subscriber_response with result true when subscriber changed
           SOAP fault when subscriber not changed           
                
        """     
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'change_subscriber', e.tostring(doc)), 
                      self._mh.fromhere())              
        
        id = doc.find('id').text if doc.find('id') else None
        name = doc.find('name').text if doc.find('name') else None
        msisdn = doc.find('msisdn').text if doc.find('msisdn') else None
        status = doc.find('status').text if doc.find('status') else None
        market = doc.find('market').text if doc.find('market') else None
        tariff = doc.find('tariff').text if doc.find('tariff') else None
        customer = doc.find('customer').text if doc.find('customer') else None
        payer = doc.find('payer').text if doc.find('payer') else None  
        
        db = self._get_db()
        res = db.change_subscriber(id, name, msisdn, status, market, tariff, customer, payer)
        db.disconnect()
        
        if (res):
            elem = e.Element('result')
            elem.text = 'true'
            return self.response('change_subscriber', elem)
        else:
            return self.fault('Subscriber not changed')            
        
    def read_contact(self, doc):
        """Method handles read_contact request         
           
        Args:
           id - int 
             
        Returns:
           read_contact_response with crm_entities.Contact in XML
           SOAP fault when contact not found            
                
        """           
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'read_contact', e.tostring(doc)), 
                      self._mh.fromhere())           

        id = doc.find('id').text if doc.find('id') else None
        
        db = self._get_db()            
        contact = db.read_contact(id)
        db.disconnect()
        
        if (contact != None):
            return self.response('read_contact', contact.toxml())
        else:
            return self.fault('Contact {0} not found'.format(id))  
        
    def create_contact(self, doc):
        """Method handles create_contact request         
           
        Args:
           contact - crm_entities.Contact in XML
           <create_contact>
             <name>Charlie Bowman</name>
             <phone>12345</phone>
             <email>xxx@xxx.com</email>
           </create_contact>   
             
        Returns:
           create_contact_response with id of created contact
           SOAP fault when contact not created           
                
        """  
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'create_contact', e.tostring(doc)), 
                      self._mh.fromhere())                      
        
        name = doc.find('name').text if doc.find('name') else None
        phone = doc.find('phone').text if doc.find('phone') else None
        email = doc.find('email').text if doc.find('email') else None
        
        db = self._get_db()
        id = db.create_contact(name, phone, email)
        db.disconnect()
        
        if (id != None):
            elem = e.Element('id')
            elem.text = str(id)
            return self.response('create_contact', elem)
        else:
            return self.fault('Contact not created')     
        
    def change_contact(self, doc):
        """Method handles change_contact request         
           
        Args:
           contact - crm_entities.Contact in XML
             
        Returns:
           change_contact_response with result true when contact changed
           SOAP fault when contact not changed           
                
        """    
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'change_contact', e.tostring(doc)), 
                      self._mh.fromhere())               
        
        id = doc.find('id').text if doc.find('id') else None
        name = doc.find('name').text if doc.find('name') else None
        phone = doc.find('phone').text if doc.find('phone') else None
        email = doc.find('email').text if doc.find('email') else None
        
        db = self._get_db()
        res = db.change_contact(id, name, phone, email)
        db.disconnect()
        
        if (res):
            elem = e.Element('result')
            elem.text = 'true'
            return self.response('change_contact', elem)
        else:
            return self.fault('Contact not changed')  
        
    def assign_contact_role(self, doc):
        """Method handles assign_contact_role request         
           
        Args:
           contact_role - crm_entities.ContactRole in XML
           <create_contact_role>
             <id>1</id>
             <title>contract</title>
             <customer>1</customer>
             <payer>1</payer>
             <subscriber>1</subscriber>
           </create_contact_role>   
             
        Returns:
           assign_contact_role_response with result true when contact role assigned
           SOAP fault when contact role not assigned          
                
        """   
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'assign_contact_role', e.tostring(doc)), 
                      self._mh.fromhere())                     
        
        id = doc.find('id').text if doc.find('id') else None
        title = doc.find('title').text if doc.find('title') else None
        customer = doc.find('customer').text if doc.find('customer') else None
        payer = doc.find('payer').text if doc.find('payer') else None
        subscriber = doc.find('subscriber').text if doc.find('subscriber') else None        
        
        db = self._get_db()
        res = db.assign_contact_role(id, title, customer, payer, subscriber)
        db.disconnect()
        
        if (res):
            elem = e.Element('result')
            elem.text = 'true'
            return self.response('assign_contact_role', elem)
        else:
            return self.fault('Contact role not assigned')   
        
    def revoke_contact_role(self, doc):
        """Method handles revoke_contact_role request         
           
        Args:
           contact_role - crm_entities.ContactRole in XML 
             
        Returns:
           revoke_contact_role_response with result true when contact role revoked
           SOAP fault when contact role not revoked          
                
        """   
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'revoke_contact_role', e.tostring(doc)), 
                      self._mh.fromhere())                     
        
        id = doc.find('id').text if doc.find('id') else None
        title = doc.find('title').text if doc.find('title') else None
        customer = doc.find('customer').text if doc.find('customer') else None
        payer = doc.find('payer').text if doc.find('payer') else None
        subscriber = doc.find('subscriber').text if doc.find('subscriber') else None        
        
        db = self._get_db()
        res = db.revoke_contact_role(id, title, customer, payer, subscriber)
        db.disconnect()
        
        if (res):
            elem = e.Element('result')
            elem.text = 'true'
            return self.response('revoke_contact_role', elem)
        else:
            return self.fault('Contact role not revoked')                     
        
    def read_address(self, doc):
        """Method handles read_address request         
           
        Args:
           id - int 
             
        Returns:
           read_address_response with crm_entities.Address in XML
           SOAP fault when address not found            
                
        """           
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'read_address', e.tostring(doc)), 
                      self._mh.fromhere())           

        id = doc.find('id').text if doc.find('id') else None
        
        db = self._get_db()            
        address = db.read_address(id)
        db.disconnect()
        
        if (address != None):
            return self.response('read_address', address.toxml())
        else:
            return self.fault('Address {0} not found'.format(id))  
        
    def create_address(self, doc):
        """Method handles create_address request         
           
        Args:
           address - crm_entities.Address in XML
           <create_adddress>
             <street>Tomickova</street>
             <street_no>2144/1</street_no>
             <city>Praha</city>
             <zip>14800</zip>
           </create_address>   
             
        Returns:
           create_address_response with id of created address
           SOAP fault when address not created           
                
        """    
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'create_address', e.tostring(doc)), 
                      self._mh.fromhere())                    
        
        street = doc.find('street').text if doc.find('street') else None
        street_no = doc.find('street_no').text if doc.find('street_no') else None
        city = doc.find('city').text if doc.find('city') else None
        zip = doc.find('zip').text if doc.find('zip') else None
        
        db = self._get_db()
        id = db.create_address(street, street_no, city, zip)
        db.disconnect()
        
        if (id != None):
            elem = e.Element('id')
            elem.text = str(id)
            return self.response('create_address', elem)
        else:
            return self.fault('Address not created')     
        
    def change_address(self, doc):
        """Method handles change_address request         
           
        Args:
           address - crm_entities.Address in XML
             
        Returns:
           change_address_response with result true when address changed
           SOAP fault when address not changed           
                
        """        
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'change_address', e.tostring(doc)), 
                      self._mh.fromhere())           
        
        id = doc.find('id').text if doc.find('id') else None
        street = doc.find('street').text if doc.find('street') else None
        street_no = doc.find('street_no').text if doc.find('street_no') else None
        city = doc.find('city').text if doc.find('city') else None
        zip = doc.find('zip').text if doc.find('zip') else None
        
        db = self._get_db()
        res = db.change_address(id, street, street_no, city, zip)
        db.disconnect()
        
        if (res):
            elem = e.Element('result')
            elem.text = 'true'
            return self.response('change_address', elem)
        else:
            return self.fault('Address not changed')    
        
    def assign_address_role(self, doc):
        """Method handles assign_address_role request         
           
        Args:
           address_role - crm_entities.AddressRole in XML
           <create_address_role>
             <id>1</id>
             <title>contract</title>
             <contact>1</contact>
             <customer>1</customer>
             <payer>1</payer>
             <subscriber>1</subscriber>
           </create_address_role>   
             
        Returns:
           assign_address_role_response with result true when address role assigned
           SOAP fault when address role not assigned          
                
        """  
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'assign_address_role', e.tostring(doc)), 
                      self._mh.fromhere())                      
        
        id = doc.find('id').text if doc.find('id') else None
        title = doc.find('title').text if doc.find('title') else None
        contact = doc.find('contact').text if doc.find('contact') else None
        customer = doc.find('customer').text if doc.find('customer') else None
        payer = doc.find('payer').text if doc.find('payer') else None
        subscriber = doc.find('subscriber').text if doc.find('subscriber') else None        
        
        db = self._get_db()
        res = db.assign_address_role(id, title, contact, customer, payer, subscriber)
        db.disconnect()
        
        if (res):
            elem = e.Element('result')
            elem.text = 'true'
            return self.response('assign_address_role', elem)
        else:
            return self.fault('Address role not assigned')   
        
    def revoke_address_role(self, doc):
        """Method handles revoke_address_role request         
           
        Args:
           address_role - crm_entities.AddressRole in XML 
             
        Returns:
           revoke_address_role_response with result true when address role revoked
           SOAP fault when address role not revoked          
                
        """ 
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'revoke_address_role', e.tostring(doc)), 
                      self._mh.fromhere())                       
        
        id = doc.find('id').text if doc.find('id') else None
        title = doc.find('title').text if doc.find('title') else None
        contact = doc.find('contact').text if doc.find('contact') else None
        customer = doc.find('customer').text if doc.find('customer') else None
        payer = doc.find('payer').text if doc.find('payer') else None
        subscriber = doc.find('subscriber').text if doc.find('subscriber') else None        
        
        db = self._get_db()
        res = db.revoke_address_role(id, title, contact, customer, payer, subscriber)
        db.disconnect()
        
        if (res):
            elem = e.Element('id')
            elem.text = 'true'
            return self.response('revoke_address_role', elem)
        else:
            return self.fault('Address role not revoked') 
        
    def read_services(self, doc):
        """Method handles read_services request         
           
        Args:
           customer - int, optional
           payer - int, optional
           subscriber - int, optional
           service - int, optional, default all services 
             
        Returns:
           read_services_response with list of crm_entities.Service in XML
           SOAP fault when address not found            
                
        """
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'read_services', e.tostring(doc)), 
                      self._mh.fromhere())                      

        customer = doc.find('customer').text if doc.find('customer') else None
        payer = doc.find('payer').text if doc.find('payer') else None
        subscriber = doc.find('subscriber').text if doc.find('subscriber') else None
        service = doc.find('service').text if doc.find('service') else None
        
        db = self._get_db()            
        services = db.read_services(customer, payer, subscriber, service)
        db.disconnect()
        
        if (len(services) > 0):
            
            elem = e.Element('services')
            for service in services:
                elem.append(service.toxml())
            
            return self.response('read_services', elem)
        else:
            return self.fault('Service not found'.format(id))          
        
    def create_service(self, doc):
        """Method handles create_service request         
           
        Args:
           service_operation - crm_entities.ServiceOperation in XML
           <create_service>
             <service>615</service>
             <customer>1</customer>
             <payer>1</payer>
             <subscriber>1</subscriber>
             <status>active</active>
             <params>
               <entry>
                 <key>121</key>
                 <value>12345</value>
             </params>
           </create_service>   
             
        Returns:
           create_service_response with result true
           SOAP fault when service not created           
                
        """  
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'create_service', e.tostring(doc)), 
                      self._mh.fromhere())                      
        
        service = doc.find('service').text if doc.find('service') else None
        customer = doc.find('customer').text if doc.find('customer') else None
        payer = doc.find('payer').text if doc.find('payer') else None
        subscriber = doc.find('subscriber').text if doc.find('subscriber') else None
        status = doc.find('status').text if doc.find('status') else None
        
        params = {}
        if (doc.find('params') != None):
            for param in doc.findall('params/entry'):
                params[param.find('key').text] = param.find('value').text
        
        db = self._get_db()
        res = db.create_service(service, customer, payer, subscriber, status, params)
        db.disconnect()
        
        if (id != None):
            elem = e.Element('result')
            elem.text = 'true'
            return self.response('create_service', elem)
        else:
            return self.fault('Service not created')     
        
    def change_service(self, doc):
        """Method handles change_service request         
           
        Args:
           service_operation - crm_entities.ServiceOperation in XML 
             
        Returns:
           change_service_response with result true
           SOAP fault when service not changed           
                
        """     
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'change_service', e.tostring(doc)), 
                      self._mh.fromhere())                   
        
        service = doc.find('service').text if doc.find('service') else None
        customer = doc.find('customer').text if doc.find('customer') else None
        payer = doc.find('payer').text if doc.find('payer') else None
        subscriber = doc.find('subscriber').text if doc.find('subscriber') else None
        status = doc.find('status').text if doc.find('status') else None
        
        params = {}
        if (doc.find('params') != None):
            for param in doc.findall('params/entry'):
                params[param.find('key').text] = param.find('value').text
        
        db = self._get_db()
        res = db.change_service(service, customer, payer, subscriber, status, params)
        db.disconnect()
        
        if (id != None):
            elem = e.Element('result')
            elem.text = 'true'
            return self.response('change_service', elem)
        else:
            return self.fault('Service not changed')                                                      