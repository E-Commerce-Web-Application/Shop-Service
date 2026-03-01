import grpc
from app.generated.shop import shop_pb2_grpc
from app.grpc.handlers import ShopGrpcService
from app.core.database import async_session_maker


class GrpcServer:
    def __init__(self):
        self.server = grpc.aio.server()

        shop_pb2_grpc.add_ShopServiceServicer_to_server(
            ShopGrpcService(async_session_maker),
            self.server
        )

        self.server.add_insecure_port("[::]:50051")

    async def start(self):
        await self.server.start()
        print("gRPC server is started...")

    async def stop(self):
        await self.server.stop()
        print("gRPC server is stopped.")
