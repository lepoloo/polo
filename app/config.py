import os
# from dotenv import load_dotenv
# load_dotenv()



# nom de projet
project_name: str = os.getenv("PROJECT_NAME", "POLO")
project_version: str = os.getenv("PROJECT_VERSION", "1.0.0")
debug: str = os.getenv("DEBUG", "True")
# connexion DB
database_username: str = os.getenv("DATABASE_USER")
database_password: str = os.getenv("DATABASE_PASSWORD")
database_hostname: str = os.getenv("DATABASE_HOST")
database_port: int = int(os.getenv("DATABASE_PORT"))
database_name: str = os.getenv("DATABASE_NAME")
# configuration de sécurité
secret_key: str = os.getenv("SECRET_KEY")
algorithm: str = os.getenv("ALGORITHM")
access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
# configuration mail
smtp_host: str = os.getenv("SMTP_HOST")
smtp_port:int = int(os.getenv("SMTP_PORT"))
smtp_username: str = os.getenv("SMTP_USERNAME")
smtp_password: str = os.getenv("SMTP_PASSWORD")
admin_mail: str = os.getenv("ADMIN_MAIL")
# configuration fichier média
parent_media_name: str = os.getenv("PARENT_MEDIA_NAME")

