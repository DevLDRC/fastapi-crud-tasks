from datetime import datetime, timedelta, timezone
from turtle import st
from typing import Annotated
from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..dtos import users, auth
from .. import models
from fastapi_crud_tasks.database import get_db
from pwdlib import PasswordHash
import jwt
import os
from dotenv import load_dotenv

route = APIRouter(
    prefix='/auth',
    tags=['auth']
)

load_dotenv()

passwordHash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def getUserAuthentication(token: Annotated[str, Depends(oauth2_scheme)]):

    secretKey = os.getenv("SECRET_SIGNATURE")

    try:
        payload = jwt.decode(token, secretKey, algorithms="HS256")
        userCredentials = payload.get('user')
    except jwt.InvalidTokenError:
        return {
            "401": "Não autorizado"
        }

    return userCredentials


@route.post("/register")
def createUser(user: users.UserCreate, db: Session = Depends(get_db)):

    userExists = db.query(models.User).filter(
        models.User.email == user.email).first()
    if userExists:
        return {
            "409": "Email ja cadastrado"
        }

    userPasswordHashed = passwordHash.hash(user.password)
    dbUser = models.User(
        name=user.name,
        email=user.email,
        password=userPasswordHashed
    )
    db.add(dbUser)
    db.commit()
    db.refresh(dbUser)
    return dbUser


@route.post("/login")
def LoginUser(user: auth.UserLogin, db: Session = Depends(get_db)):

    userCredentials = db.query(models.User).filter(
        models.User.email == user.email).first()

    # print("userCredentials:", userCredentials)
    if userCredentials is None:
        return {
            "404": "Usuario não encontrado"
        }

    checkPassword = passwordHash.verify(
        user.password, userCredentials.password)

    if checkPassword is False:
        return {
            "401": "Não autorizado"
        }

    secretKey = os.getenv("SECRET_SIGNATURE")

    expireToken = datetime.now(timezone.utc) + timedelta(seconds=30)

    userEncodePayload = {
        "sub": str(userCredentials.id),
        "user": {
            "name": userCredentials.name,
            "email": user.email
        },
        "exp": expireToken
    }

    token = jwt.encode(userEncodePayload, secretKey, algorithm="HS256")

    return {
        "token": token
    }
