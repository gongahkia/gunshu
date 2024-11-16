all:force

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

force:
	@echo "Forcing rebuild..."

clean: ./bin
	@echo "Cleaning build files..."
	@rm -rf ./bin/
	@rm -rf ./*.spec

build: force
	@echo "building binary files..."
	@pyinstaller --onefile \
		--distpath ./bin \
		--add-data "./src/font/zero_liability_please.ttf:font" \
		--add-data "./src/placeholder_sprite/static.png:placeholder_sprite" \
		--add-data "./src/placeholder_sprite/cursor.png:placeholder_sprite" \
		./src/main.py