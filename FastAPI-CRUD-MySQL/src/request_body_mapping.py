from typing import Any
from typing import Optional

from pydantic import BaseModel

class AllDBs(BaseModel):
    db_type: str
    db_name: str
    db_endpoint: str
    password: str

class UpdateStatus(BaseModel):
    status: bool
