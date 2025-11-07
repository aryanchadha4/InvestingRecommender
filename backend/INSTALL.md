# Installation Instructions

## Step 1: Install Dependencies

Navigate to the backend directory and install the package:

```bash
cd backend
pip install -e .
```

This will install all dependencies including:
- `yfinance>=0.2.43` - Market data provider
- `transformers>=4.44` - HuggingFace transformers for FinBERT
- `torch>=2.4` - PyTorch (CPU version, platform-specific)
- `beautifulsoup4>=4.12` - HTML parsing for news
- And all other dependencies

## Step 2: Download NLTK Data

Download the VADER lexicon for sentiment analysis:

```bash
python -m nltk.downloader vader_lexicon
```

Or use the provided script:

```bash
python download_nltk_data.py
```

## Step 3: Verify Installation

Check that all dependencies are installed:

```bash
python -c "import yfinance, transformers, torch, bs4, nltk; print('✅ All dependencies installed')"
```

## Platform-Specific Notes

### PyTorch Installation

The `pyproject.toml` includes platform-specific torch installations:
- **Apple Silicon (M1/M2/M3) Macs**: Automatically installs the ARM64 version
- **Intel Macs / Linux / Windows**: Automatically installs the CPU version

The installer will automatically select the correct version based on your platform.

### FinBERT Model

The FinBERT model will automatically download on first use (~500MB). Make sure you have:
- Internet connection for first download
- ~1GB free disk space
- Patience for the first download (may take a few minutes)

## Troubleshooting

### If torch installation fails:

Try installing torch separately:

```bash
# For Apple Silicon Macs
pip install torch --index-url https://download.pytorch.org/whl/cpu

# For other platforms
pip install torch
```

### If NLTK download fails:

Manually download the data:

```python
import nltk
nltk.download('vader_lexicon', download_dir='~/nltk_data')
```

### If transformers installation is slow:

The transformers library may take a while to install due to its size. Be patient!

## Development Installation

For development with additional tools:

```bash
pip install -e ".[dev]"
```

This includes:
- `pytest` - Testing framework
- `ruff` - Code formatting and linting
- `mypy` - Type checking

