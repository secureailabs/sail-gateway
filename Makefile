.PHONY: clean sail_client build_image

install:
	@./build/dev_setup.sh

run:
	@uvicorn dns-server.dns_crud:app --reload

build_image:
	@./scripts.sh build_image gateway

push_image: build_image
	@./scripts.sh push_image_to_registry gateway

generate_client:
	@./scripts.sh generate_client
