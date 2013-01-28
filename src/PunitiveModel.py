"""Clients only keep the current list of active effects."""

import datetime
from Signals import SignalObject, Signal

from DatabaseManager import Session

from BaseTables import PunitiveEffect

class PunitiveModel(SignalObject):

    update = Signal
    remove = Signal

    def __init__(self):
        SignalObject.__init__(self)
        
        self.effect_list = ""
        self.effect_list_dirty = True
        
    def create_effect(self, server, effect_type, target_id, target_name, target_ip, target_mask, 
                      master_id, master_name, master_ip, expiry_time, reason):
        """Create an entry for a new specified punitive effect."""
        with Session() as session:
            effect = PunitiveEffect(effect_type, 
                                    target_id, 
                                    target_ip, 
                                    target_mask, 
                                    target_name, 
                                    master_id, 
                                    master_ip, 
                                    master_name, 
                                    expiry_time, 
                                    reason)
            
            session.add(effect)
            
            session.commit()
            
            self.effect_list_dirty = True
            self.update.emit(effect.id, effect_type, target_ip, target_mask, reason)
        
    def remove_effect(self, effect_id):
        if PunitiveEffect.set_expired(effect_id):
            self.effect_list_dirty = True
            self.remove.emit(effect_id)
        
    def get_effect_list(self):
        if self.effect_list_dirty:
            effect_list_list = []
            
            with Session() as session:
                punitive_effect_query = session.query(PunitiveEffect.id, PunitiveEffect.effect_type, PunitiveEffect.expired, PunitiveEffect.target_ip, PunitiveEffect.target_mask, PunitiveEffect.reason)
                rows = punitive_effect_query.filter(PunitiveEffect.expired==False).all()
            
                for effect_id, effect_type, expired, target_ip, target_mask, reason in rows:
                    effect_val = "effectupdate %ld %s %ld %ld %s\n" % (effect_id, effect_type, target_ip, target_mask, reason)
                    effect_list_list.append(effect_val)
            
            self.effect_list = "".join(effect_list_list)
            self.effect_list_dirty = False
        
        return self.effect_list
    
    def refresh(self):
            
        with Session() as session:
            # Look for those effects which have expired and send out remove signals.
            punitive_effect_query = session.query(PunitiveEffect)
            punitive_effect_query = PunitiveEffect.query_expired(punitive_effect_query)
            expired_punitive_effects = punitive_effect_query.all()
            
            for punitive_effect in expired_punitive_effects:
                punitive_effect.expired = True
                self.remove.emit(punitive_effect.id)
                
            # Look for those effects which have been updated and send out update signals
            updated_punitive_effects = session.query(PunitiveEffect).filter(PunitiveEffect.updated).all()
            
            for punitive_effect in updated_punitive_effects:
                punitive_effect.updated = False
                if punitive_effect.expired:
                    self.remove.emit(punitive_effect.id)
                else:
                    self.update.emit(punitive_effect.id, punitive_effect.effect_type, punitive_effect.target_ip, punitive_effect.target_mask, punitive_effect.reason)
                
            session.commit()
