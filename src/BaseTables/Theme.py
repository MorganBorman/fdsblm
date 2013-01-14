from Common import *
from TableNames import table_names

class Theme(database_manager.Base):
    __tablename__ = table_names['Theme']
    id_member = Column(SmallInteger, primary_key=True)
    id_theme = Column(SmallInteger, primary_key=True)
    variable = Column(String(255), primary_key=True)
    value = Column(Text)
    
    @staticmethod
    def getvariable(id_member, variable):
        try:
            with Session() as session:
                return session.query(Theme.value).filter(Theme.id_member==id_member).filter(Theme.variable==variable).scalar()
        except NoResultFound:
            return None
        
    @staticmethod
    def setvariable(id_member, variable, value):
            with Session() as session:
                try:
                    variables = session.query(Theme).filter(Theme.id_member==id_member).filter(Theme.variable==variable).all()
                    
                    if len(variables) > 0:
                        for row in variables:
                            row.value = value;
                            session.add(row)
                    else:
                        raise NoResultFound()
                
                except NoResultFound:
                    row = Theme(id_member=id_member, id_theme=1, variable=variable, value=value)
                    session.add(row)
                    
                session.commit()
