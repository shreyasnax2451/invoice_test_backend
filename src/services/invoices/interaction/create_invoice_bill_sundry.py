from database.db_session import db
from services.invoices.models.invoice_billsundry import InvoiceBillSundry
from operator import attrgetter
from fastapi import HTTPException

def create_invoice_bill_sundry(request):
    with db.atomic():
        return execute_transaction_code(request)
    
def execute_transaction_code(request):
    invoice_bill_sundry = InvoiceBillSundry(**request)
    try:
        invoice_bill_sundry.save()
    except:
        raise HTTPException(status_code=500, detail='Invoice Item Not Saved')

    return {'id': invoice_bill_sundry.id}