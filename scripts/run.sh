#!/bin/bash

set -e

echo "[1/4] Creating virtual environment"
python3 -m venv .venv

echo "[2/4] Activating virtual environment and installing dependencies"
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "[3/4] Building Rust extension with maturin"
cd detection_module
maturin build --release

for whl in target/wheels/*.whl; do
    pip install "$whl"
done
cd ..

echo "[4/4] Running Python application"
python app/main.py "$1"
