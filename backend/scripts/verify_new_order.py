import sys
import pandas as pd

DEMO_XLSX = "data/Case Study Data_demo.xlsx"

def main():
    if len(sys.argv) < 2:
        print("Usage: python verify_new_order.py <SalesOrderID>")
        return

    new_id = int(sys.argv[1])

    header = pd.read_excel(DEMO_XLSX, sheet_name="SalesOrderHeader")
    detail = pd.read_excel(DEMO_XLSX, sheet_name="SalesOrderDetail")

    new_header = header[header["SalesOrderID"] == new_id]
    new_detail = detail[detail["SalesOrderID"] == new_id]

    print("=== New Header Row ===")
    print(new_header if not new_header.empty else "No header found.")

    print("\n=== New Detail Rows ===")
    print(new_detail if not new_detail.empty else "No details found.")

if __name__ == "__main__":
    main()
