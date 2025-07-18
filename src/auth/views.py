# src/auth/router.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import schemas, crud, security, models, deps
from src.database.providers import provide_async_session

router = APIRouter()

@router.post("/register", response_model=schemas.UserPublic)
def register_user(
    user: schemas.UserCreate, 
    db: Session = Depends(provide_async_session)
):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@router.post("/login", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(provide_async_session)
):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = security.create_access_token(
        data={"sub": user.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=schemas.UserPublic)
def read_users_me(current_user: models.User = Depends(deps.get_current_user)):
    return current_user