
import os

from fastapi import Depends, HTTPException, status

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from dotenv import load_dotenv
from configs.settings import smtp_host, smtp_port, smtp_username, smtp_password # autre
load_dotenv('.env')

# fetch les données
# @app.get("/fetch")
# async def fetch_data():
#     async with httpx.AsyncClient() as client:
#         response = await client.get("https://api.example.com/endpoint")
#         return response.json()

from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hsher Password
def hash(password: str):
    return pwd_context.hash(password)

# Verify token
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# send mail
class Envs:
    smtp_host_sys = smtp_host
    smtp_port_sys = smtp_port
    smtp_username_sys = smtp_username
    smtp_password_sys = smtp_password

def send_email(to_email: str, subject: str, content: str):
    # Paramètres d'authentification du serveur SMTP
    smtp_host = Envs.smtp_host_sys
    smtp_port = Envs.smtp_port_sys
    smtp_username = Envs.smtp_username_sys
    smtp_password = Envs.smtp_password_sys

    # Création de l'objet du message e-mail
    msg = MIMEMultipart()
    msg["From"] = smtp_username
    msg["To"] = to_email
    msg["Subject"] = subject

    # Ajout du contenu du message
    msg.attach(MIMEText(content, "plain"))

    # Connexion au serveur SMTP et envoi de l'e-mail
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)