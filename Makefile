
.venv:
	python3 -m venv .venv
	./.venv/bin/pip install poetry
	./.venv/bin/poetry install

node_modules:
	cd ./frontend && npm install

clean_proto_out_dir: 
	rm -rf backend/grpc_contracts
	mkdir backend/grpc_contracts

generate_proto: clean_proto_out_dir
	./.venv/bin/python -m grpc_tools.protoc -I protos --python_betterproto_opt=pydantic_dataclasses --python_betterproto_out=backend/grpc_contracts  protos/*


install: .venv node 

clean: 
	rm -rf backend/grpc_contracts/*.py
	rm -rf .venv
	rm -rf ./frontend/node_modules

reload: clean .venv node_modules

all: clean install

.PHONY: reload
.PHONY: node_modules
.PHONY: clean
.PHONY: install 