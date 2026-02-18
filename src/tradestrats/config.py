from pathlib import Path

# Project root (two levels up from this file: src/tradestrats/config.py -> project root)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Default data directory for Parquet caching
DATA_DIR = PROJECT_ROOT / "data"

# Default exchange
DEFAULT_EXCHANGE = "binance"

# Available timeframes (most common)
TIMEFRAMES = ["1m", "5m", "15m", "1h", "4h", "1d"]

# Default timeframe
DEFAULT_TIMEFRAME = "1h"

# Default trading pair
DEFAULT_SYMBOL = "BTC/USDT"
