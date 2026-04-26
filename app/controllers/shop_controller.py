from app.services.shop_service import ShopService
from fastapi import HTTPException
from uuid import UUID
from app.schemas.shop_schemas import ShopCreate, ShopUpdate, ShopReviewCreate
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

        products = await shop_service.get_shop_products(id)
        reviews = await shop_service.get_shop_reviews(id)

        return {
            "message": "Shop is fetched successfully",
            "shop": shop,
            "products": products,
            "reviews": reviews,
        }

    except HTTPException:
        raise

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

    except HTTPException:
        raise

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

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Error in deleting the shop: " + str(e)
        )


async def get_shop_products(id: UUID, shop_service: ShopService):
    try:
        result = await shop_service.get_shop_products(id)

        if result is None:
            raise HTTPException(status_code=404, detail=SHOP_NOT_FOUND_MESSAGE)

        if not result.products:
            return {"message": "No products found for this shop", "products": []}

        return {
            "message": f"Products are fetched successfully for the shop {id}",
            "products": result.products,
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Error in finding shop products: " + str(e)
        )


async def create_shop_review(
    shop_review_data: ShopReviewCreate, shop_service: ShopService
):
    try:
        result = await shop_service.create_shop_review(
            shop_id=shop_review_data.shop_id,
            user_id=shop_review_data.user_id,
            rating=shop_review_data.rating,
            comment=shop_review_data.comment,
        )

        if result is None:
            raise HTTPException(status_code=404, detail=SHOP_NOT_FOUND_MESSAGE)

        return {
            "message": "Shop review is created successfully",
            "review": result,
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Error in creating a shop review: " + str(e)
        )


async def get_shop_reviews(id: UUID, shop_service: ShopService):
    try:
        result = await shop_service.get_shop_reviews(id=id)

        if result is None:
            raise HTTPException(status_code=404, detail=SHOP_NOT_FOUND_MESSAGE)

        return {
            "message": "Shop reviewes fetched successfully",
            "reviews": result.reviews,
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Error in getting shop reviews: " + str(e)
        )


async def get_average_shop_rating(id: UUID, shop_service: ShopService):
    try:
        result = await shop_service.get_shop_average_rating(id=id)

        if result is None:
            raise HTTPException(status_code=404, detail=SHOP_NOT_FOUND_MESSAGE)

        return {"message": "Fetched shop average rating successfully", "rating": result}

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Error in getting average shop rating: " + str(e)
        )
