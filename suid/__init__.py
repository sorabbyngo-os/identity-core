"""
Sorabbyngo Universal ID (SUID) — Python Package
"""

from suid.generator import SUID
from suid.validator import validate, parse, is_tampered
from suid.registry import PREFIX
from suid.audit import AuditLogger
from suid.forensics import ForensicExtractor

__version__ = "1.1.0"
__author__  = "Sorabbyngo Company"

__all__ = [
    "SUID",
    "PREFIX",
    "validate",
    "parse",
    "is_tampered",
    "AuditLogger",
    "ForensicExtractor",
]
