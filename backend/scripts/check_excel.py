import pandas as pd

DEMO_XLSX = "data/Case Study Data_demo.xlsx"

# Load workbook and list sheets
xls = pd.ExcelFile(DEMO_XLSX)
print("Sheets found:", xls.sheet_names)

# Read 2 main tables
header = pd.read_excel(DEMO_XLSX, sheet_name="SalesOrderHeader")
detail = pd.read_excel(DEMO_XLSX, sheet_name="SalesOrderDetail")

print("Header rows:", len(header))
print("Detail rows:", len(detail))

# Find next SalesOrderID
max_id = header["SalesOrderID"].max()
next_id = int(max_id) + 1 if pd.notna(max_id) else 1

print("Current max SalesOrderID:", max_id)
print("Next SalesOrderID should be:", next_id)
