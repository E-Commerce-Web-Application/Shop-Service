from app.services.shop_service import ShopService
from fastapi import HTTPException
from uuid import UUID
from app.schemas.shop_schemas import ShopCreate, ShopUpdate
from app.constants.messages import SHOP_NOT_FOUND_MESSAGE


async def get_all_shops(shop_service: ShopService):
    try:
        shops = await shop_service.get_all_shops()

        return {"message": "Fetched all shops successfully", "shops": shops}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Error occurred in getting all shops : " + str(e)
        )


async def get_shop(id: UUID, shop_service: ShopService):
    try:
        shop = await shop_service.get_shop(id)

        if not shop:
            raise HTTPException(status_code=404, detail=SHOP_NOT_FOUND_MESSAGE)

        return shop

    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Error in finding the shop: " + str(e)
        )


async def create_shop(data: ShopCreate, shop_service: ShopService):
    try:
        shop = await shop_service.create_shop(data)

        return {"message": "Shop is created successfully", "shop": shop}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Error in creating the shop: " + str(e)
        )


async def update_shop(id: UUID, data: ShopUpdate, shop_service: ShopService):
    try:
        shop = await shop_service.update_shop(id, data)

        if not shop:
            raise HTTPException(status_code=404, detail=SHOP_NOT_FOUND_MESSAGE)

        return {"message": "Shop is updated successfully", "shop": shop}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Error in updating the shop: " + str(e)
        )


async def delete_shop(id: UUID, shop_service: ShopService):
    try:
        result = await shop_service.delete_shop(id)

        if not result:
            raise HTTPException(status_code=404, detail=SHOP_NOT_FOUND_MESSAGE)

        return {"message": "Shop is deleted successfully"}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Error in deleting the shop: " + str(e)
        )
