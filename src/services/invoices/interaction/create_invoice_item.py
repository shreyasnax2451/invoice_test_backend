from database.db_session import db
from fastapi import HTTPException
from services.invoices.models.invoice import Invoice
from services.invoices.models.invoice_items import InvoiceItems
from operator import attrgetter

def create_invoice_items(request):
    with db.atomic():
        return execute_transaction_code(request)
    
def execute_transaction_code(request):
    invoice_items = InvoiceItems(**request)

    invoice_items.validate_invoice_items()
    try:
        invoice_items.save()
    except:
        raise HTTPException(status_code=500, detail='Invoice Item Not Saved')

    return {'id': invoice_items.id}