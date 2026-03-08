"""
Automation Test Framework — Centralized Logger
Usage:
    from core.logger import get_logger
    log = get_logger(__name__)
    log.info("Test started")
"""
import logging
import sys
from pathlib import Path
from datetime import datetime

try:
    import colorlog
    _HAS_COLORLOG = True
except ImportError:
    _HAS_COLORLOG = False

LOGS_DIR = Path(__file__).resolve().parent.parent / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

_LOG_FILE = LOGS_DIR / f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

_FMT = "%(asctime)s [%(levelname)8s] %(name)s: %(message)s"
_DATE_FMT = "%Y-%m-%d %H:%M:%S"

_COLOR_FMT = (
    "%(log_color)s%(asctime)s [%(levelname)8s]%(reset)s %(name)s: %(message)s"
)
_LOG_COLORS = {
    "DEBUG": "cyan",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "bold_red",
}

_configured = False


def _configure_root() -> None:
    global _configured
    if _configured:
        return
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    if _HAS_COLORLOG:
        ch.setFormatter(
            colorlog.ColoredFormatter(_COLOR_FMT, datefmt=_DATE_FMT, log_colors=_LOG_COLORS)
        )
    else:
        ch.setFormatter(logging.Formatter(_FMT, datefmt=_DATE_FMT))

    # File handler (DEBUG level — keeps everything)
    fh = logging.FileHandler(_LOG_FILE, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(_FMT, datefmt=_DATE_FMT))

    root.addHandler(ch)
    root.addHandler(fh)
    _configured = True


def get_logger(name: str) -> logging.Logger:
    """Return a named logger. Call once per module."""
    _configure_root()
    return logging.getLogger(name)
