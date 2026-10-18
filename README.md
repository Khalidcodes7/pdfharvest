# PDFHarvest

> Extract text and tables from any PDF document and export it cleanly to Excel — with one command.

[![CI](https://github.com/Khalidcodes7/pdfharvest/actions/workflows/ci.yml/badge.svg)](https://github.com/Khalidcodes7/pdfharvest/actions)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**PDFHarvest** is a Python tool designed to automate the painful process of manually copying data from PDFs (like invoices, bank statements, or reports) into spreadsheets. 

It reads PDFs, pulls out text or structured tables, and builds a styled Excel workbook ready for analysis.

---

## ✨ Features

- 📄 **Batch Processing** — Pass a single PDF or a whole folder of PDFs.
- 📊 **Table Extraction** — Automatically detects and extracts tables into Excel sheets.
- 📝 **Text Extraction** — If no tables exist, it dumps clean, readable text.
- 🎨 **Styled Excel Output** — Auto-sized columns, colored headers, and frozen panes.
- 🖥️ **CLI & Python API** — Run it from the terminal or import it into your own scripts.
- 🛡️ **Error Handling** — Safely skips encrypted, corrupted, or unreadable files.

---

## 📦 Installation

```bash
git clone https://github.com/Khalidcodes7/pdfharvest.git
cd pdfharvest
pip install -e ".[dev]"
