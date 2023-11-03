import os
from fastapi import APIRouter, HTTPException, Depends, status, Request, File, UploadFile
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.schemas import entertainment_sites_schemas
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

# /entertainment_sites/

router = APIRouter(prefix = "/entertainment_site", tags=['Entertainment_sites Requests'])
 
# create a new entertainment_site sheet
@router.post("/create/", status_code = status.HTTP_201_CREATED, response_model=entertainment_sites_schemas.EntertainmentSiteListing)
async def create_entertainment_site(new_entertainment_site_c: entertainment_sites_schemas.EntertainmentSiteCreate, db: Session = Depends(get_db), current_user : str = Depends(oauth2.get_current_user)):
    
    formated_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")# Formatage de la date au format souhaité (par exemple, YYYY-MM-DD HH:MM:SS)
    concatenated_uuid = str(uuid.uuid4())+ ":" + formated_date
    NUM_REF = 10001
    codefin = datetime.now().strftime("%m/%Y")
    concatenated_num_ref = str(
            NUM_REF + len(db.query(models.EntertainmentSite).filter(models.EntertainmentSite.refnumber.endswith(codefin)).all())) + "/" + codefin
    
    author = current_user.id
    
    new_entertainment_site= models.EntertainmentSite(id = concatenated_uuid, **new_entertainment_site_c.dict(), refnumber = concatenated_num_ref, created_by = author)
    
    try:
        db.add(new_entertainment_site )# pour ajouter une tuple
        db.commit() # pour faire l'enregistrement
        db.refresh(new_entertainment_site)# pour renvoyer le résultat
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=403, detail="Somthing is wrong in the process, pleace try later sorry!")
    
    return jsonable_encoder(new_entertainment_site)

# Get all entertainment_sites requests
@router.get("/get_all_actif/", response_model=List[entertainment_sites_schemas.EntertainmentSiteListing])
async def read_entertainment_sites_actif(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    
    entertainment_sites_queries = db.query(models.EntertainmentSite).filter(models.EntertainmentSite.active == "True", ).offset(skip).limit(limit).all()
    
    # pas de entertainment_site
    if not entertainment_sites_queries:
       
        raise HTTPException(status_code=404, detail="entertainment_site not found")
                        
    return jsonable_encoder(entertainment_sites_queries)



# Get an entertainment_site
# "/get_entertainment_site_impersonal/?refnumber=value_refnumber&phone=valeur_phone&email=valeur_email&entertainment_sitename=valeur_entertainment_sitename" : Retourne `{"param1": "value1", "param2": 42, "param3": null}`.
@router.get("/get_entertainment_site_by_attribute/", status_code=status.HTTP_200_OK, response_model=List[entertainment_sites_schemas.EntertainmentSiteListing])
async def detail_entertainment_site_by_attribute(refnumber: Optional[str] = None, country_id: Optional[str] = None, name: Optional[str] = None, description: Optional[str] = None, address: Optional[str] = None, longitude: Optional[str] = None, latitude: Optional[str] = None, owner_id: Optional[str] = None, quarter_id: Optional[str] = None, category_site_id: Optional[str] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    entertainment_site_query = {} # objet vide
    if refnumber is not None :
        entertainment_site_query = db.query(models.EntertainmentSite).filter(models.EntertainmentSite.refnumber == refnumber).offset(skip).limit(limit).all()
    if name is not None :
        entertainment_site_query = db.query(models.EntertainmentSite).filter(models.EntertainmentSite.name == name).offset(skip).limit(limit).all()
    if description is not None :
        entertainment_site_query = db.query(models.EntertainmentSite).filter(models.EntertainmentSite.description == description).offset(skip).limit(limit).all()
    if status is not None :
        entertainment_site_query = db.query(models.EntertainmentSite).filter(models.EntertainmentSite.status == status).offset(skip).limit(limit).all()
    if address is not None :
        entertainment_site_query = db.query(models.EntertainmentSite).filter(models.EntertainmentSite.address == address).offset(skip).limit(limit).all()
    if longitude is not None :
        entertainment_site_query = db.query(models.EntertainmentSite).filter(models.EntertainmentSite.longitude == longitude).offset(skip).limit(limit).all()
    if latitude is not None :
        entertainment_site_query = db.query(models.EntertainmentSite).filter(models.EntertainmentSite.latitude == latitude).offset(skip).limit(limit).all()
    if owner_id is not None :
        entertainment_site_query = db.query(models.EntertainmentSite).filter(models.EntertainmentSite.owner_id == owner_id).offset(skip).limit(limit).all()
    if quarter_id is not None :
        entertainment_site_query = db.query(models.EntertainmentSite).filter(models.EntertainmentSite.quarter_id == quarter_id).offset(skip).limit(limit).all()
    if category_site_id is not None :
        entertainment_site_query = db.query(models.EntertainmentSite).filter(models.EntertainmentSite.category_site_id == category_site_id).offset(skip).limit(limit).all()
    
    
    if not entertainment_site_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"entertainment_site does not exist")
    return jsonable_encoder(entertainment_site_query)

# Get an entertainment_site
@router.get("/get/{entertainment_site_id}", status_code=status.HTTP_200_OK, response_model=entertainment_sites_schemas.EntertainmentSiteDetail)
async def detail_entertainment_site(entertainment_site_id: str, db: Session = Depends(get_db)):
    entertainment_site_query = db.query(models.EntertainmentSite).filter(models.EntertainmentSite.id == entertainment_site_id).first()
    if not entertainment_site_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Entertainment site  with id: {entertainment_site_id} does not exist")
    return jsonable_encoder(entertainment_site_query)





# update an entertainment_site request
@router.put("/update/{entertainment_site_id}", status_code = status.HTTP_205_RESET_CONTENT, response_model = entertainment_sites_schemas.EntertainmentSiteDetail)
async def update_entertainment_site(entertainment_site_id: str, entertainment_site_update: entertainment_sites_schemas.EntertainmentSiteUpdate, db: Session = Depends(get_db),current_user : str = Depends(oauth2.get_current_user)):
        
    entertainment_site_query = db.query(models.EntertainmentSite).filter(models.EntertainmentSite.id == entertainment_site_id, models.EntertainmentSite.active == "True").first()

    if not entertainment_site_query:
            
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Entertainment site  with id: {entertainment_site_id} does not exist")
    else:
        
        entertainment_site_query.updated_by =  current_user.id
        
        if entertainment_site_update.name:
            entertainment_site_query.name = entertainment_site_update.name
        if entertainment_site_update.description:
            entertainment_site_query.description = entertainment_site_update.description
        if entertainment_site_update.status:
            entertainment_site_query.status = entertainment_site_update.status
        if entertainment_site_update.address:
            entertainment_site_query.address = entertainment_site_update.address
        if entertainment_site_update.longitude:
            entertainment_site_query.longitude = entertainment_site_update.longitude
        if entertainment_site_update.latitude:
            entertainment_site_query.latitude = entertainment_site_update.latitude
        if entertainment_site_update.owner_id:
            entertainment_site_query.owner_id = entertainment_site_update.owner_id
        if entertainment_site_update.quarter_id:
            entertainment_site_query.quarter_id = entertainment_site_update.quarter_id
        if entertainment_site_update.category_site_id:
            entertainment_site_query.category_site_id = entertainment_site_update.category_site_id
        
    
    try:
        db.commit() # pour faire l'enregistrement
        db.refresh(entertainment_site_query)# pour renvoyer le résultat
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=403, detail="Somthing is wrong in the process , pleace try later sorry!")
        
    return jsonable_encoder(entertainment_site_query)


