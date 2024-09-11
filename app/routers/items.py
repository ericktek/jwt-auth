from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas
from app.dependency import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Item, tags=["Items"])
def create_item_for_user(user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_user_item(db=db, item=item, user_id=user_id)

@router.get("/", response_model=list[schemas.Item], tags=["Items"])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
