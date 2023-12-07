import os
from fastapi import APIRouter, HTTPException, Depends, status, Request, File, UploadFile,Form
from app.models import models
from app import config_sething
from app.database import engine, get_db
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from typing import List
from datetime import datetime
from PIL import Image
# from multipart.multipart import parse_options_header

models.Base.metadata.create_all(bind=engine)

# /users/
PARENT_MEDIA_NAME = config_sething.parent_media_name
router = APIRouter(prefix = "/medias", tags=['Medias Requests'])
 
@router.post("/uploadfile/")
async def create_media(file: UploadFile = File(...), media_use : str = None):
    
    if not os.path.exists(PARENT_MEDIA_NAME):
        os.makedirs(PARENT_MEDIA_NAME)
    
    # Vérifier si le répertoire enfant existe
    child_path = os.path.join(PARENT_MEDIA_NAME, media_use)
    if not os.path.exists(child_path):
        os.makedirs(child_path)
        
    # Sauvegarde la photo de profil
    image = Image.open(file.file)
    # file.filename = formated_date+":"+file.filename
    if media_use == "user_medias":
        image.thumbnail((500, 500))  # Redimensionne l'image en 500x500 pixels
        image.save(f"{PARENT_MEDIA_NAME}/{media_use}/{file.filename}")
    elif media_use == "product_medias":
        image.save(f"{PARENT_MEDIA_NAME}/{media_use}/{file.filename}")
    elif media_use == "card_medias":
        image.save(f"{PARENT_MEDIA_NAME}/{media_use}/{file.filename}")
    elif media_use == "event_multi_medias":
        image.save(f"{PARENT_MEDIA_NAME}/{media_use}/{file.filename}")
    elif media_use == "anounce_multi_medias":
        image.save(f"{PARENT_MEDIA_NAME}/{media_use}/{file.filename}")
    elif media_use == "category_site_multi_medias":
        image.save(f"{PARENT_MEDIA_NAME}/{media_use}/{file.filename}")
    elif media_use == "entertainment_site_multi_medias":
        image.save(f"{PARENT_MEDIA_NAME}/{media_use}/{file.filename}")
    elif media_use == "reel_medias":
        image.save(f"{PARENT_MEDIA_NAME}/{media_use}/{file.filename}")
    else :
        raise HTTPException(status_code=403, detail="this file cannot be saved, sorry!")
        
    return {"filename save": file.filename}


@router.get("/image/{image_name},{media_use}")
async def get_media(image_name: str, media_use: str):
    print(media_use)
    print(image_name)
    if media_use != "user_medias":
        child_path = os.path.join(PARENT_MEDIA_NAME, media_use)
        image_path = os.path.join(child_path, image_name)
        if not image_name :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"we don't have this media files!")
        return FileResponse(image_path)
    elif media_use != "product_medias":
        child_path = os.path.join(PARENT_MEDIA_NAME, media_use)
        image_path = os.path.join(child_path, image_name)
        if not image_name :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"we don't have this media files!")
        return FileResponse(image_path)
    elif media_use != "card_medias":
        child_path = os.path.join(PARENT_MEDIA_NAME, media_use)
        image_path = os.path.join(child_path, image_name)
        if not image_name :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"we don't have this media files!")
        return FileResponse(image_path)
    elif media_use != "anounce_multi_medias":
        child_path = os.path.join(PARENT_MEDIA_NAME, media_use)
        image_path = os.path.join(child_path, image_name)
        if not image_name :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"we don't have this media files!")
        return FileResponse(image_path)
    elif media_use != "event_multi_medias":
        child_path = os.path.join(PARENT_MEDIA_NAME, media_use)
        image_path = os.path.join(child_path, image_name)
        if not image_name :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"we don't have this media files!")
        return FileResponse(image_path)
    elif media_use != "reel_medias":
        child_path = os.path.join(PARENT_MEDIA_NAME, media_use)
        image_path = os.path.join(child_path, image_name)
        if not image_name :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"we don't have this media files!")
        return FileResponse(image_path)
    elif media_use != "category_site_multi_medias":
        child_path = os.path.join(PARENT_MEDIA_NAME, media_use)
        image_path = os.path.join(child_path, image_name)
        if not image_name :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"we don't have this media files!")
        return FileResponse(image_path)
    elif media_use != "entertainment_site_multi_medias":
        child_path = os.path.join(PARENT_MEDIA_NAME, media_use)
        image_path = os.path.join(child_path, image_name)
        if not image_name :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"we don't have this media files!")
        return FileResponse(image_path)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"we don't have this media files!")
    


