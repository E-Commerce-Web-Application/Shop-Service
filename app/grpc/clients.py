from app.core.config import PRODUCT_SERVICE_URL, REVIEW_SERVICE_URL, CART_SERVICE_URL
import grpc
from app.generated.product import product_pb2_grpc
from app.generated.review import review_pb2_grpc
from app.generated.cart import cart_pb2_grpc

product_channel = grpc.aio.insecure_channel(PRODUCT_SERVICE_URL)
product_stub = product_pb2_grpc.ProductServiceStub(product_channel)

review_channel = grpc.aio.insecure_channel(REVIEW_SERVICE_URL)
review_stub = review_pb2_grpc.ReviewServiceStub(review_channel)

cart_channel = grpc.aio.insecure_channel(CART_SERVICE_URL)
cart_stub = cart_pb2_grpc.CartServiceStub(cart_channel)
