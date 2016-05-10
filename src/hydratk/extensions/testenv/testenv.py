# -*- coding: utf-8 -*-
"""This code is part of TestEnv extension

.. module:: testenv.testenv
   :platform: Unix
   :synopsis: Extension for test automation exercises
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.core import extension
from hydratk.extensions.testenv.application import web_server
from os import path, remove
from sqlite3 import Error, connect

class Extension(extension.Extension):
    
    def _init_extension(self):
        """Method initializes extension
        
        Args:
        
        Returns:
           void
            
        """         
        
        self._ext_id   = 'testenv'
        self._ext_name = 'TestEnv'
        self._ext_version = '0.1.0'
        self._ext_author = 'Petr Rašek <bowman@hydratk.org>'
        self._ext_year = '2015'  
        
    def _register_actions(self):
        """Method registers command hooks
        
        Commands - te-install-db, te-start
        
        Args:
        
        Returns:
           void
            
        """           
        
        self._mh.match_cli_command('te-install-db')        
        hook = [{'command' : 'te-install-db', 'callback' : self.install_db_fc }]        
        self._mh.register_command_hook(hook) 
        
        self._mh.match_cli_command('te-start')
        hook = [{'command' : 'te-start', 'callback' : self.start_fc }]  
        self._mh.register_command_hook(hook)       
            
    def install_db_fc(self, ext_call=True): 
        """Method handles command te-install-db    
           
        Args:
           ext_call (bool): external method call   
           
        Returns:
           void          
                
        """         
            
        try:    
            
            if (ext_call):
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_received_cmd', 'te-install-db'), self._mh.fromhere())
            
            ext_dir = self._mh.cfg['Extensions']['TestEnv']['ext_dir']         
            db_file = path.join(ext_dir, self._mh.cfg['Extensions']['TestEnv']['db_file'])   
            if (path.exists(db_file)):        
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_delete_db', db_file), self._mh.fromhere())
                remove(db_file)
                                
            install_file = path.join(ext_dir, 'install_db.sql')
            if (path.exists(install_file)):
            
                with open(install_file, 'r') as file:
                    script = file.read()
            
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_create_db', db_file), self._mh.fromhere()) 
                with connect(db_file) as conn:
                    self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_install_db', install_file), self._mh.fromhere())
                    cur = conn.cursor()
                    cur.executescript(script)
                    conn.commit()
                    self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_db_installed'), self._mh.fromhere()) 
            else:
                self._mh.dmsg('htk_on_extension_error', self._mh._trn.msg('te_unknown_install'), self._mh.fromhere())
                    
        except Error, ex:
            self._mh.dmsg('htk_on_extension_error', 'error: {0}'.format(ex), self._mh.fromhere())
       
    def start_fc(self):
        """Method handles command te-start 
        
        Starts web server and installs database if not installed  
        
        Args:
        
        Returns:
           void                  
                
        """         
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_received_cmd', 'te-start'), self._mh.fromhere())
        
        db_file = path.join(self._mh.cfg['Extensions']['TestEnv']['ext_dir'], self._mh.cfg['Extensions']['TestEnv']['db_file'])  
        if (not path.exists(db_file)): 
            self.install_db_fc(False)           
          
        server = web_server.Server()
        server._start()                                                                     