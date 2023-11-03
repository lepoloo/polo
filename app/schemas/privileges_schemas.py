from pydantic import BaseModel, EmailStr, PositiveInt, validator, root_validator, constr,Field
from datetime import datetime, date
from enum import Enum
from typing import Optional

class Privilege(BaseModel):
    name: str
    description: str
    
    

class PrivilegeCreate(Privilege):
   pass


class PrivilegeListing(Privilege):
    id: str
    refnumber: str
    
    class Config:
        from_attributes = True 

class PrivilegeDetail(PrivilegeListing):
    
    created_at: datetime
    created_by: str
    updated_at: Optional[datetime] = None
    updated_by: Optional[constr(max_length=256)] = None
    
    class Config:
        from_attributes = True 
        # orm_mode = True 
        

class PrivilegeUpdate(BaseModel):
    name: Optional[constr(max_length=256)] = None
    description: Optional[constr(max_length=65535)] = None
    

