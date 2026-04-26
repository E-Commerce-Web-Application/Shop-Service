from fastapi import APIRouter, Depends
from app.services.shop_service import ShopService, get_shop_service
from app.schemas.shop_schemas import ShopCreate, ShopUpdate, ShopReviewCreate
from app.controllers import shop_controller
from typing import Annotated
from uuid import UUID

router = APIRouter(prefix="/shops", tags=["Shops"])


@router.get("/")
async def get_all_shops(
    shop_service: Annotated[ShopService, Depends(get_shop_service)],
):
    return await shop_controller.get_all_shops(shop_service)


@router.get("/{id}")
async def get_shop(
    id: UUID, shop_service: Annotated[ShopService, Depends(get_shop_service)]
):
    return await shop_controller.get_shop(id, shop_service)


@router.post("/")
async def create_shop(
    data: ShopCreate, shop_service: Annotated[ShopService, Depends(get_shop_service)]
):
    return await shop_controller.create_shop(data, shop_service)


@router.patch("/{id}")
async def update_shop(
    id: UUID,
    data: ShopUpdate,
    shop_service: Annotated[ShopService, Depends(get_shop_service)],
):
    return await shop_controller.update_shop(id, data, shop_service)


@router.delete("/{id}")
async def delete_shop(
    id: UUID, shop_service: Annotated[ShopService, Depends(get_shop_service)]
):
    return await shop_controller.delete_shop(id, shop_service)


@router.post("/reviews")
async def create_shop_review(
    shop_review_data: ShopReviewCreate,
    shop_service: Annotated[ShopService, Depends(get_shop_service)],
):
    return await shop_controller.create_shop_review(
        shop_review_data=shop_review_data, shop_service=shop_service
    )


@router.get("/reviews/{id}")
async def get_shop_reviews(
    id: UUID,
    shop_service: Annotated[ShopService, Depends(get_shop_service)],
):
    return await shop_controller.get_shop_reviews(id, shop_service)


@router.get("/reviews/avg/{id}")
async def get_shop_avg_rating(
    id: UUID,
    shop_service: Annotated[ShopService, Depends(get_shop_service)],
):
    return await shop_controller.get_average_shop_rating(id, shop_service)
