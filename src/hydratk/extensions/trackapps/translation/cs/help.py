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
  'type'     : { '[{h}--type defect|test-folder|test|test-set-folder|test-set|test-instance|test-suite|test-plan|build{e}]' : { 'description' : 'typ entity, default defect, podporováno pro akce: read|create|update|delete, aplikace: qc|testlink', 'commands' : ('track')}},
  'input'    : { '[{h}--input <soubor>{e}]' : { 'description' : 'jméno souboru, obsah se zapíše do description tiketu, podporováno pro akce: create|update', 'commands' : ('track')}},
  'output'   : { '[{h}--output <soubor>{e}]' : { 'description' : 'jméno souboru, zápis výstupu akce, podporováno pro akci: read', 'commands' : ('track')}},
  'url'      : { '[{h}--url <url>{e}]' : { 'description' : 'url, konfigurovatelné', 'commands' : ('track')}},
  'user'     : { '[{h}--user <uživatel>{e}]' : { 'description' : 'uživatelské jméno, konfigurovatelné', 'commands' : ('track')}},
  'passw'    : { '[{h}--passw <heslo>{e}]' : { 'description' : 'heslo, konfigurovatelné', 'commands' : ('track')}},
  'dev-key'  : { '[{h}--dev-key <klíč>{e}]' : { 'description' : 'klíč vývojáře, konfigurovatelné, podporováno pro aplikaci: testlink', 'commands' : ('track')}},
  'domain'   : { '[{h}--domain <doména>{e}]' : { 'description' : 'doména, konfigurovatelné, podporováno pro aplikaci: qc', 'commands' : ('track')}},
  'project'  : { '[{h}--project <projekt>{e}]' : { 'description' : 'projekt, konfigurovatelné, podporováno pro aplikace: qc|mantis|trac|jira|testlink', 'commands' : ('track')}},  
  'id'       : { '[{h}--id <číslo>{e}]' : { 'description' : 'id záznamu, podporováno pro akce: read|update|delete', 'commands' : ('track')}},
  'fields'   : { '[{h}--fields <seznam>{e}]' : { 'description' : 'požadovaná pole, jméno1,jméno2,... , podporováno pro akci: read', 'commands' : ('track')}},
  'query'    : { '[{h}--query <výraz>{e}]' : { 'description' : 'dotaz, podporováno pro akci: read, aplikace: qc|bugzilla|trac|jira', 'commands' : ('track')}},
  'order-by' : { '[{h}--order-by <výraz>{e}]' : { 'description' : 'řazení záznamů, jméno1:směr,jméno2:směr,... , směr asc|desc, podporováno pro akci: read, aplikaci: qc', 'commands' : ('track')}},
  'limit'    : { '[{h}--limit <číslo>{e}]' : { 'description' : 'limit, podporováno pro akci: read, aplikace: qz|bugzilla|jira', 'commands' : ('track')}},
  'offset'   : { '[{h}--offset <číslo>{e}]' : { 'description' : 'offset, podporováno pro akci: read, aplikace: qc|bugzilla|jira', 'commands' : ('track')}},
  'page'     : { '[{h}--page <číslo>{e}]' : { 'description' : 'stránka záznamů, podporováno pro akci: read, aplikaci: mantis', 'commands' : ('track')}},
  'per-page' : { '[{h}--per-page <číslo>{e}]' : { 'description' : 'počet záznamů na stránku, podporováno pro akci read: aplikaci: mantis', 'commands' : ('track')}},  
  'params'   : { '[{h}--params <slovník>{e}]' : { 'description' : 'parametry záznamu, jméno1:hodnota,jméno2:hodnota, podporováno pro akce: create|update', 'commands' : ('track')}}, 
  'path'     : { '[{h}--path <cesta>{e}]' : { 'description' : 'adresářová cesta, dir1/dir2/... , podporováno pro případy: read/create folder|read/create test set|create test|read/create suite, aplikace: qc|testlink', 'commands' : ('track')}},
  'steps'    : { '[{h}--steps <seznam>{e}]' : { 'description' : 'kroky testu oddělené |, parametry kroku používají tvar slovníku, jméno1:hodnota,jméno2:hodnota,...|jméno1:hodnota,jméno2:hodnota,... , podporováno akci: create, aplikaci: testlink', 'commands' : ('track')}}                     
}