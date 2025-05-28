@echo off
setlocal

echo [1/4] Creating virtual environment
python -m venv .venv

echo [2/4] Activating virtual environment and installing dependencies
call .venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt

echo [3/4] Building Rust extension with maturin
cd detection_module
maturin build --release
for %%f in (target\wheels\*.whl) do (
    pip install "%%f"
)
cd ..

echo [4/4] Running Python application
python app\main.py %1
