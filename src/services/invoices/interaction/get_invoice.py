from services.invoices.models.invoice import Invoice
from operator import attrgetter
from fastapi import HTTPException

def get_invoice(request):
    invoice_data = Invoice.select().where(
        Invoice.invoice_number == request['invoice_number']
    ).dicts()
    if not invoice_data:
        raise HTTPException(status_code=400, detail='Status Code Not Found')

    return invoice_data