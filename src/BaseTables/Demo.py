from Common import *
from TableNames import table_names

import datetime, time

class Demo(database_manager.Base):
    __tablename__ = table_names['Demo']
    id = Column(Integer, Sequence(__tablename__+'_id_seq'), primary_key=True)
    filename = Column(String(255), nullable=False)
    server = Column(String(32), nullable=False)
    recorded_time = Column(DateTime, nullable=False)
    mode_name = Column(String(32))
    map_name = Column(String(32))
    
    def __init__(self, filename, server, mode_name, map_name):
        self.filename = filename
        self.server = server
        self.recorded_time = datetime.datetime.now()
        self.map_name = map_name
        self.mode_name = mode_name
    
    @staticmethod
    def add_demo(filename, server, mode_name, map_name):
        """Adds a new entry for this demo and returns the id of the demo entry."""
        with Session() as session:
            demo = Demo(filename, server, mode_name, map_name)
            session.add(demo)
            session.commit()
            return demo.id