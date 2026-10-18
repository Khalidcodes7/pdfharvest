"""Core PDF extraction logic using pdfplumber."""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import pdfplumber

logger = logging.getLogger(__name__)


@dataclass
class ExtractedPage:
    """Data from a single page of a PDF."""
    page_number: int
    text: str
    tables: list[list[list[str]]]


@dataclass
class ExtractedDocument:
    """All data extracted from one PDF file."""
    file_path: str
    page_count: int
    pages: list[ExtractedPage] = field(default_factory=list)
    error: Optional[str] = None


def extract_pdf(file_path: str | Path) -> ExtractedDocument:
    """Extract text and tables from a single PDF file."""
    path = Path(file_path)
    
    if not path.exists():
        return ExtractedDocument(
            file_path=str(path), page_count=0, error="File not found"
        )

    try:
        with pdfplumber.open(path) as pdf:
            pages = []
            for i, page in enumerate(pdf.pages, start=1):
                # Extract text (fallback to empty string if None)
                text = page.extract_text() or ""
                
                # Extract tables (fallback to empty list)
                raw_tables = page.extract_tables() or []
                
                # Clean up tables: replace None cells with empty strings
                tables = [
                    [[cell if cell is not None else "" for cell in row] for row in table]
                    for table in raw_tables
                ]

                pages.append(ExtractedPage(
                    page_number=i,
                    text=text,
                    tables=tables
                ))

            return ExtractedDocument(
                file_path=str(path),
                page_count=len(pdf.pages),
                pages=pages
            )
            
    except Exception as exc:
        logger.error("Failed to extract %s: %s", path, exc)
        return ExtractedDocument(
            file_path=str(path), page_count=0, error=str(exc)
        )