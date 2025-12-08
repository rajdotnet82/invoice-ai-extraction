import pandas as pd

SRC = "data/Case Study Data_demo.xlsx"
DEST = "data/Case Study Data_small.xlsx"

# Read only the 2 necessary sheets
header = pd.read_excel(SRC, sheet_name="SalesOrderHeader")
detail = pd.read_excel(SRC, sheet_name="SalesOrderDetail")

# Write only these 2 sheets into a new workbook
with pd.ExcelWriter(DEST, engine="openpyxl") as writer:
    header.to_excel(writer, sheet_name="SalesOrderHeader", index=False)
    detail.to_excel(writer, sheet_name="SalesOrderDetail", index=False)

print("✅ Created smaller Excel:", DEST)
print("Header rows:", len(header))
print("Detail rows:", len(detail))
