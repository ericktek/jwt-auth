from datetime import timedelta
from fastapi import APIRouter, Depends, status, HTTPException
from app.utils import security
from app import models, schemas
from app.dependency import get_db
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.utils import token

router = APIRouter()

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    # Query the user from the database
    user = db.query(models.User).filter(models.User.email == request.username, models.User.is_active).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found or inactive")
    
    # Verify the password
    if not security.verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    
    # Create access token
    access_token = token.create_access_token(data={"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}
