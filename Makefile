.DEFAULT_GOAL:=help
.PHONY: help
help:  ## Display this help
	$(info Example Makefile for my blog post)
	awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z0-9_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
.PHONY: build
build: ## Build container images
		docker-compose -f docker-compose.yaml build
.PHONY: up
up: ## Build and start containers
		docker-compose -f docker-compose.yaml up -d
.PHONY: start
start: ## Start containers
		docker-compose -f docker-compose.yaml start
.PHONY: down
down: ## Stop containers
		docker-compose -f docker-compose.yaml down
.PHONY: destroy
destroy: ## Destroy containers
		docker-compose -f docker-compose.yaml down -v
.PHONY: stop
stop: ## Stop containers
		docker-compose -f docker-compose.yaml stop
.PHONY: restart
restart: ## Restart containers
		docker-compose -f docker-compose.yaml stop
		docker-compose -f docker-compose.yaml up -d
.PHONY: logs
logs: ## View Events API logs
		docker-compose -f docker-compose.yaml logs --tail=100 -f events-api
.PHONY: ps
ps: ## List running containers
		docker-compose -f docker-compose.yaml ps
.PHONY: test
test: ## Run API tests
		hurl events-api.hurl

$(VERBOSE).SILENT:
