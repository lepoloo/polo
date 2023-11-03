from pydantic import BaseModel, EmailStr, PositiveInt, validator, root_validator, constr,Field
from datetime import datetime, date
from enum import Enum
from typing import Optional

class Country(BaseModel):
    name: str
    
    
    

class CountryCreate(Country):
   pass


class CountryListing(Country):
    id: str
    refnumber: str
    
    class Config:
        from_attributes = True 

class CountryDetail(CountryListing):
    
    created_at: datetime
    created_by: str
    updated_at: Optional[datetime] = None
    updated_by: Optional[constr(max_length=256)] = None
    
    class Config:
        from_attributes = True 
        # orm_mode = True 
        

class CountryUpdate(BaseModel):
    name: Optional[constr(max_length=256)] = None
    # active: bool = True
