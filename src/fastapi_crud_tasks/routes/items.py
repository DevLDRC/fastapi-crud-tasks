import uuid
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
async def showAllItems(
    currentUser: Annotated[dict[str, str], Depends(getUserAuthentication)],
    db: Session = Depends(get_db)
):
    return db.query(models.Item).filter(models.Item.user_id == currentUser["sub"]).all()


@route.post("/")
async def createItem(
    currentUser: Annotated[dict[str, str], Depends(getUserAuthentication)],
    item: items.ItemCreate,
    db: Session = Depends(get_db)
):

    itemId = str(uuid.uuid4())

    dbItem = models.Item(
        id=itemId,
        name=item.name,
        description=item.description,
        user_id=currentUser["sub"]
    )
    db.add(dbItem)
    db.commit()
    db.refresh(dbItem)
    return dbItem


@route.get("/{itemId}")
async def showItem(
    currentUser: Annotated[dict[str, str], Depends(getUserAuthentication)],
    itemId: str,
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
async def updateItem(
    currentUser: Annotated[dict[str, str], Depends(getUserAuthentication)],
    itemId: str,
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
async def deleteItem(
    currentUser: Annotated[dict[str, str], Depends(getUserAuthentication)],
    itemId: str,
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
