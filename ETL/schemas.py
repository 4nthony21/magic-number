"""Expected column schemas for source CSV files.

Define a minimal set of required columns for each table. Tests will
validate that CSV headers contain these columns before attempting to load.
"""

EXPECTED_COLUMNS = {
    "BegInvDec": [
        "InventoryId", "Store", "City", "Brand", "Description", "Size", "onHand", "Price", "startDate",
    ],
    "EndInvDec": [
        "InventoryId", "Store", "City", "Brand", "Description", "Size", "onHand", "Price", "endDate",
    ],
    "PricingPurchasesDec": [
        "Brand", "Description", "Price", "Size", "Volume", "Classification", "PurchasePrice", "VendorNumber", "VendorName",
    ],
    "PurchaseDec": [
        "InventoryId", "Store", "Brand", "Description", "Size", "VendorNumber", "VendorName",
        "PONumber", "PODate", "ReceivingDate", "InvoiceDate", "PayDate", "PurchasePrice", "Quantity", "Dollars",
    ],
    "SalesDec": [
        "InventoryId", "Store", "Brand", "Description", "Size", "SalesQuantity", "SalesDollars", "SalesPrice", "SalesDate",
        "Volume", "Classification",
    ],
    "VendorInvoicesDec": [
        "VendorNumber", "VendorName", "InvoiceDate", "PONumber", "PODate", "PayDate", "Quantity", "Dollars",
    ],
}
