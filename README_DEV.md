Here’s a clean **Developer README (Build Guide)** you can copy directly:

---

# 🧱 Developer Build Guide — `ai-watchdog`

This document explains how to build, package, and test the **ai-watchdog** library locally before publishing.

---

## 📦 1. Setup Environment

```bash
# Clone the repo
git clone https://github.com/vivekx01/ai-watchdog.git
cd ai-watchdog

# Create and activate a virtual environment
pip install pipenv
pipenv shell

# install the dependencies
pip install -r requirements.txt

# Install build tools
pip install --upgrade build twine setuptools wheel
```

---

## 🏗️ 2. Build the Package

```bash
# Clean previous builds (optional but recommended)
rm -rf dist build *.egg-info

# Build the source and wheel distributions
python -m build
```

✅ This creates two files inside the `dist/` directory:

* `ai_watchdog-<version>-py3-none-any.whl`
* `ai_watchdog-<version>.tar.gz`

---

## 🧪 4. Test Local Installation

```bash
# Install locally built package
pip install dist/ai_watchdog-<version>-py3-none-any.whl

# Run quick import test
python -c "from ai_watchdog.core import InputWatchdog; print('✅ ai-watchdog imported successfully!')"
```

---
