import os
from fastapi import APIRouter, HTTPException, Depends, status, Request, File, UploadFile,Form
from app.models import models
from configs.settings import admin_mail,PARENT_MEDIA_NAME
from app.database import engine, get_db
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image
# from multipart.multipart import parse_options_header

models.Base.metadata.create_all(bind=engine)

# /users/

router = APIRouter(prefix = "/medias*", tags=['Medias Requests'])
 
@router.post("/uploadfile/")
async def create_media(file: UploadFile = File(...), media_use : str = None):
    # content_type, params = parse_options_header(file.content_type)
    
    if not os.path.exists(PARENT_MEDIA_NAME):
        os.makedirs(PARENT_MEDIA_NAME)
        print(f"Répertoire {media_use} créé avec succès!")
    
    # Vérifier si le répertoire enfant existe
    child_path = os.path.join(PARENT_MEDIA_NAME, media_use)
    if not os.path.exists(child_path):
        os.makedirs(child_path)
        
    # Sauvegarde la photo de profil
    image = Image.open(file.file)
    if media_use == "user_medias":
        image.thumbnail((500, 500))  # Redimensionne l'image en 500x500 pixels
        image.save(f"{PARENT_MEDIA_NAME}/user_medias/{file.filename}")
    elif media_use == "product_medias":
        image.save(f"{PARENT_MEDIA_NAME}/product_medias/{file.filename}")
    elif media_use == "event_multi_medias":
        image.save(f"{PARENT_MEDIA_NAME}/event_multi_medias/{file.filename}")
    elif media_use == "anounce_multi_medias":
        image.save(f"{PARENT_MEDIA_NAME}/anounce_multi_medias/{file.filename}")
    elif media_use == "entertainment_site_multi_medias":
        image.save(f"{PARENT_MEDIA_NAME}/entertainment_site_multi_medias/{file.filename}")
    else :
        raise HTTPException(status_code=403, detail="this file cannot be saved, sorry!")
        
    return {"filename save": file.filename}


@router.get("/image/{image_name},{media_use}")
async def get_media(image_name: str,media_use: str):
    child_path = os.path.join(PARENT_MEDIA_NAME, media_use)
    image_path = os.path.join(child_path, image_name)
    return FileResponse(image_path)