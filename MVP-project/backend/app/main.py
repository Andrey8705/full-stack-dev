from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from routers import capsuleRouters, userRouters
from database.db_setup import create_db


load_dotenv()

app = FastAPI()

@app.on_event("startup")
def startup():
    create_db()

app.include_router(userRouters.router, prefix="/api", tags=["Users"])
app.include_router(capsuleRouters.router, prefix="/api", tags=["Capsule"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
