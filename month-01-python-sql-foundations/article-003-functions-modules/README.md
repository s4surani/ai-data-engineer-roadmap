# Article 3: Python Functions, Modules & Code Organization

## Overview
Professional Python package demonstrating functions, modules, and code organization for data engineering.

## Package Structure

### data_utils/
Reusable utility library for data engineering:
- **validators.py** - Data validation functions
- **calculators.py** - Business calculation functions
- **formatters.py** - Data formatting functions

### tests/
Unit tests for all modules using pytest

### examples/
Demonstration scripts showing package usage

## Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt