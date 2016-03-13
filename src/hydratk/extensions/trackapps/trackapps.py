# -*- coding: utf-8 -*-
"""This code is part of TrackApps extension

.. module:: trackapps.trackapps
   :platform: Unix
   :synopsis: Extension with interface to bugtracking and test management systems
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.core import extension

apps = {
  'QC'       : 'qc',
  'BUGZILLA' : 'bugzilla',
  'MANTIS'   : 'mantis',
  'TRAC'     : 'trac',
  'JIRA'     : 'jira',
  'TESTLINK' : 'testlink'
}

class Extension(extension.Extension):
    
    def _init_extension(self):
        
        self._ext_id   = 'trackapps'
        self._ext_name = 'TrackApps'
        self._ext_version = '0.1.0'
        self._ext_author = 'Petr Rašek <bowman@hydratk.org>'
        self._ext_year = '2016'  
        
    def _register_actions(self):
        pass 
    
    def client(self, app, *args, **kwargs):
        """Client factory method
        
    Args:            
        app (str): application, QC|Bugzilla|Mantis|Trac|Jira|TestLink
        args (args): arguments 
        kwargs (kwargs): key value arguments
           
    Returns:
        obj: Client
       
    Raises:
        error: ValueError
                
    """       

        app = app.upper()        
        if (apps.has_key(app)):
            
            client = None     
            lib_call = 'from hydratk.extensions.trackapp.' + apps[app] + ' import Client; client = Client(*args, **kwargs)'                                             
            exec lib_call
                        
            return client

        else:
            raise ValueError('Unknown application:{0}'.format(app))
            return None                                                     