# Installation Guide - Python Version Compatibility

## ⚠️ Python Version Issue

If you're using **Python 3.13**, you may encounter build errors with older package versions. This guide provides solutions.

## Solution 1: Use Python 3.11 or 3.12 (Recommended)

The easiest solution is to use Python 3.11 or 3.12, which have better package compatibility:

```bash
# Check your Python version
python3 --version

# If you have Python 3.13, install Python 3.12 or 3.11
# On macOS with Homebrew:
brew install python@3.12

# Create venv with specific Python version
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Solution 2: Update Requirements for Python 3.13

If you must use Python 3.13, use the updated requirements:

```bash
# Use the Python 3.13 compatible requirements
pip install -r requirements-py313.txt
```

Or manually install with updated versions:

```bash
pip install fastapi>=0.115.0 uvicorn[standard]>=0.32.0 pydantic>=2.10.0 openai>=1.54.0 python-multipart>=0.0.12 jinja2>=3.1.5 requests>=2.32.0
```

## Solution 3: Use Latest Versions (No Pinning)

For maximum compatibility, install without version pinning:

```bash
pip install fastapi uvicorn[standard] pydantic openai python-multipart jinja2 requests
```

## Quick Fix for Current Error

If you're seeing the `pydantic-core` build error:

```bash
# Option A: Use Python 3.12
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Option B: Upgrade pydantic
pip install --upgrade pydantic>=2.10.0
pip install -r requirements.txt
```

## Verify Installation

After installing, verify everything works:

```bash
python -c "import fastapi, pydantic, openai; print('✅ All packages installed successfully')"
```

## Troubleshooting

### Error: "Failed building wheel for pydantic-core"
- **Cause**: Python 3.13 compatibility issue
- **Fix**: Use Python 3.11/3.12 or upgrade pydantic to >=2.10.0

### Error: "No module named 'fastapi'"
- **Cause**: Virtual environment not activated
- **Fix**: `source venv/bin/activate`

### Error: "pip: command not found"
- **Cause**: pip not installed
- **Fix**: `python3 -m ensurepip --upgrade`

---

**Recommended**: Use Python 3.12 for best compatibility with all packages.
