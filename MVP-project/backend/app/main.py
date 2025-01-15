from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from routers import capsuleRouters, userRouters
from database.db_setup import create_engine, engine
from models.base import Base


load_dotenv()

app = FastAPI()

DATABASE_URL = "sqlite:///./database.db"
#create_engine(DATABASE_URL)
#Base.metadata.create_all(bind= engine)

app.include_router(userRouters.router, prefix="/api", tags=["Users"])
app.include_router(capsuleRouters.router, prefix="/api", tags=["Capsule"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
