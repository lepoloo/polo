from pydantic import BaseModel, EmailStr, PositiveInt, validator, root_validator, constr,Field
from datetime import datetime, date
from enum import Enum
from typing import Optional, List

class EntertainmentSite(BaseModel):
    name: str
    address: str
    description: str = Field(..., max_length=65535)
    longitude: str = Field(..., description="Longitude position information of fite.")
    latitude: str = Field(..., description="Longitude position information of fite.")
    quarter_id: str
    # category_site_id: str
    
    
    

class EntertainmentSiteCreate(EntertainmentSite):
    pass


class EntertainmentSiteListing(EntertainmentSite):
    id: str
    owner_id: str
    refnumber: str
    nb_visite: int
    
    class Config:
        from_attributes = True 

class EntertainmentSiteDetail(EntertainmentSiteListing):
    # images: List[str]
    created_at: datetime
    created_by: str
    updated_at: Optional[datetime] = None
    updated_by: Optional[constr(max_length=256)] = None
    
    class Config:
        from_attributes = True 
        # orm_mode = True 
        

class EntertainmentSiteUpdate(BaseModel):
    name: Optional[constr(max_length=256)] = None
    description: Optional[constr(max_length=65535)] = None
    nb_visite: Optional[int] = Field(None, ge=0)
    address: Optional[constr(max_length=256)] = None
    longitude: Optional[constr(max_length=256)] = None
    latitude: Optional[constr(max_length=256)] = None
    owner_id: Optional[constr(max_length=256)] = None
    quarter_id: Optional[constr(max_length=256)] = None
    # category_site_id: Optional[constr(max_length=256)] = None
    
    # active: bool = True
