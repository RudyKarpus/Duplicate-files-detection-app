#!/bin/bash

set -e

cd ..

echo "[1/3] Activating virtual environment..."
source .venv/bin/activate

echo "[2/3] Running Python tests..."
python -m unittest discover -s app/tests -p "test_*.py"

echo "[3/3] Running Rust unit tests..."
cd detection_module
cargo test

echo "All tests complete!"
