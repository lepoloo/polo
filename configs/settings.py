#infos APPLICATION
PROJECT_NAME="Macro-service polo"
PROJECT_VERSION='1.0.0'

# connection DB parameters
DATABASE_USER = 'postgres'
DATABASE_PASSWORD = 'admin'
DATABASE_HOST = 'localhost'
DATABASE_PORT = 5432
DATABASE_NAME = 'polo_db'

#  configuration messagerie email
smtp_host = "smtp.office365.com"
smtp_port = 587
smtp_username = "eaoudou@bfclimited.com"
smtp_password = "19911021@Esaem"

#  email d'administration
admin_mail = "eaoudou@bfclimited.com"

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 527040 # un an en minutes

PARENT_MEDIA_NAME= "medias"