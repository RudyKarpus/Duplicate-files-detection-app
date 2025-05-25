@echo off
setlocal

cd ..
echo [1/2] Running Python tests...
python -m pytest app/tests

echo [2/2] Running Rust unit tests...
cd detection_module
cargo test

echo All tests complete!