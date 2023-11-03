
import os
from fastapi import APIRouter, HTTPException, Depends, Response, status,File, UploadFile, Request
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, get_db
from app.schemas import users_schemas
from app.models import models as models
from  utils import oauth2

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=users_schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(
        models.User.username == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not oauth2.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}

# Endpoint de déconnexion
@router.post("/logout")
async def logout(request: Request, current_user : str = Depends(oauth2.get_current_user)):
    
    headers = dict(request.headers)  # Convertir les headers en dict pour pouvoir les modifier
    print(headers)
    
    if "Authorization" in headers:
        del headers["Authorization"]  # Supprimer la clé "Authorization" du dict des headers
        
    token = request.headers.get("Authorization")  # Vérifier que le token a été supprimé
    print(token)
    
    if token is not None:
        return {"error": "Invalid token"}

    return {"message": "User successfully logged out"}
