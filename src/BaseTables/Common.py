from DatabaseManager import database_manager, Session

from sqlalchemy import or_, func
from sqlalchemy import SmallInteger, Integer, BigInteger, String, Boolean, Text
from sqlalchemy import DateTime
from sqlalchemy import Column, Sequence, ForeignKey

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.orm import relation, mapper, relationship, backref
from sqlalchemy.schema import UniqueConstraint
