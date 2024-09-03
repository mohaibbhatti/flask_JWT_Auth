import os 
from dotenv import load_dotenv


class Settings:
    def __init__(self):
        load_dotenv()

        self.secret_key = os.environ.get('SECRET_KEY')
        self.jwt_token = os.environ.get('JWT_TOKENT')
        self.database_uri = (
    f"postgresql://{os.getenv('PG_DB_USER')}:{os.getenv('PG_DB_PASSWORD')}@"
    f"{os.getenv('PG_DB_HOST')}:{os.getenv('PG_DB_PORT')}/{os.getenv('PG_DB_NAME')}"
)

settings = Settings()