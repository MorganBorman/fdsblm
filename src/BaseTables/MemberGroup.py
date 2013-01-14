from Common import *
from TableNames import table_names

class MemberGroup(database_manager.Base):
    __tablename__ = table_names['MemberGroup']
    id_group = Column(SmallInteger, primary_key=True)
    group_name = Column(String(80))
