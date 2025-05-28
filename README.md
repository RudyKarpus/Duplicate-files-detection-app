# Duplicate files detection app

## Description

Multithreaded app allowing user to scan folder for finding and deleting duplicated files in it.

## Technology

- 🐍 **Python**  – for high-level logic and threading
- 🦀 **Rust (via PyO3)** – for performance-critical hashing and duplicate detection

## Prerequisites

- [Python](https://www.python.org/downloads/) ( < 13, v12 Recommended)
- [Rust](https://www.rust-lang.org/tools/install) (latest stable version)

## Quick Start
1. **Clone the repository**
   ```bash
   git clone https://github.com/RudyKarpus/Duplicate-files-detection-app.git
   cd Duplicate-files-detection-app
2. **Run**
   - **Windows**:
       ```bash
     .\cmd\windows_run.bat
   - **Linux**:
    ```bash
    chmod +x scripts/run.sh
    ./scripts/run.sh

## Linting and formating
  - [pre-commit](https://pre-commit.com) for automatic coding style verification and formating
  - ***python***: flake8, black, isort
  - ***rust***:  clippy, fmt

### To run
  #### Python
  ```bash
  pip install -r requirements-dev.txt
  pre-commit install
  pre-commit run --all-files
  ```
  #### Rust
  ```bash
  cd model
  cargo fmt
  cargo clippy
  ```
## **To run tests**
   - **Windows**:
     ```bash
     .\cmd\windows_test.bat
     ```
   - **Linux**:
      ```bash
      chmod +x scripts/run.sh
      ./scripts/run.sh
      ```
