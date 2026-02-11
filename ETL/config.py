"""
Download files
"""

Web_page = "https://www.pwc.com/us/en/careers/university_relations/data_analytics_cases_studies/"

URLS = [
    [Web_page + "PurchasesFINAL12312016csv.zip","PurchaseDec"],
    [Web_page + "BegInvFINAL12312016csv.zip","BegInvDec"],
    [Web_page + "2017PurchasePricesDeccsv.zip","PricingPurchasesDec"],
    [Web_page + "VendorInvoices12312016csv.zip","VendorInvoicesDec"],
    [Web_page + "EndInvFINAL12312016csv.zip","EndInvDec"],
    [Web_page + "SalesFINAL12312016csv.zip","SalesDec"]
]

LOCAL_PATH = 'Data/'

DATABASE_PATH = "Annies.db"

TABLES = [
    "PurchaseDec",
    "BegInvDec",
    "PricingPurchasesDec",
    "VendorInvoicesDec",
    "EndInvDec",
    "SalesDec"
]