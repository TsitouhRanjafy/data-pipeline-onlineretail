from datetime import datetime


def transform(doc: dict, change_type: str) -> dict:
    return {
        "invoice_no":   doc["InvoiceNo"],
        "stock_code":   doc["StockCode"],
        "description":  doc["Description"],
        "quantity":     int(doc["Quantity"]),
        "invoice_date": doc["InvoiceDate"],
        "unit_price":   float(doc["UnitPrice"]),
        "customer_id":  float(doc["CustomerID"]),
        "country":      doc["Country"],
        "total_amount": float(doc["TotalAmount"]),
        "uploaded_at":  doc.get("uploaded_at"),
        "processed_at": datetime.now(),
        "change_type":  change_type,
    }