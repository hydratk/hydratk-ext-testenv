# -*- coding: utf-8 -*-
"""This code is part of TestEnv extension

.. module:: testenv.interfaces.db_int
   :platform: Unix
   :synopsis: DB interface methods to be used in helpers
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.core.masterhead import MasterHead
from hydratk.extensions.testenv.entities.crm_entities import Customer, Payer, Subscriber, Service
from hydratk.extensions.testenv.entities.crm_entities import Contact, ContactRole, Address, AddressRole
from os import path
from sqlite3 import Error, connect, Row

class DB_INT():
    
    _mh = None    
    _db_file = None
    _conn = None
    
    def __init__(self):
        """Class constructor
           
        Called when the object is initialized    
           
        """           
        
        self._mh = MasterHead.get_head()
        self._db_file = path.join(self._mh.cfg['Extensions']['TestEnv']['ext_dir'], 
                                  self._mh.cfg['Extensions']['TestEnv']['db_file'])
        
    def connect(self):
        """Method connects to database
        
        Args:            
             
        Returns:
           bool: result
                
        """        
        
        try:
                    
            self._conn = connect(self._db_file)
            self._conn.execute('PRAGMA foreign_keys = ON')
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_connected'), self._mh.fromhere())
            
            return True
        
        except Error, ex:
            self._mh.dmsg('htk_on_extension_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False        

    def disconnect(self):
        """Method disconnects from database
        
        Args:            
             
        Returns:
          bool: result
                
        """        
        
        try:
                    
            self._conn.close()
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_disconnected'), self._mh.fromhere())
            
            return True
        
        except Error, ex:
            self._mh.dmsg('htk_on_extension_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False        
        
    def read_customer(self, id):
        """Method reads customer
        
        Args:
           id (int): customer id           
             
        Returns:
           obj: crm_entities.Customer
                
        """        
        
        try:
            
            msg = 'id:{0}'.format(id)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_func', 'read_customer', msg), 
                          self._mh.fromhere())
            
            query = 'SELECT a.id, a.name, b.title AS status, a.segment, a.birth_no, a.reg_no, a.tax_no ' + \
                    'FROM customer a, lov_status b WHERE a.id = ? AND a.status = b.id'
                   
            self._conn.row_factory = Row 
            cur = self._conn.cursor()
            cur.execute(query, (id, ))
            
            row = cur.fetchone()
            if (row == None):
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_unknown_entity', 'customer', id), 
                              self._mh.fromhere())
                return None

            customer = Customer(row['id'], row['name'], row['status'], row['segment'], 
                                row['birth_no'], row['reg_no'], row['tax_no'])
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_entity_found', 'customer', customer),
                          self._mh.fromhere())
                                            
            return customer                                             
            
        except Error, ex:
            self._mh.dmsg('htk_on_extension_error', 'error: {0}'.format(ex), self._mh.fromhere())
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
           int - created customer id
                
        """           
        
        try:
            
            msg = 'name:{0}, status:{1}, segment:{2}, birth_no:{3}, reg_no:{4}, tax_no:{5}'.format(
                   name, status, segment, birth_no, reg_no, tax_no)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_func', 'create_customer', msg), 
                          self._mh.fromhere())         
                           
            query = 'SELECT id FROM lov_status WHERE title = ?'
            cur = self._conn.cursor()
            cur.execute(query, (status, ))
            row = cur.fetchone()
            status_id = row[0] if (row != None) else None
            
            query = 'INSERT INTO customer (name, status, segment, birth_no, reg_no, tax_no, create_date) ' + \
                    'VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)'
                
            cur.execute(query, (name, status_id, segment, birth_no, reg_no, tax_no))                                    
            id = cur.lastrowid
            
            query = 'INSERT INTO history (event_date, table_name, table_id, event, log) ' + \
                    'VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?)'
            log = u'id:{0}|name:{1}|status:{2}|segment:{3}'.format(id, name, status, segment) + \
                  u'|birth_no:{0}|reg_no:{1}|tax_no:{2}'.format(birth_no, reg_no, tax_no)
                  
            cur.execute(query, ('customer', id, 'create_customer', log))            
            self._conn.commit()
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_entity_created', 'customer', id), 
                          self._mh.fromhere())
            
            return id
            
        except Error, ex:
            self._mh.dmsg('htk_on_extension_error', 'error: {0}'.format(ex), self._mh.fromhere())
            self._conn.rollback()
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
        
        try:
            
            msg = 'id:{0}, name:{1}, status:{2}, segment:{3}, birth_no:{4}, reg_no:{5}, tax_no:{6}'. format(
                   id, name, status, segment, birth_no, reg_no, tax_no)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_func', 'change_customer', msg), 
                          self._mh.fromhere())
                        
            query = 'SELECT COUNT(*) FROM customer WHERE id = ?'
            cur = self._conn.cursor()
            cur.execute(query, (id, ))
            row = cur.fetchone()
            if (row[0] == 0):
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_unknown_entity', 'customer', id), 
                              self._mh.fromhere())
                return False         
                        
            query = 'UPDATE customer SET {0}, modify_date = CURRENT_TIMESTAMP WHERE id = ?'                    
            
            if (name != None):
                self._conn.execute(query.format('name = ?'), (name, id))
            if (status != None):
                query2 = 'SELECT id FROM lov_status WHERE title = ?'                
                cur.execute(query2, (status, ))
                row = cur.fetchone()
                status_id = row[0] if (row != None) else None             
                
                self._conn.execute(query.format('status = ?'), (status_id, id))
            if (segment != None):
                self._conn.execute(query.format('segment = ?'), (segment, id))
            if (birth_no != None):
                self._conn.execute(query.format('birth_no = ?'), (birth_no, id))
            if (reg_no != None):
                self._conn.execute(query.format('reg_no = ?'), (reg_no, id))
            if (tax_no != None):
                self._conn.execute(query.format('tax_no = ?'), (tax_no, id))  
                
            query = 'INSERT INTO history (event_date, table_name, table_id, event, log) ' + \
                    'VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?)'
            log = u'id:{0}|name:{1}|status:{2}|segment:{3}'.format(id, name, status, segment) + \
                  u'|birth_no:{0}|reg_no:{1}|tax_no:{2}'.format(birth_no, reg_no, tax_no)
                  
            self._conn.execute(query, ('customer', id, 'change_customer', log))
            self._conn.commit()     
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_entity_changed', 'customer', id), 
                          self._mh.fromhere())                                                                         
            
            return True
            
        except Error, ex:
            self._mh.dmsg('htk_on_extension_error', 'error: {0}'.format(ex), self._mh.fromhere())
            self._conn.rollback()
            return False
        
    def read_payer(self, id):
        """Method reads payer
        
        Args:
           id (int): payer id          
             
        Returns:
           obj: crm_entities.Payer
                
        """           
        
        try:
            
            msg = 'id:{0}'.format(id)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_func', 'read_Payer', msg), 
                          self._mh.fromhere())          
            
            query = 'SELECT a.id, a.name, b.title AS status, a.billcycle, a.bank_account, a.customer ' + \
                    'FROM payer a, lov_status b WHERE a.id = ? AND a.status = b.id'
                    
            self._conn.row_factory = Row 
            cur = self._conn.cursor()
            cur.execute(query, (id, ))
            
            row = cur.fetchone()
            if (row == None):
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_unknown_entity', 'payer', id), 
                              self._mh.fromhere())              
                return None

            payer = Payer(row['id'], row['name'], row['status'], row['billcycle'], 
                          row['customer'], row['bank_account'])
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_entity_found', 'payer', payer),
                          self._mh.fromhere())  
                                         
            return payer                                             
            
        except Error, ex:
            self._mh.dmsg('htk_on_extension_error', 'error: {0}'.format(ex), self._mh.fromhere())
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
        
        try:
        
            msg = 'name:{0}, status:{1}, billcycle:{2}, bank_account:{3}, customer:{4}'.format(
                   name, status, billcycle, bank_account, customer)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_func', 'create_payer', msg), 
                          self._mh.fromhere())
                                   
            query = 'SELECT id FROM lov_status WHERE title = ?'
            cur = self._conn.cursor()
            cur.execute(query, (status, ))
            row = cur.fetchone()
            status_id = row[0] if (row != None) else None
        
            query = 'INSERT INTO payer (name, status, billcycle, bank_account, customer, create_date) ' + \
                    'VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)'
                
            cur.execute(query, (name, status_id, billcycle, bank_account, customer))                                    
            id = cur.lastrowid
            
            query = 'INSERT INTO history (event_date, table_name, table_id, event, log) ' + \
                    'VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?)'
            log = u'id:{0}|name:{1}|status:{2}|billcycle:{3}'.format(id, name, status, billcycle) + \
                  u'|bank_account:{0}|customer:{1}'.format(bank_account, customer)
                  
            cur.execute(query, ('payer', id, 'create_payer', log))            
            self._conn.commit()
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_entity_created', 'payer', id), 
                          self._mh.fromhere())
            
            return id
            
        except Error, ex:
            self._mh.dmsg('htk_on_extension_error', 'error: {0}'.format(ex), self._mh.fromhere())
            self._conn.rollback()
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
        
        try:
            
            msg = 'id:{0}, name:{1}, status:{2}, billcycle:{3}, bank_account:{4}, customer:{5}'.format(
                   id, name, status, billcycle, bank_account, customer)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_func', 'change_payer', msg), 
                          self._mh.fromhere())  
            
            query = 'SELECT COUNT(*) FROM payer WHERE id = ?'
            cur = self._conn.cursor()
            cur.execute(query, (id, ))
            row = cur.fetchone()
            if (row[0] == 0):
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_unknown_entity', 'payer', id), 
                              self._mh.fromhere())
                return False               
                                       
            query = 'UPDATE payer SET {0}, modify_date = CURRENT_TIMESTAMP WHERE id = ?'
            
            if (name != None):
                self._conn.execute(query.format('name = ?'), (name, id))
            if (status != None):
                query2 = 'SELECT id FROM lov_status WHERE title = ?'
                cur.execute(query2, (status, ))
                row = cur.fetchone()
                status_id = row[0] if (row != None) else None              
                
                self._conn.execute(query.format('status = ?'), (status_id, id))
            if (billcycle != None):
                self._conn.execute(query.format('billcycle = ?'), (billcycle, id))
            if (bank_account != None):
                self._conn.execute(query.format('bank_account = ?'), (bank_account, id))
            if (customer != None):
                self._conn.execute(query.format('customer = ?'), (customer, id))
                
            query = 'INSERT INTO history (event_date, table_name, table_id, event, log) ' + \
                    'VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?)'
            log = u'id:{0}|name:{1}|status:{2}|billcycle:{3}'.format(id, name, status, billcycle) + \
                  u'|bank_account:{0}|customer:{1}'.format(bank_account, customer)
                  
            self._conn.execute(query, ('payer', id, 'change_payer', log))
            self._conn.commit()   
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_entity_changed', 'payer', id), 
                          self._mh.fromhere())                                                                                 
            
            return True
            
        except Error, ex:
            self._mh.dmsg('htk_on_extension_error', 'error: {0}'.format(ex), self._mh.fromhere())
            self._conn.rollback()
            return False 
        
    def read_subscriber(self, id):
        """Method reads subscriber
        
        Args:
           id (int): subscriber id           
             
        Returns:
           obj: crm_entities.Subscriber
                
        """           
        
        try:
            
            msg = 'id:{0}'.format(id)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_func', 'read_subscriber', msg), 
                          self._mh.fromhere())
                       
            query = 'SELECT a.id, a.name, a.msisdn, b.title AS status, a.market, a.tariff, a.customer, a.payer ' + \
                    'FROM subscriber a, lov_status b WHERE a.id = ? AND a.status = b.id'
                    
            self._conn.row_factory = Row 
            cur = self._conn.cursor()
            cur.execute(query, (id, ))
            
            row = cur.fetchone()
            if (row == None):
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_unknown_entity', 'subscriber', id), 
                              self._mh.fromhere())               
                return None

            subscriber = Subscriber(row['id'], row['name'], row['msisdn'], row['status'], 
                                    row['market'], row['tariff'], row['customer'], row['payer'])
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_entity_found', 'subscriber', subscriber),
                          self._mh.fromhere()) 
                                            
            return subscriber                                             
            
        except Error, ex:
            self._mh.dmsg('htk_on_extension_error', 'error: {0}'.format(ex), self._mh.fromhere())
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
        
        try:
        
            msg = 'name:{0}, msisdn:{1}, status:{2}, market:{3}, tariff:{4}, customer:{5}, payer:{6}'.format(
                   name, msisdn, status, market, tariff, customer, payer)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_func', 'create_subscriber', msg), 
                          self._mh.fromhere())                       
            
            query = 'SELECT id FROM lov_status WHERE title = ?'
            cur = self._conn.cursor()
            cur.execute(query, (status, ))
            row = cur.fetchone()
            status_id = row[0] if (row != None) else None
        
            query = 'INSERT INTO subscriber (name, msisdn, status, market, tariff, customer, payer, create_date) ' + \
                    'VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)'
                
            cur.execute(query, (name, msisdn, status_id, market, tariff, customer, payer))                                
            id = cur.lastrowid
            
            query = 'INSERT INTO history (event_date, table_name, table_id, event, log) ' + \
                    'VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?)'
            log = u'id:{0}|name:{1}|msisdn:{2}|status:{3}|market:{4}'.format(id, name, msisdn, status, market) + \
                  u'|tariff:{0}|customer:{1}|payer:{2}'.format(tariff, customer, payer)
                  
            cur.execute(query, ('subscriber', id, 'create_subscriber', log))            
            self._conn.commit()
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_entity_created', 'subscriber', id), 
                          self._mh.fromhere())
            
            return id
            
        except Error, ex:
            self._mh.dmsg('htk_on_extension_error', 'error: {0}'.format(ex), self._mh.fromhere())
            self._conn.rollback()
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
           result - bool
        
        """             
        
        try:
            
            msg = 'id:{0}, name:{1}, msisdn:{2}, status:{3}, market:{4}, tariff:{5}, customer:{6}, payer:{7}'.format(
                   id, name, msisdn, status, market, tariff, customer, payer)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_func', 'change_subscriber', msg), 
                          self._mh.fromhere())
              
            query = 'SELECT COUNT(*) FROM subscriber WHERE id = ?'
            cur = self._conn.cursor()
            cur.execute(query, (id, ))
            row = cur.fetchone()
            if (row[0] == 0):
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_unknown_entity', 'subscriber', id), 
                              self._mh.fromhere())
                return False               
                                      
            query = 'UPDATE subscriber SET {0}, modify_date = CURRENT_TIMESTAMP WHERE id = ?'
            
            if (name != None):
                self._conn.execute(query.format('name = ?'), (name, id))
            if (msisdn != None):
                self._conn.execute(query.format('msisdn = ?'), (msisdn, id))                
            if (status != None):
                query2 = 'SELECT id FROM lov_status WHERE title = ?'
                cur.execute(query2, (status, ))
                row = cur.fetchone()
                status_id = row[0] if (row != None) else None              
                
                self._conn.execute(query.format('status = ?'), (status_id, id))
            if (market != None):
                self._conn.execute(query.format('market = ?'), (market, id))
            if (tariff != None):
                self._conn.execute(query.format('tariff = ?'), (tariff, id))
            if (customer != None):
                self._conn.execute(query.format('customer = ?'), (customer, id))
            if (payer != None):
                self._conn.execute(query.format('payer = ?'), (payer, id))  
                
            query = 'INSERT INTO history (event_date, table_name, table_id, event, log) ' + \
                    'VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?)'
            log = u'id:{0}|name:{1}|msisdn:{2}|status:{3}|market:{4}'.format(id, name, msisdn, status, market) + \
                  u'|tariff:{0}|customer:{1}|payer:{2}'.format(tariff, customer, payer)
                  
            self._conn.execute(query, ('subscriber', id, 'change_subscriber', log))
            self._conn.commit()   
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_entity_changed', 'subscriber', id), 
                          self._mh.fromhere())                                                                           
            
            return True
            
        except Error, ex:
            self._mh.dmsg('htk_on_extension_error', 'error: {0}'.format(ex), self._mh.fromhere())
            self._conn.rollback()
            return False  
        
    def read_contact(self, id):
        """Method reads contact
        
        Args:
           id (int): contact id         
             
        Returns:
           obj: crm_entities.Contact
                
        """           
        
        try:
            
            msg = 'id:{0}'.format(id)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_func', 'read_contact', msg), 
                          self._mh.fromhere())
                      
            query = 'SELECT a.id, a.name, a.phone, a.email, ' + \
                    'c.title, b.customer, b.payer, b.subscriber ' + \
                    'FROM contact a LEFT JOIN contact_role b ON a.id = b.contact ' + \
                    'LEFT JOIN lov_contact_role c ON b.contact_role = c.id ' + \
                    'WHERE a.id = ?'
                    
            self._conn.row_factory = Row 
            cur = self._conn.cursor()
            cur.execute(query, (id, ))
            
            rows = cur.fetchall()
            if (cur.rowcount == 0):
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_unknown_entity', 'contact', id), 
                              self._mh.fromhere())              
                return None
            
            first = True
            id = None
            name = None
            phone = None
            email = None
            roles = []
            
            for row in rows:
                           
                if (first):
                    
                    id = row['id']
                    name = row['name']
                    phone = row['phone']
                    email = row['email']
                    first = False 
                    
                if (row['title'] != None):
                    roles.append(ContactRole(row['id'], row['title'], row['customer'],
                                             row['payer'], row['subscriber']))   

            contact = Contact(id, name, phone, email, roles)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_entity_found', 'contact', contact),
                          self._mh.fromhere())                    
                                             
            return contact                                             
            
        except Error, ex:
            self._mh.dmsg('htk_on_extension_error', 'error: {0}'.format(ex), self._mh.fromhere())
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
        
        try:
            
            msg = 'name:{0}, phone:{1}, email:{2}'.format(name, phone, email)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_func', 'create_contact', msg), 
                          self._mh.fromhere())          
        
            query = 'INSERT INTO contact (name, phone, email, create_date) ' + \
                    'VALUES (?, ?, ?, CURRENT_TIMESTAMP)'
                    
            cur = self._conn.cursor()                  
            cur.execute(query, (name, phone, email))                                
            id = cur.lastrowid
            
            query = 'INSERT INTO history (event_date, table_name, table_id, event, log) ' + \
                    'VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?)'
            log = u'id:{0}|name:{1}|phone:{2}|email:{3}'.format(id, name, phone, email)
                  
            cur.execute(query, ('contact', id, 'create_contact', log))            
            self._conn.commit()
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_entity_created', 'contact', id), 
                          self._mh.fromhere())
            
            return id
            
        except Error, ex:
            self._mh.dmsg('htk_on_extension_error', 'error: {0}'.format(ex), self._mh.fromhere())
            self._conn.rollback()
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
        
        try:
            
            msg = 'id:{0}, name:{1}, phone:{2}, email:{3}'.format(id, name, phone, email)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_func', 'change_contact', msg), 
                          self._mh.fromhere())           
            
            query = 'SELECT COUNT(*) FROM contact WHERE id = ?'
            cur = self._conn.cursor()
            cur.execute(query, (id, ))
            row = cur.fetchone()
            if (row[0] == 0):
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_unknown_entity', 'contact', id), 
                              self._mh.fromhere())
                return False             
            
            query = 'UPDATE contact SET {0}, modify_date = CURRENT_TIMESTAMP WHERE id = ?'
            
            if (name != None):
                self._conn.execute(query.format('name = ?'), (name, id))
            if (phone != None):
                self._conn.execute(query.format('phone = ?'), (phone, id))
            if (email != None):
                self._conn.execute(query.format('email = ?'), (email, id))
                
            query = 'INSERT INTO history (event_date, table_name, table_id, event, log) ' + \
                    'VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?)'
            log = u'id:{0}|name:{1}|phone:{2}|email:{3}'.format(id, name, phone, email)
                  
            self._conn.execute(query, ('contact', id, 'change_contact', log))
            self._conn.commit()     
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_entity_changed', 'contact', id), 
                          self._mh.fromhere())                                                                             
            
            return True
            
        except Error, ex:
            self._mh.dmsg('htk_on_extension_error', 'error: {0}'.format(ex), self._mh.fromhere())
            self._conn.rollback()
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
        
        try:
            
            msg = 'id:{0}, role:{1}, customer:{2}, payer:{3}, subscriber:{4}'.format(
                   id, role, customer, payer, subscriber)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_func', 'assign_contact_role', msg), 
                          self._mh.fromhere())
            
            query = 'SELECT id FROM lov_contact_role WHERE title = ?'            
            cur = self._conn.cursor()
            cur.execute(query, (role, ))
            row = cur.fetchone()
            role_id = row[0] if (row != None) else None
            
            query = 'INSERT INTO contact_role (contact_role, contact, customer, payer, subscriber, create_date) ' + \
                    'VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)'
                
            self._conn.execute(query, (role_id, id, customer, payer, subscriber))            
                     
            cur = self._conn.cursor()   
            cur.execute('SELECT last_insert_rowid()')   
            rec_id = cur.fetchone()[0]                 
            
            query = 'INSERT INTO history (event_date, table_name, table_id, event, log) ' + \
                    'VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?)'
            log = u'id:{0}|role:{1}|customer:{2}|payer:{3}'.format(id, role, customer, payer) + \
                  u'|subscriber:{0}'.format(subscriber)
                  
            self._conn.execute(query, ('contact', rec_id, 'assign_contact_role', log))
            self._conn.commit()     
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_role_assigned', 'contact'), 
                          self._mh.fromhere())        
            
            return True
            
        except Error, ex:
            self._mh.dmsg('htk_on_extension_error', 'error: {0}'.format(ex), self._mh.fromhere())
            self._conn.rollback()
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
        
        try:
            
            msg = 'id:{0}, role:{1}, customer:{2}, payer:{3}, subscriber:{4}'.format(
                   id, role, customer, payer, subscriber)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_func', 'revoke_contact_role', msg), 
                          self._mh.fromhere())
            
            query = 'SELECT id FROM lov_contact_role WHERE title = ?'            
            cur = self._conn.cursor()
            cur.execute(query, (role, ))
            row = cur.fetchone()
            role_id = row[0] if (row != None) else None
            
            query = 'SELECT id FROM contact_role WHERE contact_role = ? AND contact = ? {0}' 
            if (customer != None):
                cur.execute(query.format('AND customer = ?'), (role_id, id, customer))
            elif (payer != None):
                cur.execute(query.format('AND payer = ?'), (role_id, id, payer))
            elif (subscriber != None):
                cur.execute(query.format('AND subscriber = ?'), (role_id, id, subscriber))
            
            row = cur.fetchone()
            rec_id = row[0] if (row != None) else None
            if (rec_id == None):
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_unknown_role'), self._mh.fromhere())  
                return False
            
            query = 'DELETE FROM contact_role where id = ?'
            self._conn.execute(query, (rec_id, ))
            
            query = 'INSERT INTO history (event_date, table_name, table_id, event, log) ' + \
                    'VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?)'
            log = u'id:{0}|role:{1}|customer:{2}|payer:{3}'.format(id, role, customer, payer) + \
                  u'|subscriber:{0}'.format(subscriber)
                  
            self._conn.execute(query, ('contact', rec_id, 'revoke_contact_role', log))
            self._conn.commit()    
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_role_revoke', 'contact'), 
                          self._mh.fromhere())         
            
            return True
            
        except Error, ex:
            self._mh.dmsg('htk_on_extension_error', 'error: {0}'.format(ex), self._mh.fromhere())
            self._conn.rollback()
            return False              
        
    def read_address(self, id):
        """Method reads address
        
        Args:
           id (int): address id         
             
        Returns:
           obj: crm_entities.Address 
                
        """           
        
        try:
            
            msg = 'id:{0}'.format(id)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_func', 'read_address', msg), 
                          self._mh.fromhere())
                      
            query = 'SELECT a.id, a.street, a.street_no, a.city, a.zip, ' + \
                    'c.title, b.contact, b.customer, b.payer, b.subscriber ' + \
                    'FROM address a LEFT JOIN address_role b ON a.id = b.address ' + \
                    'LEFT JOIN lov_address_role c ON b.address_role = c.id ' + \
                    'WHERE a.id = ?'
                    
            self._conn.row_factory = Row 
            cur = self._conn.cursor()
            cur.execute(query, (id, ))
            
            rows = cur.fetchall()
            if (cur.rowcount == 0):
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_unknown_entity', 'address', id), 
                              self._mh.fromhere())            
                return None
            
            first = True
            id = None
            street = None
            street_no = None
            city = None
            zip = None
            roles = []
            
            for row in rows:
                
                if (first):
                    
                    id = row['id']
                    street = row['street']
                    street_no = row['street_no']
                    city = row['city']
                    zip = row['zip']
                    first = False 
                    
                if (row['title'] != None):
                    roles.append(AddressRole(row['id'], row['title'], row['contact'], 
                                             row['customer'], row['payer'], row['subscriber']))

            address = Address(id, street, street_no, city, zip, roles)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_entity_found', 'address', address),
                          self._mh.fromhere())
                                             
            return address                                             
            
        except Error, ex:
            self._mh.dmsg('htk_on_extension_error', 'error: {0}'.format(ex), self._mh.fromhere())
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
        
        try:
        
            msg = 'street:{0}, street_no:{1}, city:{2}, zip:{3}'.format(street, street_no, city, zip)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_func', 'create_address', msg), 
                          self._mh.fromhere())         
        
            query = 'INSERT INTO address (street, street_no, city, zip, create_date) ' + \
                    'VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)'
                
            cur = self._conn.cursor()                 
            cur.execute(query, (street, street_no, city, zip))                                              
            id = cur.lastrowid
            
            query = 'INSERT INTO history (event_date, table_name, table_id, event, log) ' + \
                    'VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?)'
            log = u'id:{0}|street:{1}|street_no:{2}|city:{3}'.format(id, street, street_no, city) + \
                  u'|zip:{0}'.format(zip)
                  
            cur.execute(query, ('address', id, 'create_address', log))            
            self._conn.commit()
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_entity_created', 'address', id), 
                          self._mh.fromhere())
            
            return id
            
        except Error, ex:
            self._mh.dmsg('htk_on_extension_error', 'error: {0}'.format(ex), self._mh.fromhere())
            self._conn.rollback()
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
        
        try:
            
            msg = 'id:{0}, street:{1}, street_no:{2}, city:{3}, zip:{4}'.format(id, street, street_no, city, zip)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_func', 'change_address', msg), 
                          self._mh.fromhere())            
            
            query = 'SELECT COUNT(*) FROM address WHERE id = ?'
            cur = self._conn.cursor()
            cur.execute(query, (id, ))
            row = cur.fetchone()
            if (row[0] == 0):
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_unknown_entity', 'address', id), 
                              self._mh.fromhere())
                return False             
            
            query = 'UPDATE address SET {0}, modify_date = CURRENT_TIMESTAMP WHERE id = ?'
            
            if (street != None):
                self._conn.execute(query.format('street = ?'), (street, id))
            if (street_no != None):
                self._conn.execute(query.format('street_no = ?'), (street_no, id))
            if (city != None):
                self._conn.execute(query.format('city = ?'), (city, id))
            if (zip != None):
                self._conn.execute(query.format('zip = ?'), (zip, id))                
                
            query = 'INSERT INTO history (event_date, table_name, table_id, event, log) ' + \
                    'VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?)'
            log = u'id:{0}|street:{1}|street_no:{2}|city:{3}'.format(id, street, street_no, city) + \
                  u'|zip:{0}'.format(zip)
                  
            self._conn.execute(query, ('address', id, 'change_address', log))
            self._conn.commit()                  
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_entity_changed', 'address', id), 
                          self._mh.fromhere())                                                                
            
            return True
            
        except Error, ex:
            self._mh.dmsg('htk_on_extension_error', 'error: {0}'.format(ex), self._mh.fromhere())
            self._conn.rollback()
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
        
        try:
            
            msg = 'id:{0}, role:{1}, contact:{2}, customer:{3}, payer:{4}, subscriber:{5}'.format(
                   id, role, contact, customer, payer, subscriber)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_func', 'assign_address_role', msg), 
                          self._mh.fromhere())
            
            query = 'SELECT id FROM lov_address_role WHERE title = ?'
            cur = self._conn.cursor()
            cur.execute(query, (role, ))
            row = cur.fetchone()
            role_id = row[0] if (row != None) else None            
            
            query = 'INSERT INTO address_role (address_role, address, contact, customer, payer, subscriber, create_date) ' + \
                    'VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)'
                
            self._conn.execute(query, (role_id, id, contact, customer, payer, subscriber))            
                     
            cur = self._conn.cursor()   
            cur.execute('SELECT last_insert_rowid()')   
            rec_id = cur.fetchone()[0]                 
            
            query = 'INSERT INTO history (event_date, table_name, table_id, event, log) ' + \
                    'VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?)'
            log = u'id:{0}|role:{1}|contact:{2}|customer:{3}'.format(id, role, contact, customer) + \
                  u'|payer:{0}|subscriber:{1}'.format(payer, subscriber)
                  
            self._conn.execute(query, ('address', rec_id, 'assign_address_role', log))
            self._conn.commit()    
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_role_assigned', 'address'), 
                          self._mh.fromhere())         
            
            return True
            
        except Error, ex:
            self._mh.dmsg('htk_on_extension_error', 'error: {0}'.format(ex), self._mh.fromhere())
            self._conn.rollback()
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
        
        try:
            
            msg = 'id:{0}, role:{1}, contact:{2}, customer:{3}, payer:{4}, subscriber:{5}'.format(
                   id, role, contact, customer, payer, subscriber)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_func', 'revoke_address_role', msg), 
                          self._mh.fromhere())
            
            query = 'SELECT id FROM lov_address_role WHERE title = ?'
            cur = self._conn.cursor()
            cur.execute(query, (role, ))
            row = cur.fetchone()
            role_id = row[0] if (row != None) else None
            
            query = 'SELECT id FROM address_role WHERE address_role = ? AND address = ? {0}' 
            if (contact != None):
                cur.execute(query.format('AND contact = ?'), (role_id, id, contact))            
            elif (customer != None):
                cur.execute(query.format('AND customer = ?'), (role_id, id, customer))
            elif (payer != None):
                cur.execute(query.format('AND payer = ?'), (role_id, id, payer))
            elif (subscriber != None):
                cur.execute(query.format('AND subscriber = ?'), (role_id, id, subscriber))
            
            row = cur.fetchone()
            rec_id = row[0] if (row != None) else None
            if (rec_id == None):
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_unknown_role'), self._mh.fromhere())  
                return False
            
            query = 'DELETE FROM address_role where id = ?'
            self._conn.execute(query, (rec_id, ))
            
            query = 'INSERT INTO history (event_date, table_name, table_id, event, log) ' + \
                    'VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?)'
            log = u'id:{0}|role:{1}|contact:{2}|customer:{3}'.format(id, role, contact, customer) + \
                  u'|payer:{0}|subscriber:{1}'.format(payer, subscriber)
                  
            self._conn.execute(query, ('address', rec_id, 'revoke_address_role', log))
            self._conn.commit()  
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_role_revoked', 'address'), 
                          self._mh.fromhere())            
            
            return True
            
        except Error, ex:
            self._mh.dmsg('htk_on_extension_error', 'error: {0}'.format(ex), self._mh.fromhere())
            self._conn.rollback()
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
        
        try:
            
            msg = 'customer:{0}, payer:{1}, subscriber:{2}, service:{3}'.format(
                   customer, payer, subscriber, service)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_func', 'read_services', msg), 
                          self._mh.fromhere())
            
            query = 'SELECT a.service, c.title, d.title AS status, b.param, b.value ' + \
                    'FROM service a LEFT JOIN service_params b ON a.id = b.service ' + \
                    'JOIN lov_service c ON a.service = c.id JOIN lov_status d ON a.status = d.id ' + \
                    'WHERE '
            self._conn.row_factory = Row
            cur = self._conn.cursor()                     
                    
            entity = None
            if (customer != None):
                query += 'a.customer = ?'
                entity = customer
            elif (payer != None):
                query += 'a.payer = ?'
                entity = payer
            elif (subscriber != None):
                query += 'a.subscriber = ?'
                entity = subscriber  
                
            if (service == None):
                query += ''
                cur.execute(query, (entity, ))
            else:
                query += ' AND a.service = ?'
                cur.execute(query, (entity, service))          
            
            rows = cur.fetchall()                   
            
            if (len(rows) > 0):

                curr = None
                services = []
                id = None
                title = None
                status = None
                params = None               

                for row in rows:
                    
                    id = row['service']
                
                    # store service
                    if (curr != None and curr != id):
                        services.append(Service(curr, title, status, params))
                        
                    # new service
                    if (curr == None or curr != id):
                        curr = id
                        title = row['title']
                        status = row['status']
                        params = {} 
                    
                    # store param
                    if (row['param'] != None):
                        params[row['param']] = row['value']
                    
                # last service
                if (id != None):
                    services.append(Service(id, title, status, params))  
                
                for service in services:    
                    self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_entity_found', 'service', service),
                                  self._mh.fromhere())
                    
                return services 
            
            else:
                return None  
            
        except Error, ex:
            self._mh.dmsg('htk_on_extension_error', 'error: {0}'.format(ex), self._mh.fromhere())
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
        
        try:
            
            msg = 'service:{0}, customer:{1}, payer:{2}, subscriber:{3}, status:{4}, params:{5}'.format(
                   service, customer, payer, subscriber, status, params)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_func', 'create_service', msg), 
                          self._mh.fromhere())
            
            query = 'SELECT customer, payer, subscriber FROM lov_service WHERE id = ?'
            self._conn.row_factory = Row
            cur = self._conn.cursor()
            cur.execute(query, (service, ))
            row = cur.fetchone()            
                            
            if (cur.rowcount == 0):
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_unknown_entity', 'service', service),
                              self._mh.fromhere())
                return False
            
            if (customer != None):
                
                if (row['customer'] != 1):
                    self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_srv_forbidden', service, 'customer'),
                                  self._mh.fromhere())
                    return False
                
                query = 'SELECT id FROM service WHERE service = ? AND customer = ?'
                cur.execute(query, (service, customer))
                if (cur.rowcount > 0):
                    self._mh.dmsg('htk_on_extension_error', self._mh._trn.msg('te_db_srv_assigned', service), 
                                  self._mh.fromhere())
                    return False
                
                query = 'INSERT INTO service (service, status, customer, create_date) ' + \
                        'VALUES (?, ?, ?, CURRENT_TIMESTAMP)'  
                
            elif (payer != None):
                
                if (row['payer'] != 1):
                    self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_srv_forbidden', service, 'payer'),
                                  self._mh.fromhere())
                    return False
                
                query = 'SELECT id FROM service WHERE service = ? AND payer = ?'
                cur.execute(query, (service, payer))
                if (cur.rowcount > 0):
                    self._mh.dmsg('htk_on_extension_error', self._mh._trn.msg('te_db_srv_assigned', service), 
                                  self._mh.fromhere())
                    return False
                
            elif (subscriber != None):
                
                if (row['subscriber'] != 1):
                    self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_srv_forbidden', service, 'subscriber'),
                                  self._mh.fromhere())
                    return False
                
                query = 'SELECT id FROM service WHERE service = ? AND subscriber = ?'
                cur.execute(query, (service, subscriber))
                if (cur.rowcount > 0):
                    self._mh.dmsg('htk_on_extension_error', self._mh._trn.msg('te_db_srv_assigned', service), 
                                  self._mh.fromhere())
                    return False   
                
            query = 'SELECT id FROM lov_status WHERE title = ?'
            cur = self._conn.cursor()
            cur.execute(query, (status, ))
            row = cur.fetchone()
            status_id = row[0] if (row != None) else None

            query = 'INSERT INTO service (service, status, customer, payer, subscriber, create_date) ' + \
                    'VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)'  
            cur.execute(query, (service, status_id, customer, payer, subscriber))
            id = cur.lastrowid

            log = u'service:{0}|status:{1}|customer:{2}|payer:{3}'.format(service, status, customer, payer) +\
                  u'|subscriber:{0}|params#'.format(subscriber) 
            
            if (len(params) > 0):
                for key, value in params.items():
                           
                    query = 'SELECT mandatory, default_value from lov_service_param WHERE service = ? AND id = ?'
                    cur.execute(query, (service, key))
                    row = cur.fetchone()
                    
                    if (cur.rowcount == 0):
                        self._mh.dmsg('htk_on_extension_error', self._mh._trn.msg('te_db_unknown_srv_param', service, key), 
                                      self._mh.fromhere())
                        self._conn.rollback()
                        return False
                    elif (row['mandatory'] == 1 and value == None):
                        self._mh.dmsg('htk_on_extension_error', self._mh._trn.msg('te_db_mandatory_param'), key, 
                                      self._mh.fromhere())
                        self._conn.rollback()
                        return False 
                    elif (row['mandatory'] == 0 and value == None):                            
                        query = 'INSERT INTO service_params (param, value, service, create_date) ' + \
                                'VALUES (?, ?, ?, CURRENT_TIMESTAMP)'
                        cur.execute(query, (key, row['default_value'], service))
                        log += u'id:{0}|value:{1}'.format(key, row['default_value'])
                    else:
                        query = 'INSERT INTO service_params (param, value, service, create_date) ' + \
                                'VALUES (?, ?, ?, CURRENT_TIMESTAMP)' 
                        cur.execute(query, (key, value, id))  
                        log += u'id:{0}|value:{1}'.format(key, value) 
                        
            query = 'INSERT INTO history (event_date, table_name, table_id, event, log) ' + \
                    'VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?)'                  
            self._conn.execute(query, ('service', id, 'create_service', log))                                                                           
            
            self._conn.commit()
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_entity_created', 'service', id), 
                          self._mh.fromhere())
            
            return True
            
        except Error, ex:
            self._mh.dmsg('htk_on_extension_error', 'error: {0}'.format(ex), self._mh.fromhere())
            self._conn.rollback()
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
        
        try:
            
            msg = 'service:{0}, customer:{1}, payer:{2}, subscriber:{3}, status:{4}, params:{5}'.format(
                   service, customer, payer, subscriber, status, params)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_func', 'change_service', msg), 
                          self._mh.fromhere())
            
            self._conn.row_factory = Row
            cur = self._conn.cursor() 
            id = None      
            
            if (customer != None):
                
                query = 'SELECT id FROM service WHERE service = ? AND customer = ?'
                cur.execute(query, (service, customer))
                row = cur.fetchone()
                
                if (cur.rowcount == 0):
                    self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_unknown_entity', 'service', id), 
                                  self._mh.fromhere())
                    return False
                
            elif (payer != None):
                
                query = 'SELECT id FROM service WHERE service = ? AND payer = ?'
                cur.execute(query, (service, payer))
                row = cur.fetchone()
                
                if (cur.rowcount == 0):
                    self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_unknown_entity', 'service', id), 
                                  self._mh.fromhere())
                    return False              
                
            elif (subscriber != None):
                
                query = 'SELECT id FROM service WHERE service = ? AND subscriber = ?'
                cur.execute(query, (service, subscriber))
                row = cur.fetchone()
                
                if (cur.rowcount == 0):
                    self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_unknown_entity', 'service', id), 
                                  self._mh.fromhere())
                    return False   
                
            id = row[0]                
                
            if (status != None):
                    
                query = 'SELECT id FROM lov_status WHERE title = ?'
                cur = self._conn.cursor()
                cur.execute(query, (status, ))
                row = cur.fetchone()
                status_id = row[0] if (row != None) else None
            
                query = 'UPDATE service SET status = ?, modify_date = CURRENT_TIMESTAMP WHERE id = ?'  
                cur.execute(query, (status_id, id))
             
            log = u'service:{0}|status:{1}|customer:{2}|payer:{3}'.format(service, status, customer, payer) +\
                  u'|subscriber:{0}|params#'.format(subscriber) 
            
            if (len(params) > 0):
                for key, value in params.items():
                           
                    query = 'SELECT a.id, b.mandatory FROM service_params a, lov_service_param b ' + \
                            'WHERE a.service = ? AND a.param = ? AND a.param = b.id'
                    cur.execute(query, (id, key))
                    row = cur.fetchone()
                    
                    if (cur.rowcount == 0):
                        self._mh.dmsg('htk_on_extension_error', self._mh._trn.msg('te_db_param_not_assigned', key),
                                      self._mh.fromhere())
                        self._conn.rollback()
                        return False
                    elif (row['mandatory'] == 1 and value == None):
                        self._mh.dmsg('htk_on_extension_error', self._mh._trn.msg('te_db_mandatory_param', key), 
                                      self._mh.fromhere())
                        self._conn.rollback()
                        return False 
                    else:
                        query = 'UPDATE service_params SET value = ?, modify_date = CURRENT_TIMESTAMP ' + \
                                'WHERE id = ?'
                        cur.execute(query, (value, row['id']))  
                        log += u'id:{0}|value:{1}'.format(key, value) 
                        
            query = 'INSERT INTO history (event_date, table_name, table_id, event, log) ' + \
                    'VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?)'                  
            self._conn.execute(query, ('service', id, 'change_service', log))                                                                           
            
            self._conn.commit()
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_entity_changed', 'service', id), 
                          self._mh.fromhere())      
            
            return True
            
        except Error, ex:
            self._mh.dmsg('htk_on_extension_error', 'error: {0}'.format(ex), self._mh.fromhere())
            self._conn.rollback()
            return False                    