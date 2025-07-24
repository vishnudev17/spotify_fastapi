import uuid
import bcrypt
from database import get_db
from fastapi import HTTPException, Depends
from middleware.auth_middleware import auth_middleware 
from models.user import User
from pydantic_schemas.user_create import UserCreate
from fastapi import APIRouter
from sqlalchemy.orm import Session
import jwt

from pydantic_schemas.user_login import UserLogin

router = APIRouter()


@router.post("/signup", status_code=201)
def signup_user(user: UserCreate, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.email == user.email).all()

    if user_db:
        raise HTTPException(400, "User with the same email already exists")

    hashed_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())

    user_db = User(
        id=str(uuid.uuid4()), email=user.email, password=hashed_pw, name=user.name
    )

    db.add(user_db)
    db.commit()

    return user_db


@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.email == user.email).first()

    if not user_db:
        raise HTTPException(400, "User with this email doesn't exists")

    isMatchPassword = bcrypt.checkpw(user.password.encode(), user_db.password)

    if not isMatchPassword:
        raise HTTPException(400, "Incorrect Password")
    token = jwt.encode({"id": user_db.id}, "password_key")

    return {"token": token, "user": user_db}


@router.get("/")
def current_user(db: Session = Depends(get_db), user_dict=Depends(auth_middleware)):

    user = db.query(User).filter(User.id == user_dict["uid"]).first()
    if not user:
        raise HTTPException(401, "User not found")
    

    return user
