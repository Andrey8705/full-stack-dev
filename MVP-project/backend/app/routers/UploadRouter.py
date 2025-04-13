from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import hashlib
from uuid import uuid4
from fastapi.security import OAuth2PasswordBearer
from database.db_setup import get_db
from sqlalchemy.orm import Session
from functions.mainLogic import verify_acces_token
from models.userBase import User
from functions.mainLogic import get_current_user
import shutil

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...),token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Проверка типа файла (например, только изображения)
    payload = verify_acces_token(token)
    user_id = payload.get("id")

    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Только изображения разрешены")

    # Уникальное имя файла
    ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid4()}{ext}{user_id}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    # Сохраняем файл
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return JSONResponse(content={"filename": unique_filename, "url": f"/{UPLOAD_DIR}/{unique_filename}"})

@router.post("/upload-avatar")
async def upload_avatar(file: UploadFile = File(...),token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    payload = verify_acces_token(token)
    user_id = payload.get("id")
    # Загрузка файла (аналогично примеру выше)
    ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid4()}{ext}"
    file_path = os.path.join("uploads", unique_filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Сохраняем путь в БД
    user = db.query(User).filter(User.id == user_id).first()
    user.avatar_url = f"/uploads/{unique_filename}"
    db.commit()

    return {"avatar_url": user.avatar_url}

@router.post("/capsules/{capsule_id}/upload")
async def upload_file_to_capsule(
    capsule_id: int,
    file: UploadFile = File(...),
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Сохраняем файл
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Хэшируем содержимое
    with open(file_path, "rb") as f:
        file_bytes = f.read()
        file_hash = hashlib.sha256(file_bytes).hexdigest()

    # Можно сохранить hash и путь в БД
    # Например:
    # db.add(Attachment(capsule_id=capsule_id, path=file_path, hash=file_hash))

    return JSONResponse({
        "filename": file.filename,
        "hash": file_hash
    })
