# core/schema.py

# This dictionary defines the single, stable JSON structure for all documents.
# It serves as the "ground truth" for both AI parsing and rule-based extraction.

NORMALIZED_SCHEMA = {
    "metadata": {
        "file_name": None,
        "parsing_method": None, # Will be 'ai' or 'rule'
        "signature_used": None   # Will be a hash or a name
    },
    "data": {
        "invoice_id": None,
        "vendor_name": None,
        "customer_name": None,
        "total_amount": None,
        "invoice_date": None,
        "due_date": None
    }
}