# @router.get("/image/{image_name},{media_use}")
# async def get_media(image_name: str, media_use: str):
#     print("ok1")
#     if media_use == "user_medias" or media_use == "product_medias"or media_use == "card_medias" or media_use == "reel_medias"  or media_use == "anounce_multi_medias" or media_use == "event_multi_medias" or media_use == "category_site_multi_medias" or media_use == "entertainment_site_multi_medias":
#         print("ok2")
#         child_path = os.path.join(PARENT_MEDIA_NAME, media_use)
#         print(child_path)
#         image_path = os.path.join(child_path, image_name)
#         return FileResponse(image_path)
#     else:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"we don't have media files this media file!")



@router.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...), media_use : str = None):
    
    # formated_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if not os.path.exists(PARENT_MEDIA_NAME):
        os.makedirs(PARENT_MEDIA_NAME)
        print(f"Répertoire {media_use} créé avec succès!")
    
    # Vérifier si le répertoire enfant existe
    child_path = os.path.join(PARENT_MEDIA_NAME, media_use)
    if not os.path.exists(child_path):
        os.makedirs(child_path)
    media_name = [file.filename for file in files]
    # media_size=[len(file) for file in files]
    # image_infos={media_name, media_size}
    for file in files:
        # Sauvegarde la photo de profil
        media = Image.open(file.file)
        # file.filename = formated_date+":"+file.filename
        if media_use == "user_medias":
            media.thumbnail((500, 500))  # Redimensionne l'image en 500x500 pixels
            media.save(f"{PARENT_MEDIA_NAME}/{media_use}/{file.filename}")
        elif media_use == "product_medias":
            media.save(f"{PARENT_MEDIA_NAME}/{media_use}/{file.filename}")
        elif media_use == "card_medias":
            media.save(f"{PARENT_MEDIA_NAME}/{media_use}/{file.filename}")
        elif media_use == "event_multi_medias":
            media.save(f"{PARENT_MEDIA_NAME}/{media_use}/{file.filename}")
        elif media_use == "anounce_multi_medias":
            media.save(f"{PARENT_MEDIA_NAME}/{media_use}/{file.filename}")
        elif media_use == "category_site_multi_medias":
            media.save(f"{PARENT_MEDIA_NAME}/{media_use}/{file.filename}")
        elif media_use == "entertainment_site_multi_medias":
            media.save(f"{PARENT_MEDIA_NAME}/{media_use}/{file.filename}")
        elif media_use == "reel_medias":
            media.save(f"{PARENT_MEDIA_NAME}/{media_use}/{file.filename}")
        else :
            raise HTTPException(status_code=403, detail="this file cannot be saved, sorry!")
    # return {"media information": image_infos}
    return {"media information": media_name}


# renvois une liste d'image
# @router.get("/images/{image_names:List[str]}/{media_use:str}")
@router.get("/images/{image_names:List[str]},{media_use:str}")
async def get_media_files(image_names: List[str], media_use: str):
    if media_use != "user_medias" or media_use != "product_medias" or media_use != "card_medias" or media_use != "anounce_multi_medias" or media_use != "event_multi_medias" or media_use != "category_site_multi_medias" or media_use != "entertainment_site_multi_medias":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"we don't have media files this media file!")
    
    child_path = os.path.join(PARENT_MEDIA_NAME, media_use)
    
    responses = []
    for image_name in image_names:
        image_path = os.path.join(child_path, image_name)
        # responses.append(FileResponse(image_path))
        responses.append(image_path)
      
    return responses



