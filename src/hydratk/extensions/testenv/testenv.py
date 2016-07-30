# -*- coding: utf-8 -*-
"""Extension for test automation exercises

.. module:: testenv.testenv
   :platform: Unix
   :synopsis: Extension for test automation exercises
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.core import extension
from hydratk.extensions.testenv.web_server import Server
from os import path, remove
from sqlite3 import Error, connect

class Extension(extension.Extension):
    """Class Extension
    """
    
    def _init_extension(self):
        """Method initializes extension
        
        Args:
           none
        
        Returns:
           void
            
        """         
        
        self._ext_id   = 'testenv'
        self._ext_name = 'TestEnv'
        self._ext_version = '0.2.0'
        self._ext_author = 'Petr Rašek <bowman@hydratk.org>'
        self._ext_year = '2015-2016'  
        
    def _register_actions(self):
        """Method registers command hooks
        
        Args:
           none
        
        Returns:
           void
            
        """           
        
        if (self._mh.cli_cmdopt_profile == 'testenv'):
            self._register_standalone_actions()             
        else:
            self._register_htk_actions()    
            
    def _register_htk_actions(self):
        """Method registers command hooks
        
        Args:  
           none        
           
        Returns:
           void
           
        """ 
        
        self._mh.match_cli_command('te-install')        
        hook = [{'command' : 'te-install', 'callback' : self.install_db_fc }]        
        self._mh.register_command_hook(hook) 
        
        self._mh.match_cli_command('te-run')
        hook = [{'command' : 'te-run', 'callback' : self.start_fc }]  
        self._mh.register_command_hook(hook)                         
        
    def _register_standalone_actions(self):
        """Method registers command hooks for standalone mode
        
        Args:  
           none        
           
        Returns:
           void
           
        """ 
        
        option_profile = 'testenv'
        help_title = '{h}' + self._ext_name + ' v' + self._ext_version + '{e}'
        cp_string = '{u}' + "(c) "+ self._ext_year +" "+ self._ext_author  + '{e}'
        self._mh.set_cli_appl_title(help_title, cp_string)                
        
        self._mh.match_cli_command('install', option_profile)        
        hook = [{'command' : 'install', 'callback' : self.install_db_fc }]        
        self._mh.register_command_hook(hook) 
        
        self._mh.match_cli_command('run', option_profile)
        hook = [{'command' : 'run', 'callback' : self.start_fc }]  
        self._mh.register_command_hook(hook)  
        
        self._mh.match_cli_command('help', option_profile)   
        
        self._mh.match_cli_option(('c','config'), True, 'config', False, option_profile)
        self._mh.match_cli_option(('d','debug'), True, 'debug', False, option_profile)   
        self._mh.match_cli_option(('e','debug-channel'), True, 'debug-channel', False, option_profile)
        self._mh.match_cli_option(('l','language'), True, 'language', False, option_profile)
        self._mh.match_cli_option(('m','run-mode'), True, 'run-mode', False, option_profile)
        self._mh.match_cli_option(('f','force'), False, 'force', False, option_profile)
        self._mh.match_cli_option(('i','interactive'), False, 'interactive', False, option_profile)                                          
            
    def install_db_fc(self, ext_call=True): 
        """Method handles command te-install    
           
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
                    
        except Error as ex:
            self._mh.dmsg('htk_on_extension_error', 'error: {0}'.format(ex), self._mh.fromhere())
       
    def start_fc(self):
        """Method handles command te-run 
        
        Starts web server and installs database if not installed  
        
        Args:
           none
        
        Returns:
           void                  
                
        """         
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('te_received_cmd', 'te-start'), self._mh.fromhere())
        
        db_file = path.join(self._mh.cfg['Extensions']['TestEnv']['ext_dir'], self._mh.cfg['Extensions']['TestEnv']['db_file'])  
        if (not path.exists(db_file)): 
            self.install_db_fc(False)           
          
        server = Server()
        server._start()                                                                     