from fastapi import APIRouter, Depends
from app.services.shop_service import ShopService, get_shop_service
from app.schemas.shop_schemas import ShopRead, ShopCreate, ShopUpdate
from app.controllers import shop_controller
from typing import Annotated

router = APIRouter(prefix="/shops", tags=["Shops"])


@router.get("/")
async def get_all_shops(
    shop_service: Annotated[ShopService, Depends(get_shop_service)],
):
    return await shop_controller.get_all_shops(shop_service)


@router.get("/{id}", response_model=ShopRead)
async def get_shop(
    id: str, shop_service: Annotated[ShopService, Depends(get_shop_service)]
):
    return await shop_controller.get_shop(id, shop_service)


@router.post("/")
async def create_shop(
    data: ShopCreate, shop_service: Annotated[ShopService, Depends(get_shop_service)]
):
    return await shop_controller.create_shop(data, shop_service)


@router.patch("/{id}")
async def update_shop(
    id: str,
    data: ShopUpdate,
    shop_service: Annotated[ShopService, Depends(get_shop_service)],
):
    return await shop_controller.update_shop(id, data, shop_service)


@router.delete("/{id}")
async def delete_shop(
    id: str, shop_service: Annotated[ShopService, Depends(get_shop_service)]
):
    return await shop_controller.delete_shop(id, shop_service)
