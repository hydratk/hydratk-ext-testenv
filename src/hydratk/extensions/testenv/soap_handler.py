# -*- coding: utf-8 -*-
"""Handles SOAP operations

.. module:: testenv.soap_handler
   :platform: Unix
   :synopsis: Handles SOAP operations
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.core.masterhead import MasterHead
from hydratk.extensions.testenv.db_handler import DbHandler
from lxml.etree import Element, SubElement, tostring, XMLSyntaxError
from lxml import objectify

class SoapHandler(object):
    """Class SoapHandler
    """

    _mh = None
    _nsmap = None
    _ns0 = None
    _ns1 = None
    
    def __init__(self):
        """Class constructor
           
        Called when the object is initialized   
        
        Args: 
           none
           
        """         
        
        self._mh = MasterHead.get_head()
        self._nsmap = {'soapenv': 'http://www.w3.org/2003/05/soap-envelope/',
                      'ns0': 'http://hydratk.org/'}
        self._ns0 = '{%s}' % self._nsmap['soapenv']
        self._ns1 = '{%s}' % self._nsmap['ns0']        

    def _get_db(self):
        """Method connect to database     
           
        Args:
           none

        Returns:
           DB_INT: DB client                 
                
        """              
    
        db = DbHandler()
        db.connect()
        return db
    
    def _fault(self, message):
        """Method creates SOAP fault     
           
        Args:
           message (str): error message 
           
        Returns:
           str: SOAP fault               
                
        """          
        
        root = Element(self._ns0+'Envelope', nsmap=self._nsmap)
        
        SubElement(root, self._ns0+'Header')
        body = SubElement(root, self._ns0+'Body')
        fault = SubElement(body, self._ns0+'Fault')
        SubElement(fault, self._ns1+'message').text = str(message)
        
        return tostring(root, pretty_print=True) 
    
    def _response(self, method, content):        
        """Method creates SOAP response     
           
        Args:
           method (str): method name
           content (xml): response body
           
        Returns:
           str: SOAP response                  
                
        """                   
        
        root = Element(self._ns0+'Envelope', nsmap=self._nsmap)
        
        SubElement(root, self._ns0+'Header')
        body = SubElement(root, self._ns0+'Body')
        response = SubElement(body, self._ns1+method+'_response')
        response.append(content)
        
        return tostring(root, pretty_print=True)         
    
    def dispatcher(self, headers, data):
        """Method dispatches request according to SOAPAction        
           
        Args:
           headers (dict): HTTP headers
           data (str): SOAP request   
           
        Returns:
           str: SOAP response or fault               
                
        """         
        
        try:
            
            action = headers['HTTP_SOAPACTION'] if 'HTTP_SOAPACTION' in headers else None
            doc = objectify.fromstring(data)
            el_action = self._ns1+action
            
            if (action == None):
                return self._fault('Missing SOAPAction')
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
                return self._fault('Invalid SOAPAction {0}'.format(action))
            
        except XMLSyntaxError as ex:
            self._mh.dmsg('htk_on_extension_error', 'XML error: {0}'.format(ex), self._mh.fromhere())
            return self._fault('Invalid XML - ' + ex)
        
    def read_customer(self, doc):
        """Method handles read_customer request         
           
        Args:
           doc (xml): read_customer request with customer id 
             
        Returns:
           xml: read_customer_response with customer detail,
                SOAP fault when customer not found   
           
        Example:
        
        .. code-block:: xml
        
           <read_customer>
             <id>1</id>
           </read_customer>         
        
           <read_customer_response>
             <customer>
               <id>1</id>
               <name>Charlie Bowman</name>
               <status>active</status>
               <segment>2</segment>
               <birth_no>700101/0001</birth_no>
               <reg_no>123456</reg_no>
               <tax_no>CZ123456</tax_no>
             </customer>
           </read_customer_response>                       
                
        """ 
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'read_customer', tostring(doc)), 
                      self._mh.fromhere())                  

        id = doc.find('id').text if doc.find('id') else None
        
        db = self._get_db()            
        customer = db.read_customer(id)
        db.disconnect()
        
        if (customer != None):
            return self._response('read_customer', customer.toxml())
        else:
            return self._fault('Customer {0} not found'.format(id))  
        
    def create_customer(self, doc):
        """Method handles create_customer request         
           
        Args:
           doc (xml): create_customer request
             
        Returns:
           xml: create_customer_response with id of created customer,
                SOAP fault when customer not created 
           
        Example:
        
        .. code-block:: xml
        
           <create_customer>
             <name>Charlie Bowman</name>
             <status>active</status>
             <segment>2</segment>
             <birth_no>700101/0001</birth_no>
             <reg_no>123456</reg_no>
             <tax_no>CZ123456</tax_no>
           </create_customer>  
           
           <create_customer_response>
             <id>1</id>
           <create_customer_response>                  
                
        """  
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'create_customer', tostring(doc)), 
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
            elem = Element('id')
            elem.text = str(id)
            return self._response('create_customer', elem)
        else:
            return self._fault('Customer not created')     
        
    def change_customer(self, doc):
        """Method handles change_customer request         
           
        Args:
           doc (xml): change_customer request
             
        Returns:
           xml: change_customer_response with result true when customer changed,
                SOAP fault when customer not changed
           
        Example:
        
        .. code-block:: xml
        
           <change_customer>
             <id>1</id>
             <name>Charlie Bowman</name>
             <status>active</status>
             <segment>2</segment>
             <birth_no>700101/0001</birth_no>
             <reg_no>123456</reg_no>
             <tax_no>CZ123456</tax_no>
           </create_customer>  
           
           <change_customer_response>
             <result>true</true>
           </change_customer_response>                      
                
        """     
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'change_customer', tostring(doc)), 
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
            elem = Element('result')
            elem.text = 'true'
            return self._response('change_customer', elem)
        else:
            return self._fault('Customer not changed')                   
        
    def read_payer(self, doc):
        """Method handles read_payer request         
           
        Args:
           doc (xml): read_payer request with payer id
             
        Returns:
           xml: read_payer_response with payer detail,
                SOAP fault when payer not found 
           
        Example:
        
        .. code-block:: xml        
           
           <read_payer>
             <id>1</id>
           </read_payer>
           
           <read_payer_response>
             <payer>
               <id>1</id>
               <name>Charlie Bowman</name>
               <status>active</status>
               <billcycle>1</billcycle>
               <bank_account>12345/0100</bank_account>
               <customer>1</customer>
             </payer>
           </read_payer_response>                                    
                
        """       
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'read_payer', tostring(doc)), 
                      self._mh.fromhere())               

        id = doc.find('id').text if doc.find('id') else None
        
        db = self._get_db()            
        payer = db.read_payer(id)
        db.disconnect()
        
        if (payer != None):
            return self._response('read_payer', payer.toxml())
        else:
            return self._fault('Payer {0} not found'.format(id))  
        
    def create_payer(self, doc):
        """Method handles create_payer request         
           
        Args:
           doc (xml): create_payer request 
             
        Returns:
           xml: create_payer_response with id of created payer,
                SOAP fault when payer not created
           
        Example:
        
        .. code-block:: xml
        
           <create_payer>
             <name>Charlie Bowman</name>
             <status>active</status>
             <billcycle>1</billcycle>
             <bank_account>12345/0100</bank_account>
             <customer>1</customer>
           </create_payer>
           
           <create_payer_response>
             <id>1</id>
           </create_payer_response>                    
                
        """    
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'create_payer', tostring(doc)), 
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
            elem = Element('id')
            elem.text = str(id)
            return self._response('create_payer', elem)
        else:
            return self._fault('Payer not created')     
        
    def change_payer(self, doc):
        """Method handles change_payer request         
           
        Args:
           doc (xml): change_payer request
             
        Returns:
           xml: change_payer_response with result true when payer changed,
                SOAP fault when payer not changed 
           
        Example:
        
        .. code-block:: xml
        
           <change_payer>
             <id>1</id>
             <name>Charlie Bowman</name>
             <status>active</status>
             <billcycle>1</billcycle>
             <bank_account>12345/0100</bank_account>
             <customer>1</customer>
           </change_payer>
           
           <change_payer_response>
             <result>true</result>
           </change_payer_response>                                  
                
        """ 
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'change_payer', tostring(doc)), 
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
            elem = Element('result')
            elem.text = 'true'
            return self._response('change_payer', elem)
        else:
            return self._fault('Payer not changed')        
        
    def read_subscriber(self, doc):
        """Method handles read_csubscriber request         
           
        Args:
           doc (xml): read_subscriber request with subscriber id 
             
        Returns:
           xml: read_subscriber_response with subscriber detail,
                SOAP fault when subscriber not found  
           
        Example:
        
        .. code-block:: xml        
           
          <read_subscriber>
            <id>1</id>
          <read_subscriber> 
           
          <read_subscriber_response>
            <subscriber>
              <id>1</id>
              <name>Charlie Bowman</name>
              <msisdn>12345</msisdn>
              <status>active</status>
              <market>1</market>
              <tariff>433</tariff>
              <customer>1</customer>
              <payer>1</payer>
            </subscriber>
          </read_subscriber_response>                                
                
        """           
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'read_subscriber', tostring(doc)), 
                      self._mh.fromhere())           

        id = doc.find('id').text if doc.find('id') else None
        
        db = self._get_db()            
        subscriber = db.read_subscriber(id)
        db.disconnect()
        
        if (subscriber != None):
            return self._response('read_subscriber', subscriber.toxml())
        else:
            return self._fault('Subscriber {0} not found'.format(id))  
        
    def create_subscriber(self, doc):
        """Method handles create_subscriber request         
           
        Args:
           doc(xml): create_subscriber request 
             
        Returns:
           xml: create_subscriber_response with id of created subscriber,
                SOAP fault when subscriber not created   
           
        Example:
        
        .. code-block:: xml
        
          <create_subscriber>
            <name>Charlie Bowman</name>
            <msisdn>12345</msisdn>
            <status>active</status>
            <market>1</market>
            <tariff>433</tariff>
            <customer>1</customer>
            <payer>1</payer>
          </create_subscriber>
           
          <create_subscriber_response>
            <id>1</id>
          <create_subscriber_response>                
                
        """             
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'create_subscriber', tostring(doc)), 
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
            elem = Element('id')
            elem.text = str(id)
            return self._response('create_subscriber', elem)
        else:
            return self._fault('Subscriber not created')     
        
    def change_subscriber(self, doc):
        """Method handles change_subscriber request         
           
        Args:
           doc (xml): change_subscriber request
             
        Returns:
           xml: change_subscriber_response with result true when subscriber changed,
                SOAP fault when subscriber not changed  
           
        Example:
        
        .. code-block:: xml
        
          <change_subscriber>
            <id>1</id>
            <name>Charlie Bowman</name>
            <msisdn>12345</msisdn>
            <status>active</status>
            <market>1</market>
            <tariff>433</tariff>
            <customer>1</customer>
            <payer>1</payer>
          </change_subscriber>
           
          <change_subscriber_response>
            <result>true</result>
          <change_subscriber_response>                                
                
        """     
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'change_subscriber', tostring(doc)), 
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
            elem = Element('result')
            elem.text = 'true'
            return self._response('change_subscriber', elem)
        else:
            return self._fault('Subscriber not changed')            
        
    def read_contact(self, doc):
        """Method handles read_contact request         
           
        Args:
           doc (int): read_contact request with contact id
             
        Returns:
           xml: read_contact_response with contact detail, choice customer|payer|subscriber,
                SOAP fault when contact not found  
           
        Example:
        
        .. code-block:: xml
           
           <read_contact>
             <id>1</id>
           </read_contact>
           
           <read_contact_response>   
             <contact> 
               <id>1</id>
               <name>Charlie Bowman</name>
               <phone>12345</phone>
               <email>xxx@xxx.com</email>
               <roles>
                 <role>
                   <id>1</id>
                   <title>contract</title>
                   <customer>1</customer>
                   <payer>1</payer>
                   <subscribe>1</subscriber>
                 </role>
               </roles>
             </contact>
           </read_contact_response>                                  
                
        """           
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'read_contact', tostring(doc)), 
                      self._mh.fromhere())           

        id = doc.find('id').text if doc.find('id') else None
        
        db = self._get_db()            
        contact = db.read_contact(id)
        db.disconnect()
        
        if (contact != None):
            return self._response('read_contact', contact.toxml())
        else:
            return self._fault('Contact {0} not found'.format(id))  
        
    def create_contact(self, doc):
        """Method handles create_contact request         
           
        Args:
           doc (xml): create_contact request
             
        Returns:
           xml: create_contact_response with id of created contact,
                SOAP fault when contact not created
           
        Example:
        
        .. code-block:: xml
        
           <create_contact>    
             <name>Charlie Bowman</name>
             <phone>12345</phone>
             <email>xxx@xxx.com</email>
           </create_contact> 
           
           <create_contact_response>
             <id>1</id>
           </create_contact_response>                                 
                
        """  
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'create_contact', tostring(doc)), 
                      self._mh.fromhere())                      
        
        name = doc.find('name').text if doc.find('name') else None
        phone = doc.find('phone').text if doc.find('phone') else None
        email = doc.find('email').text if doc.find('email') else None
        
        db = self._get_db()
        id = db.create_contact(name, phone, email)
        db.disconnect()
        
        if (id != None):
            elem = Element('id')
            elem.text = str(id)
            return self._response('create_contact', elem)
        else:
            return self._fault('Contact not created')     
        
    def change_contact(self, doc):
        """Method handles change_contact request         
           
        Args:
           doc (xml): change_contact request
             
        Returns:
           xml: change_contact_response with result true when contact changed,
                SOAP fault when contact not changed    
           
        Example:
        
        .. code-block:: xml
        
           <change_contact>    
             <id>1</id>
             <name>Charlie Bowman</name>
             <phone>12345</phone>
             <email>xxx@xxx.com</email>
           </change_contact> 
           
           <change_contact_response>
             <result>true</true>
           </change_contact_response>                     
                
        """    
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'change_contact', tostring(doc)), 
                      self._mh.fromhere())               
        
        id = doc.find('id').text if doc.find('id') else None
        name = doc.find('name').text if doc.find('name') else None
        phone = doc.find('phone').text if doc.find('phone') else None
        email = doc.find('email').text if doc.find('email') else None
        
        db = self._get_db()
        res = db.change_contact(id, name, phone, email)
        db.disconnect()
        
        if (res):
            elem = Element('result')
            elem.text = 'true'
            return self._response('change_contact', elem)
        else:
            return self._fault('Contact not changed')  
        
    def assign_contact_role(self, doc):
        """Method handles assign_contact_role request         
           
        Args:
           doc (xml): assign_contact_role request, choice customer|payer|subscriber
             
        Returns:
           xml: assign_contact_role_response with result true when contact role assigned,
                SOAP fault when contact role not assigned   
           
        Example:
        
        .. code-block:: xml
        
           <assign_contact_role>    
             <id>1</id>
             <title>contract</title>         
             <customer>1</customer>
             <payer>1</payer>
             <subscriber>1</subscriber>
           </assign_contact_role> 
           
           <assign_contact_role_response>
             <result>true</true>
           </assign_contact_role_response>                              
                
        """   
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'assign_contact_role', tostring(doc)), 
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
            elem = Element('result')
            elem.text = 'true'
            return self._response('assign_contact_role', elem)
        else:
            return self._fault('Contact role not assigned')   
        
    def revoke_contact_role(self, doc):
        """Method handles revoke_contact_role request         
           
        Args:
           doc (xml): revoke_contact_role request, choice customer|payer|subscriber 
             
        Returns:
           xml: revoke_contact_role_response with result true when contact role revoked,
                SOAP fault when contact role not revoked    
           
        Example:
        
        .. code-block:: xml
        
           <revoke_contact_role>    
             <id>1</id>
             <title>contract</title>         
             <customer>1</customer>
             <payer>1</payer>
             <subscriber>1</subscriber>
           </revoke_contact_role> 
           
           <revoke_contact_role_response>
             <result>true</true>
           </revoke_contact_role_response>                  
                
        """   
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'revoke_contact_role', tostring(doc)), 
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
            elem = Element('result')
            elem.text = 'true'
            return self._response('revoke_contact_role', elem)
        else:
            return self._fault('Contact role not revoked')                     
        
    def read_address(self, doc):
        """Method handles read_address request         
           
        Args:
           doc (xml) - read_address request with address id
             
        Returns:
           xml: read_address_response with address detail, choice contact|customer|payer|subscriber,
                SOAP fault when address not found  
           
        Example:
        
        .. code-block:: xml
        
           <read_address>
             <id>1</id>
           </read_address>           
        
           <read_address_response>
             <address>
               <id>1</id>
               <street>Tomickova</street>
               <street_no>2144/1</street_no>
               <city>Praha</city>
               <zip>14800</zip>
               <roles>
                 <role>
                   <id>1</id>
                   <title>contract</title>
                   <contact>1</contact>
                   <customer>1</customer>
                   <payer>1</payer>
                   <subscriber>1</subscriber>
                 </role>
               </roles>
             </address>
           </read_address_response>                                  
                
        """           
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'read_address', tostring(doc)), 
                      self._mh.fromhere())           

        id = doc.find('id').text if doc.find('id') else None
        
        db = self._get_db()            
        address = db.read_address(id)
        db.disconnect()
        
        if (address != None):
            return self._response('read_address', address.toxml())
        else:
            return self._fault('Address {0} not found'.format(id))  
        
    def create_address(self, doc):
        """Method handles create_address request         
           
        Args:
           doc (xml): create_address request
             
        Returns:
           xml: create_address_response with id of created address,
                SOAP fault when address not created
           
        Example:
        
        .. code-block:: xml
        
           <create_address>
             <street>Tomickova</street>
             <street_no>2144/1</street_no>
             <city>Praha</city>
             <zip>14800</zip>
           </create_address>  
           
           <create_address_response>
             <id>1</id>
           </create_address_response>         
                
        """    
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'create_address', tostring(doc)), 
                      self._mh.fromhere())                    
        
        street = doc.find('street').text if doc.find('street') else None
        street_no = doc.find('street_no').text if doc.find('street_no') else None
        city = doc.find('city').text if doc.find('city') else None
        zip = doc.find('zip').text if doc.find('zip') else None
        
        db = self._get_db()
        id = db.create_address(street, street_no, city, zip)
        db.disconnect()
        
        if (id != None):
            elem = Element('id')
            elem.text = str(id)
            return self._response('create_address', elem)
        else:
            return self._fault('Address not created')     
        
    def change_address(self, doc):
        """Method handles change_address request         
           
        Args:
           doc(xml): change_address request
             
        Returns:
           xml: change_address_response with result true when address changed,
                SOAP fault when address not changed  
           
        Example:
        
        .. code-block:: xml
        
           <change_address>
             <id>1</id>
             <street>Tomickova</street>
             <street_no>2144/1</street_no>
             <city>Praha</city>
             <zip>14800</zip>
           </change_address> 
           
           <change_address_response>
             <result>true</true>
           </change_address_response>                          
                
        """        
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'change_address', tostring(doc)), 
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
            elem = Element('result')
            elem.text = 'true'
            return self._response('change_address', elem)
        else:
            return self._fault('Address not changed')    
        
    def assign_address_role(self, doc):
        """Method handles assign_address_role request         
           
        Args:
           doc (xml): assign_address_role request, choice contact|customer|payer|subscriber
             
        Returns:
           xml: assign_address_role_response with result true when address role assigned,
                SOAP fault when address role not assigned
           
        Example:
        
        .. code-block:: xml
        
           <assign_address_role>    
             <id>1</id>
             <title>contract</title> 
             <contact>1</contact>        
             <customer>1</customer>
             <payer>1</payer>
             <subscriber>1</subscriber>
           </revoke_address_role> 
           
           <assign_address_role_response>
             <result>true</true>
           </assign_address_role_response>                
                
        """  
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'assign_address_role', tostring(doc)), 
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
            elem = Element('result')
            elem.text = 'true'
            return self._response('assign_address_role', elem)
        else:
            return self._fault('Address role not assigned')   
        
    def revoke_address_role(self, doc):
        """Method handles revoke_address_role request         
           
        Args:
           doc (xml): revoke_address_role request, choice contact|customer|payer|subscriber
             
        Returns:
           xml: revoke_address_role_response with result true when address role revoked,
                SOAP fault when address role not revoked   
           
        Example:
        
        .. code-block:: xml
        
           <revoke_address_role>    
             <id>1</id>
             <title>contract</title>
             <contact>1</contact>         
             <customer>1</customer>
             <payer>1</payer>
             <subscriber>1</subscriber>
           </revoke_address_role> 
           
           <revoke_address_role_response>
             <result>true</true>
           </revoke_address_role_response>                      
                
        """ 
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'revoke_address_role', tostring(doc)), 
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
            elem = Element('id')
            elem.text = 'true'
            return self._response('revoke_address_role', elem)
        else:
            return self._fault('Address role not revoked') 
        
    def read_services(self, doc):
        """Method handles read_services request         
           
        Args:
           doc (xml): read_services request, choice customer|payer|subscriber, all services are read if service empty
             
        Returns:
           xml: read_services_response with list of services,
                SOAP fault when service not found            
           
        Example:
        
        .. code-block:: xml
        
           <read_services>             
             <customer>1</customer>
             <payer>1</payer>
             <subscriber>1</subscriber>
             <service>615</service>
           </read_services> 
           
           <read_services_response>
             <services>
               <service>
                 <id>id</id>
                 <name>Telefonni cislo</name>
                 <status>active</active>
                 <params>
                   <entry>
                     <key>121</key>
                     <value>12345</value>
                   </entry>
                  </params>                 
               </service>
             </services>
           </read_services_response>             
                
        """
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'read_services', tostring(doc)), 
                      self._mh.fromhere())                      

        customer = doc.find('customer').text if doc.find('customer') else None
        payer = doc.find('payer').text if doc.find('payer') else None
        subscriber = doc.find('subscriber').text if doc.find('subscriber') else None
        service = doc.find('service').text if doc.find('service') else None
        
        db = self._get_db()            
        services = db.read_services(customer, payer, subscriber, service)
        db.disconnect()
        
        if (len(services) > 0):
            
            elem = Element('services')
            for service in services:
                elem.append(service.toxml())
            
            return self._response('read_services', elem)
        else:
            return self._fault('Service not found'.format(id))          
        
    def create_service(self, doc):
        """Method handles create_service request         
           
        Args:
           doc (xml): create_service request, choice customer|payer|subscriber
           
        Returns:
           xml: create_service_response with result true,
                SOAP fault when service not created            
           
        Example:
        
        .. code-block:: xml
        
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
               </entry>
             </params>
           </create_service>   
           
           <create_service_response>
             <result>true</result>
           </create_service_response>                    
                
        """  
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'create_service', tostring(doc)), 
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
            elem = Element('result')
            elem.text = 'true'
            return self._response('create_service', elem)
        else:
            return self._fault('Service not created')     
        
    def change_service(self, doc):
        """Method handles change_service request         
           
        Args:
           doc (xml): change_service request, choice customer|payer|subscriber 
             
        Returns:
           xml: change_service_response with result true,
                SOAP fault when service not changed    
           
        Example:
        
        .. code-block:: xml
        
           <change_service>
             <service>615</service>
             <customer>1</customer>
             <payer>1</payer>
             <subscriber>1</subscriber>
             <status>active</active>
             <params>
               <entry>
                 <key>121</key>
                 <value>12345</value>
               </entry>
             </params>
           </change_service>  
           
           <change_service_response>
             <result>true</result>
           </change_service_response>                                     
                
        """     
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_soap_request', 'change_service', tostring(doc)), 
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
            elem = Element('result')
            elem.text = 'true'
            return self._response('change_service', elem)
        else:
            return self._fault('Service not changed')                                                      