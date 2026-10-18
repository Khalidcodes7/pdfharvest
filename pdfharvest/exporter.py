"""Export extracted PDF data to Excel."""
from __future__ import annotations

import logging
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

from .extractor import ExtractedDocument

logger = logging.getLogger(__name__)


def export_to_excel(docs: list[ExtractedDocument], output_path: str | Path) -> str:
    """Export a list of ExtractedDocument objects to an Excel file."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    wb = Workbook()
    # Remove default sheet
    default_sheet = wb.active
    wb.remove(default_sheet)

    header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True)

    for doc in docs:
        if doc.error:
            logger.warning("Skipping %s due to error: %s", doc.file_path, doc.error)
            continue

        file_name = Path(doc.file_path).stem[:25]  # max 31 chars for sheet name
        
        # 1. Export Tables (if any)
        for page in doc.pages:
            if not page.tables:
                continue
            
            for t_idx, table in enumerate(page.tables, start=1):
                sheet_name = f"{file_name}_p{page.page_number}_t{t_idx}"[:31]
                sheet = wb.create_sheet(title=sheet_name)
                
                for row_idx, row in enumerate(table, start=1):
                    for col_idx, cell_value in enumerate(row, start=1):
                        cell = sheet.cell(row=row_idx, column=col_idx, value=str(cell_value))
                        if row_idx == 1:  # Header styling
                            cell.fill = header_fill
                            cell.font = header_font
                            cell.alignment = Alignment(horizontal="center")

        # 2. Export Text (only if no tables were found in the document)
        has_tables = any(page.tables for page in doc.pages)
        if not has_tables:
            sheet_name = f"{file_name}_Text"[:31]
            sheet = wb.create_sheet(title=sheet_name)
            
            # Headers
            sheet.append(["Page", "Text"])
            sheet.cell(1, 1).fill = header_fill
            sheet.cell(1, 1).font = header_font
            sheet.cell(1, 2).fill = header_fill
            sheet.cell(1, 2).font = header_font
            
            for page in doc.pages:
                sheet.append([page.page_number, page.text])
                
            sheet.column_dimensions['A'].width = 10
            sheet.column_dimensions['B'].width = 100

    # If everything was empty or errored, create a placeholder sheet
    if not wb.sheetnames:
        wb.create_sheet(title="No Data")
        wb["No Data"].append(["No text or tables could be extracted from the provided PDFs."])

    wb.save(path)
    logger.info("Exported %d documents to %s", len(docs), path)
    return str(path)