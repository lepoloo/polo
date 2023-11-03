from pydantic import BaseModel, EmailStr, PositiveInt, validator, root_validator, constr,Field
from datetime import datetime, date
from enum import Enum
from typing import Optional

class FamilyCard(BaseModel):
    name: str
    description: str
    
    

class FamilyCardCreate(FamilyCard):
   pass


class FamilyCardListing(FamilyCard):
    id: str
    refnumber: str
    
    class Config:
        from_attributes = True 

class FamilyCardDetail(FamilyCardListing):
    
    created_at: datetime
    created_by: str
    updated_at: Optional[datetime] = None
    updated_by: Optional[constr(max_length=256)] = None
    
    class Config:
        from_attributes = True 
        # orm_mode = True 
        

class FamilyCardUpdate(BaseModel):
    name: Optional[constr(max_length=256)] = None
    description: Optional[constr(max_length=65535)] = None
    

