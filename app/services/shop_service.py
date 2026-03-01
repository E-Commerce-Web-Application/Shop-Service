from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.models.shop_model import Shop
from sqlalchemy import select
from app.schemas.shop_schemas import ShopCreate, ShopUpdate
from fastapi import Depends
from app.core.database import get_async_session


class ShopService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_shop(self, shop_id: UUID) -> Shop | None:
        return await self.session.get(Shop, shop_id)

    async def get_all_shops(self) -> list[Shop]:
        result = await self.session.execute(select(Shop))

        return result.scalars().all()

    async def create_shop(self, shop_data: ShopCreate) -> Shop:
        new_shop = Shop(
            name=shop_data.name,
            description=shop_data.description,
            email=shop_data.email,
            phone=shop_data.phone,
            location=shop_data.location,
        )

        self.session.add(new_shop)
        await self.session.commit()
        await self.session.refresh(new_shop)

        return new_shop

    async def update_shop(self, id: UUID, shop_data: ShopUpdate) -> Shop | None:
        
        shop = await self.session.get(Shop, id)

        if shop_data.name is not None:
            shop.name = shop_data.name

        if shop_data.description is not None:
            shop.description = shop_data.description

        if shop_data.email is not None:
            shop.email = shop_data.email

        if shop_data.phone is not None:
            shop.phone = shop_data.phone

        if shop_data.location is not None:
            shop.location = shop_data.location

        await self.session.commit()
        await self.session.refresh(shop)

        return shop

    async def delete_shop(self, id: UUID) -> Shop | None:
        shop = await self.session.get(Shop, id)

        if not shop:
            return None

        await self.session.delete(shop)
        await self.session.commit()

        return shop


def get_shop_service(session: AsyncSession = Depends(get_async_session)) -> ShopService:
    return ShopService(session)
