import os
from fastapi import APIRouter, HTTPException, Depends, status, Request, File, UploadFile
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.schemas import likes_schemas
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from app.models import models
from configs.settings import admin_mail,PROJECT_NAME
import random, uuid
from datetime import datetime, timedelta
from app.database import engine, get_db
from typing import Optional
from  utils import oauth2
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

models.Base.metadata.create_all(bind=engine)

# Fonction pour permuter la valeur d'un booléen
def toggle_boolean(value):
    return not value

# /likes/

router = APIRouter(prefix = "/like", tags=['Likes Requests'])
 
# create like or dislike
@router.post("/create/", status_code = status.HTTP_201_CREATED, response_model=likes_schemas.LikeListing)
async def create_like(new_like_c: likes_schemas.LikeCreate, db: Session = Depends(get_db), current_user : str = Depends(oauth2.get_current_user)):
    likes_queries = db.query(models.Like).filter(models.Like.owner_id == new_like_c.owner_id,models.Like.owner_id == new_like_c.owner_id ).all()
    if not likes_queries:
        formated_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")# Formatage de la date au format souhaité (par exemple, YYYY-MM-DD HH:MM:SS)
        concatenated_uuid = str(uuid.uuid4())+ ":" + formated_date
        NUM_REF = 10001
        codefin = datetime.now().strftime("%m/%Y")
        concatenated_num_ref = str(
                NUM_REF + len(db.query(models.Like).filter(models.Like.refnumber.endswith(codefin)).all())) + "/" + codefin
        
        author = current_user.id
        
        likes_queries= models.Like(id = concatenated_uuid, **new_like_c.dict(), refnumber = concatenated_num_ref, created_by = author)
        
        try:
            db.add(likes_queries )# pour ajouter une tuple
            db.commit() # pour faire l'enregistrement
            db.refresh(likes_queries)# pour renvoyer le résultat
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=403, detail="Somthing is wrong in the process, pleace try later sorry!")
        
    else:
        
        likes_queries.active = toggle_boolean(likes_queries.active)
    
    return jsonable_encoder(likes_queries)

# Get all likes requests
@router.get("/get_all_actif/", response_model=List[likes_schemas.LikeListing])
async def read_likes_actif(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    
    likes_queries = db.query(models.Like).filter(models.Like.active == "True", ).offset(skip).limit(limit).all()
    
    # pas de like
    if not likes_queries:
       
        raise HTTPException(status_code=404, detail="like not found")
                        
    return jsonable_encoder(likes_queries)



# Get an like
# "/get_like_impersonal/?refnumber=value_refnumber&phone=valeur_phone&email=valeur_email&likename=valeur_likename" : Retourne `{"param1": "value1", "param2": 42, "param3": null}`.
@router.get("/get_like_by_attribute/", status_code=status.HTTP_200_OK, response_model=List[likes_schemas.LikeListing])
async def detail_like_by_attribute(refnumber: Optional[str] = None, entertainment_site_id: Optional[str] = None, owner_id: Optional[str] = None, description: Optional[str] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    like_query = {} # objet vide
    if refnumber is not None :
        like_query = db.query(models.Like).filter(models.Like.refnumber == refnumber).offset(skip).limit(limit).all()
    if owner_id is not None :
        like_query = db.query(models.Like).filter(models.Like.owner_id == owner_id).offset(skip).limit(limit).all()
    if entertainment_site_id is not None :
        like_query = db.query(models.Like).filter(models.Like.entertainment_site_id == entertainment_site_id).offset(skip).limit(limit).all()
    
    
    if not like_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"like does not exist")
    return jsonable_encoder(like_query)

# Get an like
@router.get("/get/{like_id}", status_code=status.HTTP_200_OK, response_model=likes_schemas.likeDetail)
async def detail_like(like_id: str, db: Session = Depends(get_db)):
    like_query = db.query(models.Like).filter(models.Like.id == like_id).first()
    if not like_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"like with id: {like_id} does not exist")
    return jsonable_encoder(like_query)






