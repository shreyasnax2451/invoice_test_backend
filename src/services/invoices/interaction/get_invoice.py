from services.invoices.models.invoice import Invoice
from fastapi import HTTPException
from playhouse.shortcuts import model_to_dict

def get_invoice(request):
    invoice_data = Invoice.select().where(
        Invoice.invoice_number == request['invoice_number']
    ).get()

    invoice_items = list(invoice_data.invoice_items.dicts())
    invoice_bill_sundry = list(invoice_data.invoice_bill_sundry.dicts())
    invoice_data = model_to_dict(invoice_data) | {
        'invoice_items':invoice_items,
        'invoice_bill_sundry':invoice_bill_sundry
    }
    
    if not invoice_data:
        raise HTTPException(status_code=400, detail='Status Code Not Found')

    return invoice_data