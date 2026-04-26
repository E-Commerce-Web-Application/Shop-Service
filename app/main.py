from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.routes import shop_routes
from app.grpc.server import GrpcServer

grpc_server = GrpcServer()


@asynccontextmanager
async def lifespan(app: FastAPI):

    await grpc_server.start()
    yield
    await grpc_server.stop()


app = FastAPI(lifespan=lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(shop_routes.router)


@app.get("/shops")
async def root():
    return {"message": "Shop service is active"}


@app.get("/health")
async def health():
    return {"message": "Shop service is running..."}
