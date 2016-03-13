# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.extensions.trackapps.translation.cs
   :platform: Unix
   :synopsis: Czech language translation for TrackApps extension
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""
language = {
  'name' : 'Čeština',
  'ISO-639-1' : 'cs'
} 


msg = { 
    'track_connecting'     : ["Připojuji se ns server s parametry: {0}"],
    'trakc_connected'      : ["Spojení se serverem bylo úspěšné"],
    'track_missing_cookie' : ["V odpovědi se nevrátilo cookie"],
    'track_missing_token'  : ["V odpovědi se nevrátil token"],
    'track_error'          : ["Nastala chyba HTTP status:'{0}', chyba: {1}"],
    'track_disconnecting'  : ["Ukončuji spojení se serverem"],
    'track_disconnected'   : ["Spojení se serverem bylo ukončeno"],
    'track_reading'        : ["Čtu záznamy s parametry: {0}"],
    'track_read'           : ["Přečteno záznamů: '{0}'"],
    'track_creating'       : ["Vytvářím záznam entita:'{0}', parametry: {1}"],
    'track_created'        : ["Záznam s id:'{0}' vytvořen"],
    'track_updating'       : ["Měním záznam entita:'{0}', id:'{1}', parametry: {2}"],
    'track_updated'        : ["Záznam s id:'{0}' změněn"],
    'track_deleting'       : ["Mažu záznam entita:'{0}', id:'{1}'"],
    'track_deleted'        : ["Záznam s id:'{0}' smazán"],
    'trac_unknown_record'  : ["Neexistující záznam s id:'{0}'"]        
}