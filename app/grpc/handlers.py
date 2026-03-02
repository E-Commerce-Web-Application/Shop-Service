from app.generated.shop.shop_pb2_grpc import ShopServiceServicer
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.services.shop_service import ShopService
from grpc import StatusCode
from grpc.aio import ServicerContext
from app.generated.shop import shop_pb2 as shop_pb
from app.schemas.shop_schemas import ShopCreate, ShopUpdate
from uuid import UUID


class ShopGrpcService(ShopServiceServicer):
    def __init__(self, session_factory: async_sessionmaker):
        self.session_factory = session_factory

    async def GetAllShops(self, request, context: ServicerContext):
        try:
            async with self.session_factory() as session:
                service = ShopService(session)

                shops = await service.get_all_shops()

                return shop_pb.Shops(
                    shops=[
                        shop_pb.Shop(
                            id=str(shop.id),
                            name=shop.name,
                            description=shop.description,
                            location=shop.location,
                            email=shop.email,
                            phone=shop.phone,
                            owner_id=str(shop.owner_id),
                            created_at=shop.created_at,
                            updated_at=shop.updated_at,
                        )
                        for shop in shops
                    ]
                )

        except Exception as e:
            await context.abort(
                StatusCode.INTERNAL, details="Error in getting all shops: " + str(e)
            )

    async def GetShop(self, request, context: ServicerContext):
        try:
            async with self.session_factory() as session:
                service = ShopService(session)

                shop = await service.get_shop(UUID(request.id))

                if not shop:
                    await context.abort(StatusCode.NOT_FOUND, details="Shop not found!")

                return shop_pb.Shop(
                    id=str(shop.id),
                    name=shop.name,
                    description=shop.description,
                    email=shop.email,
                    phone=shop.phone,
                    location=shop.location,
                    owner_id=str(shop.owner_id),
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
                    owner_id=request.owner_id,
                )

                shop = await service.create_shop(shop_data)

                return shop_pb.Shop(
                    id=str(shop.id),
                    name=shop.name,
                    description=shop.description,
                    email=shop.email,
                    phone=shop.phone,
                    location=shop.location,
                    owner_id=str(shop.owner_id),
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

                data = ShopUpdate(
                    id=UUID(request.id),
                    name=request.name.value if request.HasField("name") else None,
                    description=(
                        request.description.value
                        if request.HasField("description")
                        else None
                    ),
                    location=(
                        request.location.value if request.HasField("location") else None
                    ),
                    email=request.email.value if request.HasField("email") else None,
                    phone=request.phone.value if request.HasField("phone") else None,
                )

                updated_shop = await service.update_shop(
                    id=UUID(request.id), shop_data=data
                )

                return shop_pb.Shop(
                    id=str(updated_shop.id),
                    name=updated_shop.name,
                    description=updated_shop.description,
                    email=updated_shop.email,
                    phone=updated_shop.phone,
                    location=updated_shop.location,
                    owner_id=str(updated_shop.owner_id),
                    created_at=updated_shop.created_at,
                    updated_at=updated_shop.updated_at,
                )

        except Exception as e:
            await context.abort(
                StatusCode.INTERNAL, details="Error in updating the shop! : " + str(e)
            )

    async def Delete(self, request, context: ServicerContext):
        try:
            async with self.session_factory() as session:
                service = ShopService(session)

                shop = await service.delete_shop(UUID(request.id))

                if shop is None:
                    await context.abort(StatusCode.NOT_FOUND, details="Shop not found!")

                return None
        except Exception as e:
            await context.abort(
                StatusCode.INTERNAL, details="Error in deleting the shop"
            )
