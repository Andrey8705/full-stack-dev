from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from routers import capsuleRouters, userRouters
from database.db_setup import create_db
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers import UploadRouter

load_dotenv()

app = FastAPI()

@app.on_event("startup")
def startup():
    create_db()

app.include_router(userRouters.router, prefix="/api", tags=["Users"])
app.include_router(capsuleRouters.router, prefix="/api", tags=["Capsule"])
app.include_router(UploadRouter.router, prefix="/api", tags=["Upload"])
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Можно ограничить определенные источники, например, ['http://localhost:3000']
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
