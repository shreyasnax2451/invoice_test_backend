from database.db_session import db
from fastapi import HTTPException
from services.invoices.models.invoice import Invoice
from services.invoices.models.invoice_billsundry import InvoiceBillSundry
from services.invoices.models.invoice_items import InvoiceItems

def create_invoice(request):
    with db.atomic():
        return execute_transaction_code(request)

def execute_transaction_code(request):
    invoice_data = Invoice(**request)

    invoice_items_amount = 0
    invoice_bill_sundry_amount = 0

    for invoice_item in request['invoice_items']:
        invoice_items_amount += invoice_item['amount']
    
    for invoice_bill_sundry in request['invoice_bill_sundry']:
        invoice_bill_sundry_amount += invoice_bill_sundry['amount']
    
    invoice_data.validate_invoice_total_amount(invoice_items_amount, invoice_bill_sundry_amount)

    try:
        invoice_data.save()
    except:
        raise HTTPException(status_code=500, detail='Invoice Not Saved')
    
    invoice_id = invoice_data.id
    invoice_items = []
    invoice_bill_sundry = []
    for item in request['invoice_items']:
        item['invoice_id'] = invoice_id
        invoice_items.append(item)
    for item in request['invoice_bill_sundry']:
        item['invoice_id'] = invoice_id
        invoice_bill_sundry.append(item)

    try:
        InvoiceItems.insert_many(invoice_items).execute()
    except:
        raise HTTPException(status_code=500, detail='Invoice Items Not Saved')

    try:
        InvoiceBillSundry.insert_many(invoice_bill_sundry).execute()
    except:
        raise HTTPException(status_code=500, detail='Invoice Bill Sundry Not Saved')

    return {'id':invoice_id}
    