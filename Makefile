.PHONY: help install setup run pipeline collect preprocess train visualize test clean

help:
	@echo "Air Quality Prediction System - Make Commands"
	@echo ""
	@echo "Usage:"
	@echo "  make install      - Install dependencies"
	@echo "  make setup        - Setup environment and directories"
	@echo "  make pipeline     - Run full pipeline (data + train + viz)"
	@echo "  make quick        - Run quick pipeline (skip LSTM)"
	@echo "  make collect      - Collect data only"
	@echo "  make preprocess   - Preprocess data only"
	@echo "  make train        - Train models only"
	@echo "  make visualize    - Create visualizations only"
	@echo "  make run          - Run web application"
	@echo "  make test         - Run tests"
	@echo "  make clean        - Clean generated files"
	@echo "  make clean-all    - Clean everything including data"

install:
	@echo "Installing dependencies..."
	pip install --upgrade pip
	pip install -r requirements.txt
	@echo "✓ Installation completed"

setup:
	@echo "Setting up environment..."
	mkdir -p data models static notebooks
	cp .env.example .env 2>/dev/null || true
	@echo "✓ Setup completed"

pipeline:
	@echo "Running full pipeline..."
	python run_pipeline.py --all

quick:
	@echo "Running quick pipeline (skip LSTM)..."
	python run_pipeline.py --all --skip-lstm

collect:
	@echo "Collecting data..."
	python src/data_collection.py

preprocess:
	@echo "Preprocessing data..."
	python src/preprocessing.py

train:
	@echo "Training models..."
	python src/model_training.py

visualize:
	@echo "Creating visualizations..."
	python src/visualization.py

run:
	@echo "Starting web application..."
	@echo "Open http://localhost:5000 in your browser"
	python app.py

test:
	@echo "Running tests..."
	python -m pytest tests/ -v

clean:
	@echo "Cleaning generated files..."
	rm -f models/*.pkl models/*.h5 models/*.json models/*.png
	rm -f static/*.html static/*.json
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "✓ Cleaned"

clean-all: clean
	@echo "Cleaning all data..."
	rm -f data/*.csv
	@echo "✓ All cleaned"

dev:
	@echo "Starting development server..."
	FLASK_ENV=development FLASK_DEBUG=1 python app.py

prod:
	@echo "Starting production server with Gunicorn..."
	gunicorn -w 4 -b 0.0.0.0:5000 app:app

notebook:
	@echo "Starting Jupyter notebook..."
	jupyter notebook notebooks/

requirements:
	@echo "Freezing requirements..."
	pip freeze > requirements.txt
	@echo "✓ Requirements updated"

check:
	@echo "Checking installation..."
	python -c "import pandas, numpy, sklearn, tensorflow, flask; print('✓ All packages OK')"
	@echo "Python version:"
	python --version
