# -*- coding: utf-8 -*-
"""This code is a part of Hydra Toolkit

.. module:: hydratk.extensions.testenv
   :platform: Unix
   :synopsis: TestEnv extension for test automation exercises
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.core import extension
import hydratk.extensions.testenv.application.web_server as web_server
import os
import sqlite3

class Extension(extension.Extension):
    
    def _init_extension(self):
        
        self._ext_id   = 'testenv'
        self._ext_name = 'TestEnv'
        self._ext_version = '0.1.0'
        self._ext_author = 'Petr Rašek <bowman@hydratk.org>'
        self._ext_year = '2015'  
        
    def _register_actions(self):
        
        self._mh.match_command('te-install-db')        
        hook = [{'command' : 'te-install-db', 'callback' : self.install_db_fc }]        
        self._mh.register_command_hook(hook) 
        
        self._mh.match_command('te-start')
        hook = [{'command' : 'te-start', 'callback' : self.start_fc }]  
        self._mh.register_command_hook(hook)       
            
    def install_db_fc(self, ext_call=True): 
            
        try:    
            
            if (ext_call):
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_received_cmd', 'te-install-db'), self._mh.fromhere())
                    
            db_file = self._mh.cfg['Extensions']['TestEnv']['db_file']   
            if (os.path.exists(db_file)):        
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_delete_db', db_file), self._mh.fromhere())
                os.remove(db_file)
                                
            install_file = os.path.join(self._mh.cfg['System']['Extending']['extensions_dir'], 'testenv/application/install_db.sql')
            if (os.path.exists(install_file)):
            
                with open(install_file, 'r') as file:
                    script = file.read()
            
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_create_db', db_file), self._mh.fromhere()) 
                with sqlite3.connect(db_file) as conn:
                    self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_install_db', install_file), self._mh.fromhere())
                    cur = conn.cursor()
                    cur.executescript(script)
                    conn.commit()
                    self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_installed'), self._mh.fromhere()) 
            else:
                self._mh.dmsg('htk_on_extension_error', self._mh._trn.msg('te_unknown_install'), self._mh.fromhere())
                    
        except sqlite3.Error, ex:
            self._mh.dmsg('htk_on_extension_error', 'error: {0}'.format(ex), self._mh.fromhere())
       
    def start_fc(self):
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_received_cmd', 'te-start'), self._mh.fromhere())
        
        db_file = self._mh.cfg['Extensions']['TestEnv']['db_file']  
        if (not os.path.exists(db_file)): 
            self.install_db_fc(False)           
          
        server = web_server.Server()
        server._start()                                                                     