from typing import Annotated
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi_crud_tasks.routes.auth import getUserAuthentication
from ..dtos import items
from .. import models
from fastapi_crud_tasks.database import get_db

route = APIRouter(
    prefix='/items',
    tags=['items']
)


@route.get("/")
async def showAllItems(currentUser: Annotated[models.User, Depends(getUserAuthentication)], db: Session = Depends(get_db)):
    return currentUser
    # return db.query(models.Item).all()


@route.post("/")
def createItem(item: items.ItemCreate, db: Session = Depends(get_db)):
    dbItem = models.Item(name=item.name, description=item.description)
    db.add(dbItem)
    db.commit()
    db.refresh(dbItem)
    return dbItem


@route.get("/{itemId}")
def showItem(
    itemId: int,
    db: Session = Depends(get_db)
):
    # search item
    dbItem = db.query(models.Item).filter(models.Item.id == itemId).first()

    # Exception to NotFound
    if dbItem is None:
        return {
            "success": False,
            "message": "Item não encontrado"
        }

    return dbItem


@route.put("/{itemId}")
def updateItem(
    itemId: int,
    updatedItem: items.ItemUpdate,
    db: Session = Depends(get_db)
):
    # search item
    dbItem = db.query(models.Item).filter(models.Item.id == itemId).first()

    # Exception to NotFound
    if dbItem is None:
        return {
            "success": False,
            "message": "Item não encontrado"
        }

    # Success to Update!
    dbItem.name = updatedItem.name
    dbItem.description = updatedItem.description

    db.commit()
    db.refresh(dbItem)

    return dbItem


@route.delete("/{itemId}")
def deleteItem(
    itemId: int,
    db: Session = Depends(get_db)
):
    # search item
    dbItem = db.query(models.Item).filter(models.Item.id == itemId).first()

    # Exception to NotFound
    if dbItem is None:
        return {
            "success": False,
            "message": "Item não encontrado"
        }

    db.delete(dbItem)
    db.commit()

    # db.refresh(dbItem)

    return {
        "success": True,
        "message": "Item deletado com sucesso"
    }
