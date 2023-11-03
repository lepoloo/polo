from pydantic import BaseModel, EmailStr, PositiveInt, validator, root_validator, constr,Field
from datetime import datetime, date
from enum import Enum
from typing import Optional
from app.schemas import countries_schemas

class Town(BaseModel):
    name: str
    country_id: str
    
    
    

class TownCreate(Town):
   pass


class TownListing(Town):
    id: str
    refnumber: str
    # country_id: countries_schemas.CountryListing
    
    class Config:
        from_attributes = True 

class TownDetail(TownListing):
    
    created_at: datetime
    created_by: str
    updated_at: Optional[datetime] = None
    updated_by: Optional[constr(max_length=256)] = None
    
    class Config:
        from_attributes = True 
        # orm_mode = True 
        

class TownUpdate(BaseModel):
    name: Optional[constr(max_length=256)] = None
    country_id: Optional[constr(max_length=256)] = None
    
    # active: bool = True
