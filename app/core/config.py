import os
from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT", 5000))
DB_URL = os.getenv("DB_URL")
GRPC_SERVER_PORT = os.getenv("GRPC_SERVER_PORT", 50051)
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", 50052)
REVIEW_SERVICE_URL = os.getenv("REVIEW_SERVICE_URL",50053)
CART_SERVICE_URL = os.getenv("CART_SERVICE_URL", 50054)