# upmode la video
@router.post("/upload_videos/")
async def upload_videos(files: list[UploadFile] = File(...), media_use : str = None):
    if not os.path.exists(PARENT_MEDIA_NAME):
        os.makedirs(PARENT_MEDIA_NAME)
        print(f"Répertoire {media_use} créé avec succès!")
    
    # Vérifier si le répertoire enfant existe
    child_path = os.path.join(PARENT_MEDIA_NAME, media_use)
    if not os.path.exists(child_path):
        os.makedirs(child_path)
    
    responses = []
    
    if media_use == "reel_medias":
        for file in files:
            file_path = os.path.join(child_path, file.filename)
            with open(file_path, "wb") as video_file:
                video_file.write(file.file.read())
            responses.append(FileResponse(file.filename))
    elif media_use == "product_medias":
        for file in files:
            file_path = os.path.join(child_path, file.filename)
            with open(file_path, "wb") as video_file:
                video_file.write(file.file.read())
            responses.append(FileResponse(file.filename))
    elif media_use == "card_medias":
        for file in files:
            file_path = os.path.join(child_path, file.filename)
            with open(file_path, "wb") as video_file:
                video_file.write(file.file.read())
            responses.append(FileResponse(file.filename))
    elif media_use == "event_multi_medias":
        for file in files:
            file_path = os.path.join(child_path, file.filename)
            with open(file_path, "wb") as video_file:
                video_file.write(file.file.read())
            responses.append(FileResponse(file.filename))
    elif media_use == "anounce_multi_medias":
        for file in files:
            file_path = os.path.join(child_path, file.filename)
            with open(file_path, "wb") as video_file:
                video_file.write(file.file.read())
            responses.append(FileResponse(file.filename))
    elif media_use == "category_site_multi_medias":
        for file in files:
            file_path = os.path.join(child_path, file.filename)
            with open(file_path, "wb") as video_file:
                video_file.write(file.file.read())
            responses.append(FileResponse(file.filename))
    elif media_use == "entertainment_site_multi_medias":
        for file in files:
            file_path = os.path.join(child_path, file.filename)
            with open(file_path, "wb") as video_file:
                video_file.write(file.file.read())
            responses.append(FileResponse(file.filename))
    else :
        raise HTTPException(status_code=403, detail="this file cannot be saved, sorry!")   
    
    return responses


# # renvois une liste de vidéo
# @router.get("/get_video/{video_files:List[str]},{media_use:str}")
# async def get_media_files(video_files: List[str], media_use: str):
#     if media_use != "reel_medias":
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"we don't have media files this media file!")
    
#     child_path = os.path.join(PARENT_MEDIA_NAME, media_use)
    
#     responses = []
#     for video_file in video_files:
#         video_path = os.path.join(child_path, video_file)
#         video_path = os.path.join(child_path, video_file)
#         responses.append(FileResponse(video_path))
      
#     return responses

# renvois une liste de vidéo
@router.get("/get_video/{video_file:str},{media_use:str}")
async def get_media_files(video_file: str, media_use: str):
    if media_use != "reel_medias":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"we don't have media files this media file!")
    
    child_path = os.path.join(PARENT_MEDIA_NAME, media_use)
    video_path = os.path.join(child_path, video_file)
    
    # Vérifiez si la vidéo existe
    # if video_path.is_file():
    if video_path:
        # return FileResponse(video_path, media_type="video/mp4")
        # Renvoyer le fichier vidéo au frontend
        return FileResponse(child_path + video_file)
      
    return {"error": "Vidéo non trouvée"}

@router.get("/get_uploaded_videos/")
async def get_uploaded_videos(media_use: str):
    if media_use not in ["reel_medias"]:
        raise HTTPException(status_code=400, detail="Invalid media_use. Supported values: reel_medias")

    media_path = os.path.join(PARENT_MEDIA_NAME, media_use)

    if not os.path.exists(media_path):
        raise HTTPException(status_code=404, detail=f"No videos found for media_use: {media_use}")

    video_files = [f for f in os.listdir(media_path) if os.path.isfile(os.path.join(media_path, f))]

    if not video_files:
        raise HTTPException(status_code=404, detail=f"No videos found for media_use: {media_use}")

    # return {"videos": video_files}
    print("OK")
    return FileResponse(video_files, media_type="video/mp4")

# Suppression  des vidéos expiré
# def update_attribute(db: Session = Depends(get_db)):
    
#     # Exemple de mise à jour d'une valeur dans la table
#     formated_date = datetime.now()
#     events_queries = db.query(models.Event).filter(models.Event.active == "True").all()
#     for events_querie in events_queries :
#         if events_querie.end_date < formated_date:
#             events_querie.active = "False"
#             db.commit()
#             db.refresh(events_querie)
    
#     db.close()

# # config_sethinguration de l'ordonnanceur
# scheduler = BackgroundScheduler()
# scheduler.add_job(update_attribute, 'interval', hours=1)
# scheduler.start()

# # Tâche pour arrêter l'ordonnanceur lorsque l'application FastAPI se ferme
# def close_scheduler():
#     scheduler.shutdown()

# router.add_event_handler("shutdown", close_scheduler)