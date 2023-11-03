import os
from fastapi import APIRouter, HTTPException, Depends, status, Request, File, UploadFile
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.schemas import users_schemas
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from app.models import models
from utils.users_utils import send_email, hash
from configs.settings import admin_mail,PROJECT_NAME
import random, uuid
from datetime import datetime, timedelta
from app.database import engine, get_db
from typing import Optional
from  utils import oauth2
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

models.Base.metadata.create_all(bind=engine)

# /users/

router = APIRouter(prefix = "/user", tags=['Users Requests'])

# create a new user
@router.post("/create/", status_code = status.HTTP_201_CREATED, response_model=users_schemas.UserListing)
# async def create_user(new_user_c: users_schemas.UserCreate, file: UploadFile = File(...), db: Session = Depends(get_db)):
async def create_user(new_user_c: users_schemas.UserCreate, db: Session = Depends(get_db)):
    # Vérifiez si l'utilisateur existe déjà dans la base de données
    if db.query(models.User).filter(models.User.username == new_user_c.username).first():
        raise HTTPException(status_code=400, detail='Registered user with this username')
    if db.query(models.User).filter(models.User.phone == new_user_c.phone).first():
        raise HTTPException(status_code=400, detail='Registered user with this phone number')
    if db.query(models.User).filter(models.User.email == new_user_c.email).first():
        raise HTTPException(status_code=400, detail='Registered user with this email')
    if db.query(models.User).filter(models.User.image == new_user_c.image).first():
        raise HTTPException(status_code=400, detail='Registered user with this image')
    
    formated_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")# Formatage de la date au format souhaité (par exemple, YYYY-MM-DD HH:MM:SS)
    concatenated_uuid = str(uuid.uuid4())+ ":" + formated_date
    NUM_REF = 10001
    codefin = datetime.now().strftime("%m/%Y")
       
    concatenated_num_ref = str(
            NUM_REF + len(db.query(models.User).filter(models.User.refnumber.endswith(codefin)).all())) + "/" + codefin
    hashed_password = hash(new_user_c.password)
    new_user_c.password = hashed_password
    
    author = "current_user"
    
    new_user= models.User(id = concatenated_uuid, **new_user_c.dict(), refnumber = concatenated_num_ref, created_by = author)
    
    try:
        db.add(new_user )# pour ajouter une tuple
        db.commit() # pour faire l'enregistrement
        db.refresh(new_user)# pour renvoyer le résultat
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=403, detail="Somthing is wrong in the process, pleace try later sorry!")
    
    return jsonable_encoder(new_user)

