from pydantic import BaseModel, EmailStr, PositiveInt, validator, root_validator, constr,Field
from datetime import datetime, date
from enum import Enum
from typing import Optional

class Event(BaseModel):
    name: str
    description: str = Field(..., max_length=65535)
    label_event_id: str
    entertainment_site_id: str
    start_date: datetime
    end_date: datetime
    start_hour: str
    end_hour: str
    
    

class EventCreate(Event):
   pass


class EventListing(Event):
    id: str
    refnumber: str
    
    class Config:
        from_attributes = True 

class EventDetail(EventListing):
    nb_visite: str
    created_at: datetime
    created_by: str
    updated_at: Optional[datetime] = None
    updated_by: Optional[constr(max_length=256)] = None
    
    class Config:
        from_attributes = True 
        # orm_mode = True 
        

class EventUpdate(BaseModel):
    name: Optional[constr(max_length=256)] = None
    description: Optional[constr(max_length=65535)] = None
    label_event_id: Optional[constr(max_length=256)] = None
    entertainment_site_id: Optional[constr(max_length=256)] = None
    status: Optional[constr(max_length=256)] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    start_hour: Optional[constr(max_length=256)] = None
    end_hour: Optional[constr(max_length=256)] = None
    # active: bool = True
   