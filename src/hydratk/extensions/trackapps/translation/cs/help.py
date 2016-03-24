# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.extensions.trackapps.translation.cs.help
   :platform: Unix
   :synopsis: Czech language translation for TrackAPps extension help generator
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""
language = {
  'name' : 'Čeština',
  'ISO-639-1' : 'cs'
} 

''' TrackApps Commands '''
help_cmd = {
  'track'  : 'spustit konzolové rozšíření trackapps'            
}

''' TrackApps Options '''
help_opt = { 
  'app'      : { '{h}--app qc|bugzilla|mantis|trac|testlink{e}' : { 'description' : 'aplikace', 'commands' : ('track')}},    
  'action'   : { '{h}--action read|create|update|delete{e}' : { 'description' : 'akce, delete podporováno pro aplikace: qc|mantis|trac', 'commands' : ('track')}},
  'type'     : { '[{h}--type defect|test|test-folder|test-set-folder|test-set|test-instance{e}]' : { 'description' : 'typ entity, default defect, podporováno pro akce: read|create|update|delete, aplikace: qc', 'commands' : ('track')}},
  'input'    : { '[{h}--input <soubor>{e}]' : { 'description' : 'jméno souboru, obsah se zapíše do description tiketu, podporováno pro akce: create|update', 'commands' : ('track')}},
  'output'   : { '[{h}--output <soubor>{e}]' : { 'description' : 'jméno souboru, zápis výstupu akce, podporováno pro akci: read', 'commands' : ('track')}},
  'url'      : { '[{h}--url <url>{e}]' : { 'description' : 'url, konfigurovatelné', 'commands' : ('track')}},
  'user'     : { '[{h}--user <uživatel>{e}]' : { 'description' : 'uživatelské jméno, konfigurovatelné', 'commands' : ('track')}},
  'passw'    : { '[{h}--passw <heslo>{e}]' : { 'description' : 'heslo, konfigurovatelné', 'commands' : ('track')}},
  'domain'   : { '[{h}--domain <doména>{e}]' : { 'description' : 'doména, konfigurovatelné, podporováno pro aplikaci: qc', 'commands' : ('track')}},
  'project'  : { '[{h}--project <projekt>{e}]' : { 'description' : 'projekt, konfigurovatelné, podporováno pro aplikace: qc|mantis|trac|jira', 'commands' : ('track')}},  
  'id'       : { '[{h}--id <číslo>{e}]' : { 'description' : 'id záznamu, podporováno pro akce: read|update|delete', 'commands' : ('track')}},
  'fields'   : { '[{h}--fields <seznam>{e}]' : { 'description' : 'požadovaná pole, jméno1,jméno2,... , podporováno pro akci: read', 'commands' : ('track')}},
  'query'    : { '[{h}--limit <výraz>{e}]' : { 'description' : 'dotaz, podporováno pro akci: read, aplikace: qc|bugzilla|trac|jira', 'commands' : ('track')}},
  'order-by' : { '[{h}--order-by <výraz>{e}]' : { 'description' : 'řazení záznamů, name1:direction,name2:direction,... , direction asc|desc, podporováno pro akci: read, aplikace: qc', 'commands' : ('track')}},
  'limit'    : { '[{h}--limit <číslo>{e}]' : { 'description' : 'limit, podporováno pro akci: read, aplikace: qz|bugzilla|jira', 'commands' : ('track')}},
  'offset'   : { '[{h}--offset <číslo>{e}]' : { 'description' : 'offset, podporováno pro akci: read, aplikace: qc|bugzilla|jira', 'commands' : ('track')}},
  'page'     : { '[{h}--page <číslo>{e}]' : { 'description' : 'stránka záznamů, podporováno pro akci: read, aplikaci: mantis', 'commands' : ('track')}},
  'per-page' : { '[{h}--per-page <číslo>{e}]' : { 'description' : 'počet záznamů na stránku, podporováno pro akci read: aplikaci: mantis', 'commands' : ('track')}},  
  'params'   : { '[{h}--params <slovník>{e}]' : { 'description' : 'parametry záznamu, jméno1:hodnota,jméno2:hodnota, podporováno pro akce: create|update', 'commands' : ('track')}}, 
  'qc-path'  : { '[{h}--qc-path <cesta>{e}]' : { 'description' : 'adresářová cesta v qc, dir1/dir2/... , podporováno pro případy: read/create folder|read/create test set|create test, aplikaci: qc', 'commands' : ('track')}}                    
}