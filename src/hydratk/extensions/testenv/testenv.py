# -*- coding: utf-8 -*-
"""This code is a part of Hydra Toolkit

.. module:: hydratk.extensions.testenv
   :platform: Unix
   :synopsis: TestEnv extension for test automation exercises
.. moduleauthor:: Petr Rašek <pr@hydratk.org>

"""

from hydratk.core import extension;
from hydratk.core import event;
from hydratk.core.masterhead import PYTHON_MAJOR_VERSION
from hydratk.lib.console.commandlinetool import CommandlineTool;
from hydratk.lib.console.commandlinetool import rprint;
from hydratk.lib.compat import utils;
import hydratk.extensions.testenv.application.web_server as web_server;
import hydratk.extensions.testenv.interfaces.db_int as db_int;
import hydratk.extensions.testenv.interfaces.rest_int as rest_int;
import sys;
import os;
import sqlite3 as db;

class Extension(extension.Extension):
    
    def _init_extension(self):
        
        self._ext_id   = 'testenv';
        self._ext_name = 'TestEnv';
        self._ext_version = '0.1.0';
        self._ext_author = 'Petr Rašek <pr@headz.cz>';
        self._ext_year = '2015';  
        
    def _register_actions(self):
        
        self._mh.match_command('testenv-install-db');        
        hook = [{'command' : 'testenv-install-db', 'callback' : self.install_db_fc }];        
        self._mh.register_command_hook(hook); 
        
        self._mh.match_command('testenv-start-server');
        hook = [{'command' : 'testenv-start-server', 'callback' : self.start_server_fc }];  
        self._mh.register_command_hook(hook);       
        
        self._mh.match_command('testenv-run-bist');  
        hook = [{'command' : 'testenv-run-bist', 'callback' : self.run_bist_fc }];     
        self._mh.register_command_hook(hook);  
            
    def install_db_fc(self, ext_call=True): 
            
        try:    
            
            if (ext_call):
                self._mh.dmsg('htk_on_debug_info', 'received testenv-install-db command', self._mh.fromhere());
        
            db_file = self._mh.cfg['Extensions']['TestEnv']['db_file'];
            if (os.path.exists(db_file)):        
                self._mh.dmsg('htk_on_debug_info', 'removing previous db_file {0}'.format(db_file), self._mh.fromhere());
                os.remove(db_file);
                                
            install_file = self._mh.cfg['System']['Extending']['extensions_dir'] + '/testenv/application/install_db.sql';
            if (os.path.exists(install_file)):
            
                with open(install_file, 'r') as file:
                    script = file.read();
            
                self._mh.dmsg('htk_on_debug_info', 'creating db_file {0}'.format(db_file), self._mh.fromhere()); 
                with db.connect(db_file) as conn:
                    self._mh.dmsg('htk_on_debug_info', 'installing database from script {0}'.format(install_file), self._mh.fromhere());
                    cur = conn.cursor();
                    cur.executescript(script);
                    conn.commit();
                    self._mh.dmsg('htk_on_debug_info', 'installion completed', self._mh.fromhere()); 
            else:
                self._mh.dmsg('htk_on_extension_error', 'install file not found', self._mh.fromhere());
                    
        except db.Error, ex:
            self._mh.dmsg('htk_on_extension_error', 'database error: {0}'.format(ex), self._mh.fromhere());
       
    def start_server_fc(self):
        
        self._mh.dmsg('htk_on_debug_info', 'received testenv-start-server command', self._mh.fromhere());  
        server = web_server.Server(self._mh);
        server._start();                   
            
    def run_bist_fc(self):
        
        self._mh.dmsg('htk_on_debug_info', 'received testenv-run-bist command', self._mh.fromhere());        
        self.install_db_fc(False);
        
        self.run_bist_db();
        self.run_bist_rest();
        
        self.install_db_fc(False);
        
    def run_bist_db(self):
        
        self._mh.dmsg('htk_on_debug_info', 'running DB self tests', self._mh.fromhere());
        db = db_int.DB_INT(self._mh);
        db.connect();
        
        # customer operations
        self._mh.dmsg('htk_on_debug_info', 'testing customer operations', self._mh.fromhere());
        cust_id = db.create_customer(name='Charlie Bowman', status='active', segment=2, birth_no='700101/0001', 
                                     reg_no='123456', tax_no='CZ123456');
        db.read_customer(cust_id);
        db.change_customer(id=cust_id, name='Vince Neil', status='deactive', segment=3, birth_no='700101/0002',
                           reg_no='654321', tax_no='CZ654321'); 
        db.read_customer(cust_id);         
        
        # payer operations
        self._mh.dmsg('htk_on_debug_info', 'testing payer operations', self._mh.fromhere());
        pay_id = db.create_payer(name='Charlie Bowman', status='active', billcycle=1, bank_account='123456/0100', 
                                 customer=cust_id);
        db.read_payer(pay_id);
        db.change_payer(id=pay_id, name='Vince Neil', status='deactive', billcycle=2, bank_account='123456/0800'); 
        db.read_payer(pay_id); 
        
        # subscriber operations
        self._mh.dmsg('htk_on_debug_info', 'testing subscriber operations', self._mh.fromhere());
        subs_id = db.create_subscriber(name='Charlie Bowman', msisdn='123456', status='active', market=1, tariff=433, 
                                       customer=cust_id, payer=pay_id);
        db.read_subscriber(subs_id);
        db.change_subscriber(id=subs_id, name='Vince Neil', msisdn='654321', status='deactive', market=2, tariff=434); 
        db.read_subscriber(subs_id);  
        
        # contact operations
        self._mh.dmsg('htk_on_debug_info', 'testing contact operations', self._mh.fromhere());
        con_id = db.create_contact(name='Charlie Bowman', phone='123456', email='aaa@xxx.com');
        db.read_contact(con_id);
        db.change_contact(id=con_id, name='Vince Neil', phone='654321', email='bbb@xxx.com'); 
        db.read_contact(con_id);
        db.assign_contact_role(id=con_id, role='contract', customer=cust_id);
        db.assign_contact_role(id=con_id, role='invoicing', payer=pay_id);
        db.assign_contact_role(id=con_id, role='contact', subscriber=subs_id);  
        db.read_contact(con_id);
        db.revoke_contact_role(id=con_id, role='contract', customer=cust_id);
        db.revoke_contact_role(id=con_id, role='invoicing', payer=pay_id);
        db.revoke_contact_role(id=con_id, role='contact', subscriber=subs_id);  
        db.read_contact(con_id);        
        
        # address operations
        self._mh.dmsg('htk_on_debug_info', 'testing address operations', self._mh.fromhere());
        addr_id = db.create_address(street='Tomickova', street_no='2144/1', city='Praha', zip=14800);
        db.read_address(addr_id);
        db.change_address(id=addr_id, street='Babakova', street_no='2152/6', city='Praha 4', zip=14900); 
        db.read_address(addr_id);     
        db.assign_address_role(id=addr_id, role='contract', customer=cust_id);
        db.assign_address_role(id=addr_id, role='invoicing', payer=pay_id);
        db.assign_address_role(id=addr_id, role='contact', subscriber=subs_id);  
        db.assign_address_role(id=addr_id, role='delivery', contact=con_id);
        db.read_address(con_id);
        db.revoke_address_role(id=addr_id, role='contract', customer=cust_id);
        db.revoke_address_role(id=addr_id, role='invoicing', payer=pay_id);
        db.revoke_address_role(id=addr_id, role='contact', subscriber=subs_id); 
        db.revoke_address_role(id=addr_id, role='delivery', contact=con_id); 
        db.read_address(con_id); 
        
        # service operations
        self._mh.dmsg('htk_on_debug_info', 'testing service operations', self._mh.fromhere());
        db.create_service(service=615, subscriber=subs_id, status='active', params={121:'123456'});  
        db.create_service(service=619, subscriber=subs_id, status='active', params={122:'23001123456', 123:'88123456'}); 
        db.read_services(subscriber=subs_id)[0];    
        db.read_services(subscriber=subs_id)[1]; 
        db.read_services(subscriber=subs_id, service=615)[0];     
        db.change_service(service=615, subscriber=subs_id, status='active', params={121:'654321'});  
        db.change_service(service=619, subscriber=subs_id, status='active', params={122:'23001654321', 123:'88654321'});  
        db.read_services(subscriber=subs_id)[0];  
        db.read_services(subscriber=subs_id, service=619)[0];                                                    
        
        db.disconnect();       
        
    def run_bist_rest(self):
        
        self._mh.dmsg('htk_on_debug_info', 'running REST self tests', self._mh.fromhere());
        rest = rest_int.REST_INT(self._mh);
        
        # customer operations
        self._mh.dmsg('htk_on_debug_info', 'testing customer operations', self._mh.fromhere());
        cust_id = rest.create_customer(name='Charlie Bowman', status='active', segment=2, birth_no='700101/0001', 
                                     reg_no='123456', tax_no='CZ123456');
        rest.read_customer(cust_id);
        rest.change_customer(id=cust_id, name='Vince Neil', status='deactive', segment=3, birth_no='700101/0002',
                             reg_no='654321', tax_no='CZ654321'); 
        rest.read_customer(cust_id);         
        
        # payer operations
        self._mh.dmsg('htk_on_debug_info', 'testing payer operations', self._mh.fromhere());
        pay_id = rest.create_payer(name='Charlie Bowman', status='active', billcycle=1, bank_account='123456/0100', 
                                   customer=cust_id);
        rest.read_payer(pay_id);
        rest.change_payer(id=pay_id, name='Vince Neil', status='deactive', billcycle=2, bank_account='123456/0800'); 
        rest.read_payer(pay_id); 
        
        # subscriber operations
        self._mh.dmsg('htk_on_debug_info', 'testing subscriber operations', self._mh.fromhere());
        subs_id = rest.create_subscriber(name='Charlie Bowman', msisdn='123456', status='active', market=1, tariff=433, 
                                         customer=cust_id, payer=pay_id);
        rest.read_subscriber(subs_id);
        rest.change_subscriber(id=subs_id, name='Vince Neil', msisdn='654321', status='deactive', market=2, tariff=434); 
        rest.read_subscriber(subs_id);  
        
        # contact operations
        self._mh.dmsg('htk_on_debug_info', 'testing contact operations', self._mh.fromhere());
        con_id = rest.create_contact(name='Charlie Bowman', phone='123456', email='aaa@xxx.com');
        rest.read_contact(con_id);
        rest.change_contact(id=con_id, name='Vince Neil', phone='654321', email='bbb@xxx.com'); 
        rest.read_contact(con_id);
        rest.assign_contact_role(id=con_id, role='contract', customer=cust_id);
        rest.assign_contact_role(id=con_id, role='invoicing', payer=pay_id);
        rest.assign_contact_role(id=con_id, role='contact', subscriber=subs_id);  
        rest.read_contact(con_id);
        rest.revoke_contact_role(id=con_id, role='contract', customer=cust_id);
        rest.revoke_contact_role(id=con_id, role='invoicing', payer=pay_id);
        rest.revoke_contact_role(id=con_id, role='contact', subscriber=subs_id);  
        rest.read_contact(con_id);        
        
        # address operations
        self._mh.dmsg('htk_on_debug_info', 'testing address operations', self._mh.fromhere());
        addr_id = rest.create_address(street='Tomickova', street_no='2144/1', city='Praha', zip=14800);
        rest.read_address(addr_id);
        rest.change_address(id=addr_id, street='Babakova', street_no='2152/6', city='Praha 4', zip=14900); 
        rest.read_address(addr_id);     
        rest.assign_address_role(id=addr_id, role='contract', customer=cust_id);
        rest.assign_address_role(id=addr_id, role='invoicing', payer=pay_id);
        rest.assign_address_role(id=addr_id, role='contact', subscriber=subs_id);  
        rest.assign_address_role(id=addr_id, role='delivery', contact=con_id);
        rest.read_address(con_id);
        rest.revoke_address_role(id=addr_id, role='contract', customer=cust_id);
        rest.revoke_address_role(id=addr_id, role='invoicing', payer=pay_id);
        rest.revoke_address_role(id=addr_id, role='contact', subscriber=subs_id); 
        rest.revoke_address_role(id=addr_id, role='delivery', contact=con_id); 
        rest.read_address(con_id); 
        
        # service operations
        self._mh.dmsg('htk_on_debug_info', 'testing service operations', self._mh.fromhere());
        rest.create_service(service=615, subscriber=subs_id, status='active', params={121:'123456'});  
        rest.create_service(service=619, subscriber=subs_id, status='active', params={122:'23001123456', 123:'88123456'}); 
        rest.read_services(subscriber=subs_id)[0];    
        rest.read_services(subscriber=subs_id)[1]; 
        rest.read_services(subscriber=subs_id, service=615)[0];     
        rest.change_service(service=615, subscriber=subs_id, status='active', params={121:'654321'});  
        rest.change_service(service=619, subscriber=subs_id, status='active', params={122:'23001654321', 123:'88654321'});  
        rest.read_services(subscriber=subs_id)[0];  
        rest.read_services(subscriber=subs_id, service=619)[0];  
                                                      