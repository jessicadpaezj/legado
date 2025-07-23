import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    POSTGRES_DB             = os.getenv("POSTGRES_DB", "postgres")
    POSTGRES_USER           = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD       = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_HOST           = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT           = os.getenv("POSTGRES_PORT", "5432")
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "nRvyYC4soFxBdZ-F-5Nnzz5USXstR1YylsTd-mA0aKtI9HUlriGrtkf-TiuDapkLiUCogO3JOK7kwZisrHp6wA")
    JWT_ALGORITHM = "HS512"
