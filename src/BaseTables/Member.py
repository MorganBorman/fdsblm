from Common import *
import TableNames
from TableNames import table_names
from MemberGroup import MemberGroup
from Theme import Theme

class Member(database_manager.Base):
    __tablename__ = table_names['Member']
    id_member = Column(Integer, primary_key=True)
    member_name = Column(String(80))
    real_name = Column(String(255))
    email_address = Column(String(255))
    id_group = Column(SmallInteger)
    additional_groups = Column(String(255))
    
    @property
    def ingame(self):
        return Theme.getvariable(self.id_member, "cust_ingame")
        
    @ingame.setter
    def ingame(self, value):
        Theme.setvariable(self.id_member, "cust_ingame", value)
    
    @property
    def public_auth_key(self):
        return Theme.getvariable(self.id_member, "cust_public")
        
    @public_auth_key.setter
    def public_auth_key(self, value):
        Theme.setvariable(self.id_member, "cust_public", value)
        
    @property
    def private_auth_key(self):
        return Theme.getvariable(self.id_member, "cust_privat")
        
    @private_auth_key.setter
    def private_auth_key(self, value):
        Theme.setvariable(self.id_member, "cust_privat", value)
    
    @staticmethod
    def by_member_id(id_member):
        try:
            with Session() as session:
                return session.query(Member).filter(Member.id_member==id_member).one()
        except NoResultFound:
            return None
    
    @staticmethod
    def by_member_email(member_email):
        try:
            with Session() as session:
                return session.query(Member).filter(Member.email_address==member_email).one()
        except NoResultFound:
            return None
    
    @staticmethod
    def by_member_name(member_name):
        try:
            with Session() as session:
                return session.query(Member).filter(Member.member_name==member_name).one()
        except NoResultFound:
            return None
            
    @property
    def groups(self):
        group_ids = [self.id_group]
        group_ids.extend(map(int, filter(lambda g: g != "", self.additional_groups.split(','))))
        
        try:
            with Session() as session:
                return session.query(MemberGroup).filter(MemberGroup.id_group.in_(group_ids)).all()
        except NoResultFound:
            return None
            
    @property
    def group_list(self):
        return map(lambda g: g.group_name, self.groups)
