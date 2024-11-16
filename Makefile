all:main

client: ./src/client.py
	@echo "executing client script..."
	@python3 ./src/client.py

server: ./src/server.py
	@echo "executing server script..."
	@python3 ./src/server.py

main: ./src/main.py
	@echo "executing main script..."
	@python3 ./src/main.py

run: config build
	@echo "executing run target..."

config: 
	@echo "installing precommit hooks..."
	@pip install pre-commit
	@pre-commit install
	@pre-commit autoupdate
	@pre-commit run --all-files
	@echo "WARNING: these are meant for testing and not to be run in production!"
	@echo "installing dependancies for local development..."
	@pip install pyinstaller

build: ./src/server.py
	@echo "building binary files..."
	@pyinstaller --onefile --distpath ./bin ./src/server.py
