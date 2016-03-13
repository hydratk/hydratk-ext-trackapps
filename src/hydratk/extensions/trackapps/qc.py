# -*- coding: utf-8 -*-
"""This code is part of TrackApps extension

.. module:: trackapps.qc
   :platform: Unix
   :synopsis: Client for HP Quality Center
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
track_before_delete
track_after_delete

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
from hydratk.lib.network.rest.client import RESTClient
from lxml.etree import Element, SubElement, tostring

config = {
  'sign_in'  : '/authentication-point/authenticate',
  'sign_out' : '/authentication-point/logout',
  'rest'     : '/rest/domains/{0}/projects/{1}/{2}s/'
}

class Client():
    
    _mh = None
    _client = None
    _url = None
    _user = None
    _passw = None
    _domain = None
    _project = None
    _cookie = None
    _mapping = None
    
    def __init__(self):
        """Class constructor
           
        Called when the object is initialized   
                
        """  
        
        self._mh = MasterHead.get_head()
        self._client = RESTClient()   
        self._mapping = self._mh.cfg['Extensions']['TrackApps']['mapping']['qc'] 
        
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
    def domain(self):
        """ domain property getter """
        
        return self._domain
    
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
     
    def connect(self, url, user, passw, domain, project):
        """Method connects to QC
        
        Args:    
           url (str): URL        
           user (str): username
           passw (str): password
           domain (str): QC domain
           project (str): QC project
             
        Returns:
           bool: result
           
        Raises:
           event: track_before_connect
           event: track_after_connect
                
        """    
        
        message = 'url:{0}, user:{1}, passw:{2}, domain:{3}, project:{4}'.format(url, user, passw, domain, project)
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_connecting', message), self._mh.fromhere()) 
        
        ev = event.Event('track_before_connect', url, user, passw, domain, project)
        if (self._mh.fire_event(ev) > 0):
            url = ev.argv(0)
            user = ev.argv(1)
            passw = ev.argv(2)
            domain = ev.argv(3)
            project = ev.argv(4)
            
        if (ev.will_run_default()):
            self._url = url
            self._user = user
            self._passw = passw
            self._domain = domain
            self._project = project  
            
            url = self._url + config['sign_in']
            res, body = self._client.send_request(self._url, self._user, self._passw, 'POST')
        
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
            self._mh.dmsg('htk_on_error', self._mh._trn.msg('track_error', res, body.Title), self._mh.fromhere())    
        
        return result   
    
    def disconnect(self):
        """Method disconnects from QC
        
        Args:    
             
        Returns:
           bool: result
                
        """   
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_disconnecting'), self._mh.fromhere()) 
        
        url = self._url + config['sign_out']
        res, body = self._client.send_request(url, method='POST', headers={'Cookie': self._cookie})
        
        result = False
        if (res == 200):
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_disconnected'), self._mh.fromhere())
            self._cookie = None
            result = True
        else:
            self._mh.dmsg('htk_on_error', self._mh._trn.msg('track_error', res, body.Title), self._mh.fromhere())
            
        return result  
    
    def read(self, id=None, entity='defect', fields=None, query=None, order_by=None, limit=None, offset=None): 
        """Method reads records
        
        Args: 
           id (int): record id
           entity (str): entity type, defect           
           fields (list): fields to be returned, default all
           query (str): record query
           order_by (dict): record ordering, key - field, value - direction asc|desc 
           limit (int): record count    
           offset (int): record offset
             
        Returns:
           tuple: result (bool), records (list of dictionary)
           
        Raises:
           event: track_before_read
           event: track_after_read
                
        """   
        
        message = 'entity:{0}, id:{1}, fields:{2}, query:{3}, order_by:{4}, limit:{5}, offset:{6}'.format(
                   entity, id, fields, query, order_by, limit, offset)
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_reading', message), self._mh.fromhere()) 
        
        ev = event.Event('track_before_read', entity, id, fields, query, order_by, limit, offset)
        if (self._mh.fire_event(ev) > 0):
            entity = ev.argv(0)
            id = ev.argv(1)
            fields = ev.argv(2)
            query = ev.argv(3)
            order_by = ev.argv(4)
            limit = ev.argv(5)
            offset = ev.argv(6)   
            
        if (ev.will_run_default()): 
            
            params = {}
            if (fields != None and len(fields) > 0):
                param = ""
                for field in fields:
                    if (self._mapping.has_key(field)):
                        field = self._mapping[field]
                    param += field + ','
                params['fields'] = param[:-1]
            if (query != None):
                params['query'] = query
            if (id != None):
                params['query'] = '{ID[=%d]}' % id if (not params.has_key('query')) else params['query'] + '; {ID[=%d]}' % id
            if (order_by != None and len(order_by.keys()) > 0):
                param = ""
                for field, direction in order_by.items():
                    if (direction == 'asc'):
                        param += '+' + field + ','
                    elif (direction == 'desc'):
                        param += '-' + field + ','
                params['order-by'] = param[:-1]
            if (limit != None):
                params['limit'] = limit
            if (offset != None):
                params['offset'] = offset
            
            url = self._url + config['rest'].format(self._domain, self._project, entity)
            headers = {'Cookie': self._cookie}
            res, body = self._client.send_request(url, method='GET', headers=headers, params=params,
                                                  content_type='xml')                      
            
            result = False
            records = None
            if (res == 200):
                
                cnt = int(body.get('TotalResults'))
                records = []
                for i in xrange(0, cnt):
                    record = {}
                    for field in body.Entity[i].Fields.Field:
                        key = field.get('Name')
                        if (key in self._mapping.values()):
                            key = self._mapping.keys()[self._mapping.values().index(key)]
                        value = field.Value if (hasattr(field, 'Value')) else None
                        if (fields == None or key in fields):
                            record[key] = value 
                    records.append(record)       
                            
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_qc_read', cnt), self._mh.fromhere())            
                ev = event.Event('track_after_read')
                self._mh.fire_event(ev)   
                result = True   
            else:
                self._mh.dmsg('htk_on_error', self._mh._trn.msg('track_error', res, body.Title), self._mh.fromhere())           
            
            return (result, records)   
        
    def create(self, entity='defect', params={}):  
        """Method creates record
        
        Args: 
           entity (str): entity type, defect
           params (dict): record content, key - field name, value - field value
             
        Returns:
           int: record id
           
        Raises:
           event: track_before_create
           event: track_after_create
                
        """       
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_creating', entity, params), self._mh.fromhere())
        
        ev = event.Event('track_before_create', entity, params)
        if (self._mh.fire_event(ev) > 0):
            entity = ev.argv(0)
            params = ev.argv(1)  
            
        if (ev.will_run_default()): 
            
            root = Element('Entity')
            root.set('Type', entity)
            el_fields = SubElement(root, 'Fields')
            for key, value in params.items():
                elem = SubElement(el_fields, 'Field')            
                if (self._mapping.has_key(key)):
                    key = self._mapping[key]
                elem.set('Name', key)
                SubElement(elem, 'Value').text = value           
            body = tostring(root)
             
            url = self._url + config['rest'].format(self._domain, self._project, entity)
            headers = {'Cookie': self._cookie}           
            res, body = self._client.send_request(url, method='POST', headers=headers, body=body,
                                                  content_type='xml')
        id = None
        if (res in (200, 201)):
            id = int(body.xpath("//Entity/Fields/Field[@Name='id']/Value/text()")[0])
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_created', id), self._mh.fromhere())            
            ev = event.Event('track_after_create')
            self._mh.fire_event(ev) 
        else:
            self._mh.dmsg('htk_on_error', self._mh._trn.msg('track_error', res, body.Title), self._mh.fromhere())            
        
        return id    
    
    def update(self, id, entity='defect', params={}):
        """Method updates record
        
        Args: 
           id (int): entity id
           entity (str): entity type, defect           
           params (dict): record content, key - field name, value - field value 
             
        Returns:
           bool: result
           
        Raises:
           event: track_before_update
           event: track_after_update
                
        """          
      
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_updating', entity, id, params), self._mh.fromhere())
        
        ev = event.Event('track_before_update', entity, id, params)
        if (self._mh.fire_event(ev) > 0):
            entity = ev.argv(0)
            id = ev.argv(1)
            params = ev.argv(2)  
            
        if (ev.will_run_default()): 
            
            root = Element('Entity')
            root.set('Type', entity)
            el_fields = SubElement(root, 'Fields')
            for key, value in params.items():
                elem = SubElement(el_fields, 'Field')            
                if (self._mapping.has_key(key)):
                    key = self._mapping[key]
                elem.set('Name', key)
                SubElement(elem, 'Value').text = value           
            body = tostring(root)
             
            url = self._url + config['rest'].format(self._domain, self._project, entity) + str(id)
            headers = {'Cookie': self._cookie}           
            res, body = self._client.send_request(url, method='PUT', headers=headers, body=body,
                                                  content_type='xml')
        result = False
        if (res == 200):
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_updated', id), self._mh.fromhere())            
            ev = event.Event('track_after_update')
            self._mh.fire_event(ev) 
            result = True
        else:
            self._mh.dmsg('htk_on_error', self._mh._trn.msg('track_error', res, body.Title), self._mh.fromhere())            
        
        return result        
    
    def delete(self, id, entity='defect'):
        """Method deletes record
        
        Args: 
           id (int): entity id
           entity (str): entity type, defect           
             
        Returns:
           bool: result
           
        Raises:
           event: track_before_delete
           event: track_after_delete
                
        """         
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_deleting', entity, id), self._mh.fromhere())
        
        ev = event.Event('track_before_delete', entity, id)
        if (self._mh.fire_event(ev) > 0):
            entity = ev.argv(0)
            id = ev.argv(1)  
            
        if (ev.will_run_default()):         
             
            url = self._url + config['rest'].format(self._domain, self._project, entity) + str(id)
            headers = {'Cookie': self._cookie}           
            res, body = self._client.send_request(url, method='DELETE', headers=headers, content_type='xml')
            
        result = False
        if (res == 200):
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_deleted', id), self._mh.fromhere())            
            ev = event.Event('track_after_delete')
            self._mh.fire_event(ev) 
            result = True
        else:
            self._mh.dmsg('htk_on_error', self._mh._trn.msg('track_error', res, body.Title), self._mh.fromhere())            
        
        return result                                                                          