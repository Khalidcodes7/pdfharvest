from pdfharvest import extract_pdf, export_to_excel

# 1. Extract the PDF
doc = extract_pdf('examples/dummy.pdf')
print(f"Read {doc.page_count} page(s) from {doc.file_path}")

# 2. Export to Excel
export_to_excel([doc], 'output/test_report.xlsx')
print("Success! Excel file created.")