# delete entertainment_site
@router.patch("/delete/{entertainment_site_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_entertainment_site(entertainment_site_id: str,  db: Session = Depends(get_db), current_user : str = Depends(oauth2.get_current_user)):
    
    entertainment_site_query = db.query(models.EntertainmentSite).filter(models.EntertainmentSite.id == entertainment_site_id, models.EntertainmentSite.active == "True").first()
    
    if not entertainment_site_query:    
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Entertainment site  with id: {entertainment_site_id} does not exist")
        
    entertainment_site_query.active = False
    entertainment_site_query.updated_by =  current_user.id
    
    try:  
        db.commit() # pour faire l'enregistrement
        db.refresh(entertainment_site_query)# pour renvoyer le résultat
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=403, detail="Somthing is wrong in the process, pleace try later sorry!")
    
    
    return {"message": "entertainment_site deleted!"}


# Get all entertainment_site inactive requests
@router.get("/get_all_inactive/", response_model=List[entertainment_sites_schemas.EntertainmentSiteListing])
async def read_entertainment_sites_inactive(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user : str = Depends(oauth2.get_current_user)):
    
    entertainment_sites_queries = db.query(models.EntertainmentSite).filter(models.EntertainmentSite.active == "False", ).offset(skip).limit(limit).all()
    
    # pas de entertainment_site
    if not entertainment_sites_queries:
       
        raise HTTPException(status_code=404, detail="entertainment_sites not found")
                        
    return jsonable_encoder(entertainment_sites_queries)


# Restore entertainment_site
@router.patch("/restore/{entertainment_site_id}", status_code = status.HTTP_200_OK,response_model = entertainment_sites_schemas.EntertainmentSiteListing)
async def restore_entertainment_site(entertainment_site_id: str,  db: Session = Depends(get_db), current_user : str = Depends(oauth2.get_current_user)):
    
    entertainment_site_query = db.query(models.EntertainmentSite).filter(models.EntertainmentSite.id == entertainment_site_id, models.EntertainmentSite.active == "False").first()
    
    if not entertainment_site_query:
            
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Entertainment site  with id: {entertainment_site_id} does not exist")
        
    entertainment_site_query.active = True
    entertainment_site_query.updated_by =  current_user.id
    
    try:  
        db.commit() # pour faire l'enregistrement
        db.refresh(entertainment_site_query)# pour renvoyer le résultat
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=403, detail="Somthing is wrong in the process, pleace try later sorry!")
    
    
    return jsonable_encoder(entertainment_site_query)
