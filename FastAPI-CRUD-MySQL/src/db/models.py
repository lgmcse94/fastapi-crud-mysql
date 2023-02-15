from uuid import uuid4

from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import Boolean

from db import base


class AllDBs(base):
    __tablename__ = 'alldbs'
    #__table_args__ = {'schema': 'sample'}

    id = Column(String(500), primary_key=True, index=True, default=str(uuid4()))
    db_type = Column(String(500))
    db_name = Column(String(500))
    db_endpoint = Column(String(500))
    password = Column(String(500))
    is_active = Column(Boolean, default=True)
    created_by = Column(String(500))
    modified_by = Column(String(500))
    created_date = Column(DateTime(timezone=False), server_default=func.now())
    modified_date = Column(DateTime(timezone=False), onupdate=func.now())

    def __repr__(self):
        return (
            f"<AllDBs(id = {self.id},db_type = {self.db_type}, "
            f"db_name = {self.db_name},db_endpoint = {self.db_endpoint},"
            f"password = {self.password},is_active = {self.is_active},"
            f"created_by = {self.created_by},modified_by = {self.modified_by},"
            f"created_date = {self.created_date},modified_date = {self.modified_date})>")
