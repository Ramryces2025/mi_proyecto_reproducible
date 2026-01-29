.PHONY: help data train install clean

help:
	@echo "Commands:"
	@echo "  make data   - show expected data location"
	@echo "  make train  - train model using default paths"
	@echo "  make install - install dependencies from requirements.txt"
	@echo "  make clean  - remove model artifacts"

data:
	@if not exist data\raw\data_export.csv ( \
		echo "Missing dataset: data/raw/data_export.csv" & exit 1 \
	) else ( \
		echo "Dataset OK: data/raw/data_export.csv" \
	)

train:
	python src/train.py

install:
	pip install -r requirements.txt

clean:
	@echo "Removing models/*.pkl"
	@del /Q models\*.pkl 2>NUL || exit 0
