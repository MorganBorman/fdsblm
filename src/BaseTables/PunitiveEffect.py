from Common import *
from TableNames import table_names

import datetime, time

class PunitiveEffect(database_manager.Base):
    __tablename__ = table_names['PunitiveEffect']
    id = Column(BigInteger, Sequence(__tablename__+'_id_seq'), primary_key=True)
    effect_type     = Column(String(16),    nullable=False,     index=True)
    
    target_id       = Column(Integer,       nullable=True)
    target_ip       = Column(BigInteger,    nullable=False,     index=True)
    target_mask     = Column(BigInteger,    nullable=False,     index=True)
    target_name     = Column(String(16),    nullable=False)
    
    master_id       = Column(Integer,       nullable=True)
    master_ip       = Column(BigInteger,    nullable=True)
    master_name     = Column(String(16),    nullable=False)
    
    created_time    = Column(DateTime,      nullable=False)
    modified_time   = Column(DateTime,      nullable=False)
    expiry_type     = Column(Integer,       nullable=False)
    expiry_time     = Column(DateTime,      nullable=True)
    
    expiry_types = enum(NEVEREXPIRES=-1, EXPIRYDATE=0)
    
    expired         = Column(Boolean)
    updated         = Column(Boolean)
    
    reason          = Column(String(128))
    
    def __init__(self, effect_type, target_id, target_ip, target_mask, target_name, 
                 master_id, master_ip, master_name, expiry_time, reason):
        
        self.effect_type = effect_type
        
        self.target_id = target_id
        self.target_ip = target_ip
        self.target_mask = target_mask
        self.target_name = target_name
        
        self.master_id = master_id
        self.master_ip = master_ip
        self.master_name = master_name
        
        self.created_time = datetime.datetime.now()
        self.modified_time = datetime.datetime.now()
        
        if expiry_time == 0:
            self.expiry_time = None
            self.expiry_type = self.expiry_types.NEVEREXPIRES
        else:
            self.expiry_time = datetime.datetime.fromtimestamp(time.time()+expiry_time)
            self.expiry_type = self.expiry_types.EXPIRYDATE
            
        self.expired = False
        self.updated = False
        
        self.reason = reason

    @staticmethod
    def query_expired(query):
        query = query.filter(PunitiveEffect.expired==False)
        return query.filter(and_(PunitiveEffect.expiry_type==PunitiveEffect.expiry_types.EXPIRYDATE, 
                                 PunitiveEffect.expiry_time<datetime.datetime.now()))
        
    @staticmethod
    def set_expired(effect_id):
        "If a matching effect was found unexpired set it to expired and return True else return False."
        try:
            with Session() as session:
                punitive_effect_query = session.query(PunitiveEffect)
                punitive_effect_query = punitive_effect_query.filter(PunitiveEffect.id==effect_id)
                punitive_effect_query = punitive_effect_query.filter(PunitiveEffect.expired==False)
                
                punitive_effect = punitive_effect_query.one()
                
                punitive_effect.expired = True
                session.commit()
                return True
        except NoResultFound:
            return False