proto:
	python -m grpc_tools.protoc \
	-I ./app/protos \
	--python_out=./app/generated \
	--grpc_python_out=./app/generated \
	./app/protos/*/*.proto