"""Command line interface for PDFHarvest."""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from .extractor import extract_pdf
from .exporter import export_to_excel

logger = logging.getLogger("pdfharvest")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pdfharvest",
        description="Extract text and tables from PDFs into Excel.",
    )
    parser.add_argument("input", help="Path to a PDF file or a folder containing PDFs")
    parser.add_argument(
        "-o", "--output", 
        default="output/report.xlsx", 
        help="Output Excel file path (default: output/report.xlsx)"
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug logging")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)-7s %(message)s",
        datefmt="%H:%M:%S",
    )

    input_path = Path(args.input)
    
    # Find all PDFs
    pdf_files = []
    if input_path.is_file() and input_path.suffix.lower() == ".pdf":
        pdf_files.append(input_path)
    elif input_path.is_dir():
        pdf_files.extend(input_path.glob("*.pdf"))
    else:
        logger.error("Input must be a valid .pdf file or a directory containing .pdf files.")
        return 1

    if not pdf_files:
        logger.error("No PDF files found in %s", input_path)
        return 1

    logger.info("Found %d PDF file(s)", len(pdf_files))

    # Extract
    docs = []
    for pdf in pdf_files:
        logger.info("Extracting: %s", pdf.name)
        doc = extract_pdf(pdf)
        if doc.error:
            logger.error("Failed: %s", doc.error)
        else:
            docs.append(doc)

    if not docs:
        logger.error("No documents were successfully extracted.")
        return 1

    # Export
    logger.info("Exporting to %s", args.output)
    export_to_excel(docs, args.output)
    logger.info("Done.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())