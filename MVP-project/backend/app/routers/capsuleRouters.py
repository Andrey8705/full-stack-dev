from typing import List
from fastapi.responses import JSONResponse
from uuid import UUID
from models.capsuleBaseModel import CapsuleCreate, CapsuleSchema
from database.db_setup import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from models.capsuleBase import Capsule
from fastapi.security import OAuth2PasswordBearer
from functions.mainLogic import verify_acces_token, check_user_role, check_user_and_capsule_user_id, get_current_user


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/capsule/create-capsule/")
def create_capsule(
    capsule: CapsuleCreate, 
    db: Session = Depends(get_db), 
    token: str = Depends(oauth2_scheme)
):
    user_data = verify_acces_token(token)
    create_date_now = datetime.utcnow()

    try:
        open_date = datetime.strptime(capsule.unlock_date, "%Y-%m-%d")
    except ValueError:
        return JSONResponse(
            status_code=400,
            content={"message": "Invalid date format. Use 'YYYY-MM-DD'."}
        )

    if open_date < create_date_now:
        return JSONResponse(
            status_code=422,
            content={"message": "Open date can't be earlier than today."}
        )

    new_capsule = Capsule(
        name=capsule.name,
        create_date=create_date_now,
        unlock_date=open_date,
        message=capsule.message,
        user_id=user_data["id"]
    )

    time_to_open = (new_capsule.unlock_date - new_capsule.create_date).days

    db.add(new_capsule)
    db.commit()
    db.refresh(new_capsule)    

    return JSONResponse(
        status_code=201,
        content={
            "message": f"Capsule '{new_capsule.name}' successfully created.",
            "days_until_open": time_to_open
        }
    )

@router.get("/admin/get/capsule/all", response_model=List[CapsuleSchema])
def get_capsules(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_data = verify_acces_token(token)
    check_user_role(user_data, "admin")

    capsules = db.query(Capsule).all()
    

    return capsules

@router.get("/capsule/capsules/my", response_model=List[CapsuleSchema])
def get_my_capsules(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user_data = get_current_user(token, db)
    user_id = user_data.id
    capsules = db.query(Capsule).filter(Capsule.user_id == user_id).all()
    
    if not capsules:
        raise HTTPException(status_code=404, detail="Капсулы не найдены")

    for capsule in capsules:
        if capsule.unlock_date > datetime.utcnow():
            capsule.message = ""

    return capsules

@router.get("/admin/get/capsule/{id}")
def get_capsule_by_id_admin(id : int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_data =  verify_acces_token(token)
    capsule = db.query(Capsule).filter(Capsule.id == id).first()
    if not capsule:
        return JSONResponse(status_code=404, detail="Capsule not found")
    
    check_user_and_capsule_user_id(user_data["id"], capsule.user_id)

    return JSONResponse(capsule)

@router.get("/capsule/{capsule_id}", response_model=CapsuleSchema)
def get_capsule_by_id(capsule_id: UUID, db: Session = Depends(get_db)):
    capsule = db.query(Capsule).filter(Capsule.id == str(capsule_id)).first()
    if not capsule:
        raise HTTPException(status_code=404, detail="Капсула не найдена")
    
    if capsule.is_public == 0:
       raise HTTPException(status_code=403, detail="Капсула недоступна для просмотра")
    
    if capsule.unlock_date > datetime.utcnow():
        capsule.message = ""

    return capsule


@router.delete("/admin/delete/capsule/{id}")
def delete_capsule(id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_data = verify_acces_token(token)
    check_user_role(user_data, "admin")
    capsule = db.query(Capsule).filter(Capsule.id == id).first()
    if not capsule:
        return JSONResponse(status_code=404, detail="Capsule not found")
    db.delete(capsule)
    db.commit()

    return JSONResponse({"message":f"{capsule["name"]} successfuly deleted"})

@router.put("/admin/edit/capsule/{id}")
def edit_capsule(id: int, capsule_data: CapsuleCreate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_data = verify_acces_token(token)
    check_user_role(user_data, "admin")
    capsule = db.query(Capsule).filter(Capsule.id == id).first()
    if not capsule:
        return JSONResponse(status_code=404, detail="Capsule not found")
    
    capsule.name = capsule_data.name
    capsule.unlock_date = capsule_data.unlock_date
    capsule.message = capsule_data.message
    db.commit()
    return JSONResponse(capsule)