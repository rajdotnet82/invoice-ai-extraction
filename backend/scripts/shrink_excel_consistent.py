import pandas as pd

SRC = "data/Case Study Data_demo.xlsx"
DEST = "data/Case Study Data_tiny.xlsx"

KEEP_HEADER_ROWS = 200  # adjust smaller if you want

header_full = pd.read_excel(SRC, sheet_name="SalesOrderHeader")
header = header_full.tail(KEEP_HEADER_ROWS)

keep_ids = set(header["SalesOrderID"].tolist())

detail_full = pd.read_excel(SRC, sheet_name="SalesOrderDetail")
detail = detail_full[detail_full["SalesOrderID"].isin(keep_ids)]

with pd.ExcelWriter(DEST, engine="openpyxl") as writer:
    header.to_excel(writer, sheet_name="SalesOrderHeader", index=False)
    detail.to_excel(writer, sheet_name="SalesOrderDetail", index=False)

print("✅ Created tiny consistent Excel:", DEST)
print("Header kept:", len(header))
print("Detail kept:", len(detail))
