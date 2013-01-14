from Common import *
from TableNames import table_names

import time

class IpName(database_manager.Base):
    __tablename__ = table_names['IpName']
    id = Column(Integer, Sequence(__tablename__+'_id_seq'), primary_key=True)
    ip = Column(BigInteger, index=True)
    name = Column(String(16))
    date = Column(BigInteger, index=True)
    
    def __init__(self, name, ip):
        self.name = name
        self.ip = ip 
        self.date = time.time()
    
    @staticmethod
    def record(name, ip):
        with Session() as session:
            record = IpName(name, ip)
            session.add(record)
            session.commit()
            
    @staticmethod
    def fetch(ip, mask):
        maskedip = ip & mask
        with Session() as session:
            results = session.query(IpName.name, func.max(IpName.date).label("date"), func.count(IpName.date).label("count")).filter(IpName.ip.op('&')(mask)==maskedip).group_by(IpName.ip, IpName.name).all()
            return results
        
            
