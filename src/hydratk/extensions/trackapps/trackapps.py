# -*- coding: utf-8 -*-
"""This code is part of TrackApps extension

.. module:: trackapps.trackapps
   :platform: Unix
   :synopsis: Extension with interface to bugtracking and test management systems
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.core import extension
from hydratk.lib.console.commandlinetool import CommandlineTool
from os import path

apps = {
  'qc'       : 'qc',
  'bugzilla' : 'bugzilla',
  'mantis'   : 'mantis',
  'trac'     : 'trac',
  'jira'     : 'jira',
  'testlink' : 'testlink'
}

class Extension(extension.Extension):
    
    def _init_extension(self):
        
        self._ext_id   = 'trackapps'
        self._ext_name = 'TrackApps'
        self._ext_version = '0.1.0'
        self._ext_author = 'Petr Rašek <bowman@hydratk.org>'
        self._ext_year = '2016'  
        
    def _register_actions(self):
        
        self._mh.match_cli_command('track')
         
        hook = [
                {'command' : 'track', 'callback' : self.handle_track}
               ]  
        self._mh.register_command_hook(hook)  
        
        self._mh.match_long_option('app', True)
        self._mh.match_long_option('action', True)  
        self._mh.match_long_option('type', True)  
        self._mh.match_long_option('input', True)   
        self._mh.match_long_option('output', True)    
        self._mh.match_long_option('url', True) 
        self._mh.match_long_option('user', True) 
        self._mh.match_long_option('passw', True)
        self._mh.match_long_option('domain', True)
        self._mh.match_long_option('project', True)
        self._mh.match_long_option('id', True)
        self._mh.match_long_option('fields', True)
        self._mh.match_long_option('query', True)
        self._mh.match_long_option('order-by', True)
        self._mh.match_long_option('limit', True)
        self._mh.match_long_option('offset', True)
        self._mh.match_long_option('page', True)
        self._mh.match_long_option('per-page', True)
        self._mh.match_long_option('params', True)
        self._mh.match_long_option('qc-path', True)
    
    def init_client(self, app, *args, **kwargs):
        """Client factory method
        
        Args:            
            app (str): application, qc|bugzilla|mantis|trac|jira|testlink
            args (args): arguments 
            kwargs (kwargs): key value arguments
           
        Returns:
            obj: Client
       
        Raises:
            error: ValueError
                
        """       

        self._app = app.lower()        
        if (apps.has_key(self._app)):
            
            client = None     
            lib_call = 'from hydratk.extensions.trackapps.' + apps[app] + ' import Client; client = Client(*args, **kwargs)'                                             
            exec lib_call
                        
            return client

        else:
            raise ValueError('Unknown application:{0}'.format(app))
            return None  
        
    def handle_track(self):
        """Method handles command track
                
        """             
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_received_cmd', 'track'), self._mh.fromhere()) 

        app = CommandlineTool.get_input_option('--app')
        action = CommandlineTool.get_input_option('--action')
        
        if (not app):
            print ('Missing option app')            
        elif (not apps.has_key(app.lower())):
            print ('Application not in qc|bugzilla|mantis|trac|jira|testlink')                         
        elif (not action):
            print ('Missing option action')             
        elif (action not in ['read', 'create', 'update', 'delete']):
            print ('Action not in read|create|update|delete')   
        elif (action == 'delete' and app.lower() not in ['qc', 'mantis', 'trac']):
            print ('Application {0} doesn\'t support {1}'.format(app, action))            
        else:
            
            self._client = self.init_client(app)  
            self._cfg = self._mh.cfg['Extensions']['TrackApps'][self._app] 
            
            url = CommandlineTool.get_input_option('--url')                                   
            if (not url):
                if (self._cfg.has_key('url') and self._cfg['url'] != None):
                    url = self._cfg['url']
                else:
                    print ('Enter url') 
                    url = raw_input(":")
            
            user = CommandlineTool.get_input_option('--user')      
            if (not user):
                if (self._cfg.has_key('user') and self._cfg['user'] != None):
                    user = self._cfg['user']
                else:
                    print ('Enter username') 
                    user = raw_input(":") 
              
            passw = CommandlineTool.get_input_option('--passw')         
            if (not passw):
                if (self._cfg.has_key('passw') and self._cfg['passw'] != None):
                    passw = self._cfg['passw']
                else:
                    print ('Enter password') 
                    passw = raw_input(":")      
                    
            domain = CommandlineTool.get_input_option('--domain')         
            if (not domain and self._app == 'qc'):
                if (self._cfg.has_key('domain') and self._cfg['domain'] != None):
                    domain = self._cfg['domain']
                else:
                    print ('Enter domain') 
                    domain = raw_input(":")   
                    
            project = CommandlineTool.get_input_option('--project')         
            if (not project and self._app in ['qc', 'mantis', 'trac', 'jira']):
                if (self._cfg.has_key('project') and self._cfg['project'] != None):
                    project = self._cfg['project']
                else:
                    print ('Enter project') 
                    project = raw_input(":") 
                    
            self._entity = CommandlineTool.get_input_option('--type')
            if (not self._entity):
                self._entity = 'defect'
            if (self._entity not in ['defect', 'test-folder', 'test', 'test-set-folder', 'test-set', 'test-instance']):
                print ('Type not in defect|test-folder|test|test-set-folder|test-set|test-instance')
                return                                                                          
            
            if (self._app == 'qc'):    
                res = self._client.connect(url, user, passw, domain, project)
            elif (self._app == 'bugzilla'):
                res = self._client.connect(url, user, passw)
            elif (self._app in ['mantis', 'trac', 'jira']):
                res = self._client.connect(url, user, passw, project)
                
            if (not res):
                print ('Connection error')
                return 
            
            if (action == 'read'):
                self.read()
            elif (action == 'create'):
                self.create()
            elif (action == 'update'):
                self.update()
            elif (action == 'delete'):
                self.delete()
            
            if (self._app in ['qc', 'bugzilla', 'jira']):
                self._client.disconnect()  
            
    def read(self):
        """Method handles read action
                
        """            
        
        id = CommandlineTool.get_input_option('--id')
        if (not id):
            id = None
            
        fields = CommandlineTool.get_input_option('--fields')
        if (not fields):
            fields = None
        
        query = CommandlineTool.get_input_option('--query')
        if (not query):
            query = None
                  
        order_by_in = CommandlineTool.get_input_option('--order-by')
        if (order_by_in != False):           
            order_by = {}  
            order_by_in = order_by_in.split(',')
            for param in order_by_in:
                rec = param.split(':')
                key = rec[0]
                if (self._client.mapping.has_key(key)):
                    key = self._client.mapping[key]
                order_by[key] = rec[1]
        else:
            order_by = None                     
        
        limit = CommandlineTool.get_input_option('--limit')
        if (not limit):
            limit = None
        
        offset = CommandlineTool.get_input_option('--offset')
        if (not offset):
            offset = None   
            
        page = CommandlineTool.get_input_option('--page')
        if (not page):
            page = -1  
            
        per_page = CommandlineTool.get_input_option('--per-page')
        if (not per_page):
            per_page = -1                                                
        
        if (self._app == 'qc'):
            if (self._entity in ['test-folder', 'test-set-folder']):
                qc_path = CommandlineTool.get_input_option('--qc-path')
                if (not qc_path):
                    print ('Enter qc path') 
                    qc_path = raw_input(":")
                res, records = self._client.read_test_folder(qc_path, self._entity)
            elif (self._entity == 'test-set'):
                if (not id):
                    print ('Enter test set id') 
                    id = raw_input(":")
                res, records = self._client.read_test_set(int(id)) 
            else:
                res, records = self._client.read(id, self._entity, fields, query, order_by, limit, offset)   
                    
        elif (self._app == 'bugzilla'):                
            res, records = self._client.read(id, fields, query, limit, offset)
        elif (self._app == 'mantis'):
            res, records = self._client.read(id, fields, page, per_page)
        elif (self._app == 'trac'):
            res, records = self._client.read(id, fields, query)
        elif (self._app == 'jira'):
            res, records = self._client.read(id, fields, query, limit, offset)        
            
        if (res):
            output = CommandlineTool.get_input_option('--output')
            if (not output):
                print records
            else:
                with (open(output, 'w')) as f:
                    f.write(str(records))
        else:
            print ('Read error')  
            
       
    def create(self):
        """Method handles create action
                
        """              
        
        if (self._app == 'qc'):
            params = {}
            if (self._client._default_values.has_key(self._entity)):
                params = self._client._default_values[self._entity]
        else:
            params = self._client.default_values
                  
        params_in = CommandlineTool.get_input_option('--params')
        if (params_in != False):           
            params_in = params_in.split(',')
            for param in params_in:
                rec = param.split(':')
                key = rec[0]
                if (self._client.mapping.has_key(key)):
                    key = self._client.mapping[key]
                params[key] = rec[1]
                
        input = CommandlineTool.get_input_option('--input')
        if (input != False and path.exists(input)):      
            with open(input, 'r') as f:                                         
                params['description'] = f.read()        
                
        if (self._cfg.has_key('required_fields') and self._cfg['required_fields'] != None):
            if (self._app == 'qc'):
                if (self._cfg['required_fields'].has_key(self._entity) and 
                    self._cfg['required_fields'][self._entity] != None):
                    fields = self._cfg['required_fields'][self._entity].split(',') 
                else:
                    fields = []
            else:
                fields = self._cfg['required_fields'].split(',')
            
            lov = {}
            if (self._cfg.has_key('lov') and self._cfg['lov'] != None):    
                if (self._app == 'qc'):
                    if (self._cfg['lov'].has_key(self._entity) and 
                        self._cfg['lov'][self._entity] != None):
                        lov = self._cfg['lov'][self._entity]
                else:
                    lov = self._cfg['lov']
                    
                if (len(lov) > 0):
                    for key, value in lov.items():
                        lov[key] = value.split(',')                
                            
            for field in fields:
                                
                field_remap = field
                if (self._cfg.has_key('mapping') and self._cfg['mapping'] != None):
                    mapping = self._cfg['mapping']
                    if (self._app == 'qc'):
                        if (mapping.has_key(self._entity) and mapping[self._entity] != None
                            and field in mapping[self._entity].values()):
                            field_remap = mapping[self._entity].keys()[mapping[self._entity].values().index(field)]
                    elif (field in mapping.values()):
                        field_remap = mapping.keys()[mapping.values().index(field)]
                
                if (not params.has_key(field)):
                    print ('Enter required field: {0}'.format(field_remap)) 
                    
                    if (not lov.has_key(field)):                        
                        value = raw_input(":")
                        params[field] = value
                        
                    else:
                        prompt = ''          
                        values = lov[field]              
                        cnt = len(values)
                        for i in xrange(0, cnt):
                            prompt += '{0} - {1}\n'.format(i+1, values[i])
                            
                        valid = False
                        while (not valid):
                            try:
                                idx = int(raw_input('{0}'.format(prompt))) - 1        
                            except ValueError:
                                idx = -1
                                
                            if (idx >= 0 and idx < cnt):
                                valid = True
                            else:
                                print ('Wrong choice, enter required field: {0}'.format(field_remap))
                                
                        params[field] = values[idx]
        
        if (self._app == 'qc'): 
            if (self._entity in ('defect', 'test-instance')):           
                id = self._client.create(self._entity, params)
            else:
                qc_path = CommandlineTool.get_input_option('--qc-path')
                if (not qc_path):
                    print ('Enter qc path') 
                    qc_path = raw_input(":")
                if (self._entity == 'test'):
                    id = self._client.create_test(qc_path, params)
                elif (self._entity == 'test-set'):
                    id = self._client.create_test_set(qc_path, params)
                else:
                    folders = qc_path.split('/')
                    id = self._client.create_test_folder('/'.join(folders[:-1]), folders[-1], self._entity)
                    
        else:
            id = self._client.create(params)
        if (id != None):
            print ('Record {0} created'.format(id))
        else:
            print ('Create error')
    
    def update(self):
        """Method handles update action
                
        """              
        
        id = CommandlineTool.get_input_option('--id')
        if (not id):
            print ('Enter id') 
            id = raw_input(":")        
        
        params_in = CommandlineTool.get_input_option('--params')
        if (not params_in):
            params = {}
        else:            
            params_in = params_in.split(',')
            params = {}
            for param in params_in:
                rec = param.split(':')
                params[rec[0]] = rec[1]
                
        input = CommandlineTool.get_input_option('--input')
        if (input != False and path.exists(input)):      
            with open(input, 'r') as f:                                         
                params['description'] = f.read()                   
        
        if (self._app == 'qc'):
            res = self._client.update(id, self._entity, params)
        else:            
            res = self._client.update(id, params)
        if (res):
            print ('Record {0} updated'.format(id))
        else:
            print ('Update error')        
    
    def delete(self):
        """Method handles delete action
                
        """              
        
        id = CommandlineTool.get_input_option('--id')
        if (not id):
            print ('Enter id') 
            id = raw_input(":")         
        
        if (self._app == 'qc'):
            res = self._client.delete(id, self._entity)
        else:            
            res = self._client.delete(id)
        if (res):
            print ('Record {0} deleted'.format(id))
        else:
            print ('Delete error')                                                                                                 