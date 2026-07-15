.PHONY: setup setup-backend setup-frontend \
	dev dev-backend dev-frontend \
	check test lint clean

PYTHON ?= python

BACKEND_DIR := backend
FRONTEND_DIR := frontend
VENV_DIR := $(BACKEND_DIR)/venv
VENV_PYTHON := $(VENV_DIR)/bin/python

setup: setup-backend setup-frontend

setup-backend:
	cd $(BACKEND_DIR) && $(PYTHON) -m venv venv
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PYTHON) -m pip install -r $(BACKEND_DIR)/requirements.txt

setup-frontend:
	cd $(FRONTEND_DIR) && npm install

dev:
	@echo "Run in separate terminals:"
	@echo "  make dev-backend"
	@echo "  make dev-frontend"

dev-backend:
	$(VENV_PYTHON) -m uvicorn app.main:app --reload --app-dir $(BACKEND_DIR)

dev-frontend:
	cd $(FRONTEND_DIR) && npm run dev

check:
	$(MAKE) lint
	$(MAKE) test

lint:
	@echo "Lint tools are not configured yet."

test:
	@echo "Test frameworks are not configured yet."

clean:
	rm -rf $(VENV_DIR)
	rm -rf $(FRONTEND_DIR)/node_modules $(FRONTEND_DIR)/dist
	find $(BACKEND_DIR) -type d -name __pycache__ -prune -exec rm -rf {} +
	find $(BACKEND_DIR) -type f -name '*.pyc' -delete