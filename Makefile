proto:
	python -m grpc_tools.protoc \
	-I ./app/protos \
	--python_out=. \
	--grpc_python_out=. \
	./app/protos/*/*.proto