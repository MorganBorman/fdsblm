from Common import *
from TableNames import table_names

import datetime, time

class DemoTag(database_manager.Base):
    __tablename__ = table_names['DemoTag']
    id = Column(BigInteger, Sequence(__tablename__+'_id_seq'), primary_key=True)
    demo_id = Column(Integer, nullable=False)
    member_id = Column(Integer, nullable=False)
    tag = Column(String(60), nullable=False)
    
    def __init__(self, demo_id, member_id, tag):
        self.demo_id = demo_id
        self.member_id = member_id
        self.tag = tag
    
    @staticmethod
    def add_tag(demo_id, member_id, tag):
        """Adds a new demo tag entry for the given demo id."""
        if demo_id is None:
            raise ValueError("Cannot add tag for None demo.")
        
        with Session() as session:
            demo_tag = DemoTag(demo_id, member_id, tag)
            session.add(demo_tag)
            session.commit()