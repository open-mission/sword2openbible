"""sword2openbible - Conversor de módulos SWORD para SQLite OpenBible."""

__version__ = "0.1.0"

from .converter import SwordConverter, ConversionError
from .canon import PROTESTANT_CANON, APOCRYPHA_BOOKS, normalize_book_name, get_book_info

__all__ = [
    "SwordConverter",
    "ConversionError",
    "PROTESTANT_CANON",
    "APOCRYPHA_BOOKS",
    "normalize_book_name",
    "get_book_info",
]
