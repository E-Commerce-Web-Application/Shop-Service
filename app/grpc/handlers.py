from app.generated.shop.shop_pb2_grpc import ShopServiceServicer
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.services.shop_service import ShopService
from grpc import StatusCode
from grpc.aio import ServicerContext
from app.generated.shop import shop_pb2 as shop_pb
from app.schemas.shop_schemas import ShopCreate


class ShopGrpcService(ShopServiceServicer):
    def __init__(self, session_factory: async_sessionmaker):
        self.session_factory = session_factory

    async def GetAllShops(self, request, context: ServicerContext):
        try:
            async with self.session_factory() as session:
                service = ShopService(session)

                shops = await service.get_all_shops()

                return shops

        except Exception as e:
            await context.abort(
                StatusCode.INTERNAL, details="Error in getting all shops: " + str(e)
            )

    async def GetShop(self, request, context: ServicerContext):
        try:
            async with self.session_factory() as session:
                service = ShopService(session)

                shop = await service.get_shop(request.id)

                if not shop:
                    await context.abort(StatusCode.NOT_FOUND, details="Shop not found!")

                return shop_pb.Shop(
                    id=str(shop.id),
                    name=shop.name,
                    description=shop.description,
                    email=shop.email,
                    phone=shop.phone,
                    location=shop.location,
                    owner_id=shop.owner_id,
                    created_at=shop.created_at,
                    updated_at=shop.updated_at,
                )

        except Exception as e:
            await context.abort(
                StatusCode.INTERNAL, details="Error in getting the shop"
            )

    async def CreateShop(self, request, context: ServicerContext):
        try:
            async with self.session_factory() as session:
                service = ShopService(session)

                shop_data = ShopCreate(
                    name=request.name,
                    description=request.description,
                    email=request.email,
                    phone=request.phone,
                    location=request.location,
                )

                shop = await service.create_shop(shop_data)

                return shop_pb.Shop(
                    id=str(shop.id),
                    name=shop.name,
                    description=shop.description,
                    email=shop.email,
                    phone=shop.phone,
                    location=shop.location,
                    owner_id=shop.owner_id,
                    created_at=shop.created_at,
                    updated_at=shop.updated_at,
                )

        except Exception as e:
            await context.abort(
                StatusCode.INTERNAL, details="Error in creating the shop"
            )

    async def UpdateShop(self, request, context: ServicerContext):
        try:
            async with self.session_factory() as session:
                service = ShopService(session)

                shop = await service.get_shop(request.id)

                if not shop:
                    await context.abort(StatusCode.NOT_FOUND, details="Shop not found!")

                data = shop_pb.ShopUpdate(
                    id=str(request.id),
                    name=request.name,
                    description=request.description,
                    location=request.location,
                    email=request.email,
                    phone=request.password,
                )

                updated_shop = await service.update_shop(data)

                return shop_pb.Shop(
                    id=str(updated_shop.id),
                    name=updated_shop.name,
                    description=updated_shop.description,
                    email=updated_shop.email,
                    phone=updated_shop.phone,
                    location=updated_shop.location,
                    owner_id=updated_shop.owner_id,
                    created_at=updated_shop.created_at,
                    updated_at=updated_shop.updated_at,
                )

        except Exception as e:
            await context.abort(
                StatusCode.INTERNAL, details="Error in updating the shop"
            )

    async def Delete(self, request, context: ServicerContext):
        try:
            async with self.session_factory() as session:
                service = ShopService(session)

                shop = await service.delete_shop(request.id)

                if shop is None:
                    await context.abort(StatusCode.NOT_FOUND, details="Shop not found!")

                return None
        except Exception as e:
            await context.abort(
                StatusCode.INTERNAL, details="Error in deleting the shop"
            )
