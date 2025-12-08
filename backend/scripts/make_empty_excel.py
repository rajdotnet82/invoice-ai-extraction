import pandas as pd

SRC = "data/Case Study Data_demo.xlsx"
DEST = "data/Case Study Data_empty.xlsx"

header_cols = pd.read_excel(SRC, sheet_name="SalesOrderHeader", nrows=0)
detail_cols = pd.read_excel(SRC, sheet_name="SalesOrderDetail", nrows=0)

with pd.ExcelWriter(DEST, engine="openpyxl") as writer:
    header_cols.to_excel(writer, sheet_name="SalesOrderHeader", index=False)
    detail_cols.to_excel(writer, sheet_name="SalesOrderDetail", index=False)

print("✅ Created empty structured Excel:", DEST)
