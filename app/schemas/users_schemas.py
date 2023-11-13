from pydantic import BaseModel, EmailStr, PositiveInt, validator, root_validator, constr,Field
from datetime import datetime, date
from enum import Enum
from typing import Optional
from app.schemas.profils_schemas import ProfilListing
from app.schemas.entertainment_sites_schemas import EntertainmentSiteListing
from app.models.models import GenderType

class User(BaseModel):
    name: str
    surname: str
    phone: str
    email: EmailStr
    birthday: date
    gender: GenderType
    username: str
    

class UserCreate(User):
   image: str
   password: str
   is_staff: bool = False
   is_owner: bool = False


class UserListing(User):
    id: str
    refnumber: str
    # entertainment_site: ProfilListing
    # profil:EntertainmentSiteListing
    
    class Config:
        from_attributes = True 

class UserDetail(UserListing):
    
    image: str
    is_staff: bool
    is_owner: bool
    created_at: datetime
    created_by: str
    # entertainment_site: ProfilListing
    # profil:EntertainmentSiteListing
    updated_at: Optional[datetime] = None
    updated_by: Optional[constr(max_length=256)] = None
    
    class Config:
        from_attributes = True 
        # orm_mode = True 
        

class UserUpdate(BaseModel):
    name: Optional[constr(max_length=256)] = None
    surname: Optional[constr(max_length=256)] = None
    phone: Optional[constr(max_length=256)] = None
    birthday: Optional[date] = None
    gender: Optional[GenderType] = None
    email: Optional[EmailStr] = None
    image: Optional[constr(max_length=256)] = None
    username: Optional[constr(max_length=256)] = None
    password: Optional[constr(max_length=256)] = None
    is_staff: Optional[bool] = False
    is_owner: Optional[bool] = False
    # active: bool = True


class UserLogin(BaseModel):
#    email: EmailStr
   username: str
   password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