# Get all users requests
@router.get("/get_all_actif/", response_model=List[users_schemas.UserListing])
async def read_users_actif(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    
    users_queries = db.query(models.User).filter(models.User.active == "True", ).offset(skip).limit(limit).all()
    print(users_queries)
    
    # pas de user
    if not users_queries:
       
        raise HTTPException(status_code=404, detail="User not found")
                        
    return jsonable_encoder(users_queries)



# Get an user
# "/get_user_impersonal/?refnumber=value_refnumber&phone=valeur_phone&email=valeur_email&username=valeur_username" : Retourne `{"param1": "value1", "param2": 42, "param3": null}`.
@router.get("/get_user_by_attribut/", status_code=status.HTTP_200_OK, response_model=List[users_schemas.UserListing])
async def detail_user_by_attribut(refnumber: Optional[str] = None, phone: Optional[str] = None, name: Optional[str] = None, surname: Optional[str] = None, email: Optional[str] = None, username: Optional[str] = None,is_owner: Optional[bool] = None ,is_staff: Optional[bool] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user_query = {} # objet vide
    if refnumber is not None :
        user_query = db.query(models.User).filter(models.User.refnumber == refnumber).offset(skip).limit(limit).all()
    if name is not None :
        user_query = db.query(models.User).filter(models.User.name == name).offset(skip).limit(limit).all()
    if surname is not None :
        user_query = db.query(models.User).filter(models.User.surname == surname).offset(skip).limit(limit).all()
    if phone is not None :
        user_query = db.query(models.User).filter(models.User.phone == phone).offset(skip).limit(limit).all()
    if email is not None:
        user_query = db.query(models.User).filter(models.User.email == email).offset(skip).limit(limit).all()
    if username is not None :
        user_query = db.query(models.User).filter(models.User.username == username).offset(skip).limit(limit).all()
    if is_staff is not None :
        user_query = db.query(models.User).filter(models.User.is_staff == is_staff).offset(skip).limit(limit).all()
    if is_owner is not None :
        user_query = db.query(models.User).filter(models.User.is_owner == is_owner).offset(skip).limit(limit).all()
    
    print(user_query)
    if not user_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User does not exist")
    return jsonable_encoder(user_query)

# Get an user
@router.get("/get/{user_id}", status_code=status.HTTP_200_OK, response_model=users_schemas.UserDetail)
async def detail_user(user_id: str, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == user_id).first()
    if not user_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {user_id} does not exist")
    return jsonable_encoder(user_query)





# update an permission request
@router.put("/update/{user_id}", status_code = status.HTTP_205_RESET_CONTENT, response_model = users_schemas.UserDetail)
async def update_user(user_id: str, user_update: users_schemas.UserUpdate, db: Session = Depends(get_db), current_user : str = Depends(oauth2.get_current_user)):
        
    user_query = db.query(models.User).filter(models.User.id == user_id, models.User.active == "True").first()

    if not user_query:
            
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {user_id} does not exist")
    else:
        
        user_query.updated_by =  current_user.id
        
        if user_update.name:
            user_query.name = user_update.name
        if user_update.surname:
            user_query.surname = user_update.surname
        if user_update.phone:
            user_query.phone = user_update.phone
        if user_update.birthday:
            user_query.birthday = user_update.birthday
        if user_update.gender:
            user_query.gender = user_update.gender
        if user_update.email:
            user_query.email = user_update.email
        if user_update.image:
            user_query.image = user_update.image
        if user_update.username:
            user_query.username = user_update.username
        if user_update.password:
            hashed_password = hash(user_update.password)
            user_update.password = hashed_password
            user_query.password = user_update.password
        if user_update.is_staff:
            user_query.is_staff = user_update.is_staff
        if user_update.is_owner:
            user_query.is_owner = user_update.is_owner
    
    try:
        db.commit() # pour faire l'enregistrement
        db.refresh(user_query)# pour renvoyer le résultat
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=403, detail="Somthing is wrong in the process , pleace try later sorry!")
        
    return jsonable_encoder(user_query)


# delete permission
@router.patch("/delete/{user_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str,  db: Session = Depends(get_db),current_user : str = Depends(oauth2.get_current_user)):
    
    user_query = db.query(models.User).filter(models.User.id == user_id, models.User.active == "True").first()
    
    if not user_query:    
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {user_id} does not exist")
        
    user_query.active = False
    user_query.updated_by =  current_user.id
    
    try:  
        db.commit() # pour faire l'enregistrement
        db.refresh(user_query)# pour renvoyer le résultat
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=403, detail="Somthing is wrong in the process, pleace try later sorry!")
    
    
    return {"message": "User deleted!"}


# Get all user inactive requests
@router.get("/get_all_inactive/", response_model=List[users_schemas.UserListing])
async def read_users_inactive(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user : str = Depends(oauth2.get_current_user)):
    
    users_queries = db.query(models.User).filter(models.User.active == "False", ).offset(skip).limit(limit).all()
    
    # pas de user
    if not users_queries:
       
        raise HTTPException(status_code=404, detail="Users not found")
                        
    return jsonable_encoder(users_queries)


# Restore user
@router.patch("/restore/{user_id}", status_code = status.HTTP_200_OK,response_model = users_schemas.UserListing)
async def restore_user(user_id: str,  db: Session = Depends(get_db), current_user : str = Depends(oauth2.get_current_user)):
    
    user_query = db.query(models.User).filter(models.User.id == user_id, models.User.active == "False").first()
    
    if not user_query:
            
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {user_id} does not exist")
        
    user_query.active = True
    user_query.updated_by =  current_user.id
    
    try:  
        db.commit() # pour faire l'enregistrement
        db.refresh(user_query)# pour renvoyer le résultat
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=403, detail="Somthing is wrong in the process, pleace try later sorry!")
    
    
    return jsonable_encoder(user_query)
