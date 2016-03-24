# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.extensions.trackapps.translation.en.help
   :platform: Unix
   :synopsis: English language translation for TrackApps extension help generator
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""
language = {
  'name' : 'English',
  'ISO-639-1' : 'en'
} 

''' TrackApps Commands '''
help_cmd = {
  'track'  : 'start trackapps command line extension'            
}

''' TrackApps Options '''
help_opt = { 
  'app'      : { '{h}--app qc|bugzilla|mantis|trac|testlink{e}' : { 'description' : 'application', 'commands' : ('track')}},    
  'action'   : { '{h}--action read|create|update|delete{e}' : { 'description' : 'action, delete supported for apps: qc|mantis|trac', 'commands' : ('track')}},
  'type'     : { '[{h}--type defect|test|test-folder|test-set-folder|test-set|test-instance{e}]' : { 'description' : 'entity type, default defect, supported for actions: read|create|update|delete, app: qc', 'commands' : ('track')}},
  'input'    : { '[{h}--input <filename>{e}]' : { 'description' : 'filename, content is written to ticket description, supported for actions: create|update', 'commands' : ('track')}},
  'output'   : { '[{h}--output <filename>{e}]' : { 'description' : 'filename, writes action output, supported for action: read', 'commands' : ('track')}},
  'url'      : { '[{h}--url <url>{e}]' : { 'description' : 'url, configurable', 'commands' : ('track')}},
  'user'     : { '[{h}--user <username>{e}]' : { 'description' : 'username, configurable', 'commands' : ('track')}},
  'passw'    : { '[{h}--passw <password>{e}]' : { 'description' : 'password, configurable', 'commands' : ('track')}},
  'domain'   : { '[{h}--domain <domain>{e}]' : { 'description' : 'domain, configurable, supported for app: qc', 'commands' : ('track')}},
  'project'  : { '[{h}--project <project>{e}]' : { 'description' : 'project, configurable, supported for apps: qc|mantis|trac|jira', 'commands' : ('track')}},
  'id'       : { '[{h}--id <num>{e}]' : { 'description' : 'record id, supported for actions: read|update|delete', 'commands' : ('track')}},
  'fields'   : { '[{h}--fields <list>{e}]' : { 'description' : 'requested fields, name1,name2,... , supported for action: read', 'commands' : ('track')}},
  'query'    : { '[{h}--query <expression>{e}]' : { 'description' : 'query, supported for action: read, apps: qc|bugzilla|trac|jira', 'commands' : ('track')}},
  'order-by' : { '[{h}--order-by <expression>{e}]' : { 'description' : 'record ordering, name1:direction,name2:direction,... , direction asc|desc, supported for action: read, app: qc', 'commands' : ('track')}},
  'limit'    : { '[{h}--limit <num>{e}]' : { 'description' : 'limit, supported for action: read, apps: qc|bugzilla|jira', 'commands' : ('track')}},
  'offset'   : { '[{h}--offset <num>{e}]' : { 'description' : 'offset, supported for action: read, apps: qc|bugzilla|jira', 'commands' : ('track')}},
  'page'     : { '[{h}--page <num>{e}]' : { 'description' : 'record page, supported for action: read, app: mantis', 'commands' : ('track')}},
  'per-page' : { '[{h}--per-page <num>{e}]' : { 'description' : 'records per page, supported for action: read, app: mantis', 'commands' : ('track')}},
  'params'   : { '[{h}--params <dict>{e}]' : { 'description' : 'record parameters, name1:value,name2:value,... , supported for actions: create|update', 'commands' : ('track')}},
  'qc-path'  : { '[{h}--qc-path <path>{e}]' : { 'description' : 'directory path in qc, dir1/dir2/... , supported for use cases: read/create folder|read/create test set|create test, app: qc', 'commands' : ('track')}}                                          
}