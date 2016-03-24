# -*- coding: utf-8 -*-
"""This code is part of TrackApps Extension

.. module:: trackapps.jira
   :platform: Unix
   :synopsis: Client for Jira
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

"""
Events:
-------
track_before_connect
track_after_connect
track_before_read
track_after_read
track_before_create
track_after_create
track_before_update
track_after_update

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
from hydratk.lib.network.rest.client import RESTClient
from jsonlib2 import write

config = {
  'session' : '/rest/auth/1/session',
  'search'  : '/rest/api/2/search',
  'issue'   : '/rest/api/2/issue'
}

class Client():
    
    _mh = None
    _client = None
    _url = None
    _user = None
    _passw = None
    _project = None
    _cookie = None
    _mapping = {}
    _return_fields = None
    _default_values = {}
    
    def __init__(self):
        """Class constructor
           
        Called when the object is initialized   
                
        """  
        
        self._mh = MasterHead.get_head()
        self._client = RESTClient() 

        cfg = self._mh.cfg['Extensions']['TrackApps']['jira'] 
        if (cfg.has_key('mapping') and cfg['mapping'] != None):
            self._mapping = cfg['mapping'] 
        if (cfg.has_key('return_fields') and cfg['return_fields'] != None):
            self._return_fields = cfg['return_fields'].split(',') 
        if (cfg.has_key('default_values') and cfg['default_values'] != None):
            self._default_values = cfg['default_values']  
        if (cfg.has_key('url') and cfg['url'] != None):
            self._url = cfg['url']    
        if (cfg.has_key('user') and cfg['user'] != None):
            self._user = cfg['user']   
        if (cfg.has_key('passw') and cfg['passw'] != None):
            self._passw = cfg['passw']  
        if (cfg.has_key('project') and cfg['project'] != None):
            self._project = cfg['project']                    
    
    @property
    def client(self):
        """ client property getter """
        
        return self._client
    
    @property
    def url(self):
        """ url property getter """
        
        return self._url
    
    @property
    def user(self):
        """ user property getter """
        
        return self._user
    
    @property
    def passw(self):
        """ passw property getter """
        
        return self._passw 
    
    @property
    def project(self):
        """ project property getter """
        
        return self._project      
    
    @property
    def cookie(self):
        """ cookie property getter """
        
        return self._cookie  
    
    @property
    def mapping(self):
        """ mapping property getter """
        
        return self._mapping  
    
    @property
    def return_fields(self):
        """ return_fields property getter """
        
        return self._return_fields   
    
    @property
    def default_values(self):
        """ default_values property getter """
        
        return self._default_values         
    
    def connect(self, url=None, user=None, passw=None, project=None):
        """Method connects to Jira
        
        Args:    
           url (str): URL        
           user (str): username
           passw (str): password
           project (str): project
             
        Returns:
           bool: result
           
        Raises:
           event: track_before_connect
           event: track_after_connect
                
        """    
        
        message = 'url:{0}, user:{1}, passw:{2}, project:{3}'.format(url, user, passw, project)
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_connecting', message), self._mh.fromhere()) 
        
        if (url == None):
            url = self._url
        if (user == None):
            user = self._user
        if (passw == None):
            passw = self._passw    
        if (project == None):
            project = self._project        
        
        ev = event.Event('track_before_connect', url, user, passw, project)
        if (self._mh.fire_event(ev) > 0):
            url = ev.argv(0)
            user = ev.argv(1)
            passw = ev.argv(2)
            project = ev.argv(3)
            
        if (ev.will_run_default()):
            self._url = url
            self._user = user
            self._passw = passw
            self._project = project
            
            url = self._url + config['session']
            body = write({'username': self._user, 'password': self._passw})
            res, body = self._client.send_request(url, method='POST', headers={'Accept': 'application/json'}, 
                                                  body=body, content_type='json')
        
        result = False
        if (res == 200): 

            self._cookie = self._client.get_header('set-cookie')
            if (self._cookie != None):
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_connected'), self._mh.fromhere())            
                ev = event.Event('track_after_connect')
                self._mh.fire_event(ev)   
                result = True
            else:
                self._mh.dmsg('htk_on_error', self._mh._trn.msg('track_missing_cookie'), self._mh.fromhere())
        else:
            self._mh.dmsg('htk_on_error', self._mh._trn.msg('track_error', res, body), self._mh.fromhere())    
            
        return result  
    
    def disconnect(self):
        """Method disconnects from Jira
        
        Args:    
             
        Returns:
           bool: result
                
        """   
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_disconnecting'), self._mh.fromhere()) 
        
        url = self._url + config['session']
        res, body = self._client.send_request(url, method='DELETE', headers={'Cookie': self._cookie})
        
        result = False
        if (res == 200):
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_disconnected'), self._mh.fromhere())
            self._cookie = None
            result = True
        else:
            self._mh.dmsg('htk_on_error', self._mh._trn.msg('track_error', res, body), self._mh.fromhere())
            
        return result       
    
    def read(self, id=None, fields=None, query=None, limit=None, offset=None): 
        """Method reads records
        
        Args: 
           id (int): record id         
           fields (list): fields to be returned, default all
           query (str): record query
           limit (int): record count    
           offset (int): record offset
             
        Returns:
           tuple: result (bool), records (list of dictionary)
           
        Raises:
           event: track_before_read
           event: track_after_read
                
        """   
        
        message = 'id:{0}, fields:{1}, query:{2}, limit:{3}, offset:{4}'.format(
                   id, fields, query, limit, offset)
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_reading', message), self._mh.fromhere()) 
        
        if (fields == None and self._return_fields != None):
            fields = []
            for key in self._return_fields:
                if (key in self._mapping.values()):
                    key = self._mapping.keys()[self._mapping.values().index(key)] 
                fields.append(key)        
        
        ev = event.Event('track_before_read', id, fields, query, limit, offset)
        if (self._mh.fire_event(ev) > 0):
            id = ev.argv(0)
            fields = ev.argv(1)
            query = ev.argv(2)
            limit = ev.argv(3)
            offset = ev.argv(4)   
            
        if (ev.will_run_default()): 
            
            body = {}            
            if (id != None):
                body['jql'] = 'key={0}-{1}'.format(self._project, id)  
            else:
                body['jql'] = 'project=' + self._project          
            if (fields != None and len(fields) > 0):
                fields_new = []
                for field in fields:
                    if (self._mapping.has_key(field)):
                        fields_new.append(self._mapping[field])   
                    else:
                        fields_new.append(field)                 
                body['fields'] = fields_new           
            if (query != None):
                body['jql'] += 'and ' + query
            if (limit != None):
                body['maxResults'] = limit
            if (offset != None):
                body['startAt'] = offset
            body = write(body)
            
            url = self._url + config['search']
            headers = {'Cookie': self._cookie, 'Accept': 'application/json'}
            res, body = self._client.send_request(url, method='POST', headers=headers, 
                                                  body=body, content_type='json')                      
            result = False
            records = None
            if (res == 200):
                cnt = body['total']
                records = []
                for i in xrange(0, cnt):
                    record = {}
                    if (fields == None or 'id' in fields):
                        record['id'] = body['issues'][i]['key']
                    for key, value in body['issues'][i]['fields'].items():
                        if (key in self._mapping.values()):
                            key = self._mapping.keys()[self._mapping.values().index(key)]                     
                        if (fields == None or key in fields):
                            record[key] = value                                         
                    records.append(record)       
                            
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_read', cnt), self._mh.fromhere())            
                ev = event.Event('track_after_read')
                self._mh.fire_event(ev)   
                result = True   
            else:
                self._mh.dmsg('htk_on_error', self._mh._trn.msg('track_error', res, body), self._mh.fromhere())           
            
            return (result, records)     
        
    def create(self, params={}):  
        """Method creates record
        
        Args: 
           params (dict): record content, key - field name, value - field value
             
        Returns:
           int: record id
           
        Raises:
           event: track_before_create
           event: track_after_create
                
        """       
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_creating', 'issue', params), self._mh.fromhere())
        
        if (self._default_values != {}):
            for key, value in self._default_values.items():
                if (not params.has_key(key)):
                    params[key] = value         
        
        ev = event.Event('track_before_create', params)
        if (self._mh.fire_event(ev) > 0):
            params = ev.argv(0)  
            
        if (ev.will_run_default()): 
            
            root = {'fields': {}}
            for key, value in params.items():          
                if (self._mapping.has_key(key)):
                    key = self._mapping[key]
                root['fields'][key] = value   
            if (not root['fields'].has_key('project')):
                root['fields']['project'] = {'key': self._project}
            if (not root['fields'].has_key('issuetype')):
                root['fields']['issuetype'] = {'name': 'Bug'}                  
            body = write(root)
             
            url = self._url + config['issue']
            headers = {'Cookie': self._cookie, 'Accept': 'application/json'}
            res, body = self._client.send_request(url, method='POST', headers=headers,
                                                  body=body, content_type='json')
            
        id = None
        if (res in (200, 201)):
            id = int(body['key'].split('-')[1])
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_created', id), self._mh.fromhere())            
            ev = event.Event('track_after_create')
            self._mh.fire_event(ev) 
        else:
            self._mh.dmsg('htk_on_error', self._mh._trn.msg('track_error', res, body), self._mh.fromhere())            
        
        return id                 
    
    def update(self, id, params={}):  
        """Method updates record
        
        Args: 
           id (int): record id
           params (dict): record content, key - field name, value - field value
             
        Returns:
           bool: result
           
        Raises:
           event: track_before_update
           event: track_after_update
                
        """       
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_updating', 'issue', id, params), 
                      self._mh.fromhere())
        
        ev = event.Event('track_before_update', id, params)
        if (self._mh.fire_event(ev) > 0):
            id = ev.argv(0)
            params = ev.argv(1)  
            
        if (ev.will_run_default()): 
            
            root = {'fields': {}}
            for key, value in params.items():          
                if (self._mapping.has_key(key)):
                    key = self._mapping[key]
                root['fields'][key] = value                  
            body = write(root)
             
            url = self._url + config['issue'] + '/{0}-{1}'.format(self._project, id)
            headers = {'Cookie': self._cookie, 'Accept': 'application/json'}
            res, body = self._client.send_request(url, method='PUT', headers=headers,
                                                  body=body, content_type='json')
            
        result = False
        if (res in (200, 204)):
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_updated', id), self._mh.fromhere())            
            ev = event.Event('track_after_update')
            self._mh.fire_event(ev) 
            result = True
        else:
            self._mh.dmsg('htk_on_error', self._mh._trn.msg('track_error', res, body), self._mh.fromhere())            
        
        return result       