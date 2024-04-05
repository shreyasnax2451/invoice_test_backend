from database.db_session import db
from fastapi import HTTPException
from services.invoices.models.invoice import Invoice
from services.invoices.interaction.create_invoice_item import create_invoice_items
from services.invoices.interaction.create_invoice_bill_sundry import create_invoice_bill_sundry

def create_invoice(request):
    with db.atomic():
        return execute_transaction_code(request)

def execute_transaction_code(request):
    invoice_data = Invoice(**request)

    invoice_item_ids = []
    invoice_bill_sundry_ids = []
    invoice_items_amount = 0
    invoice_bill_sundry_amount = 0

    for invoice_item in request['invoice_items']:
        item_id = create_invoice_items(invoice_item)['id']
        invoice_item_ids.append(item_id)
        invoice_items_amount += invoice_item['amount']
    
    for invoice_bill_sundry in request['invoice_bill_sundry']:
        sundry_id = create_invoice_bill_sundry(invoice_bill_sundry)['id']
        invoice_bill_sundry_ids.append(sundry_id)
        invoice_bill_sundry_amount += invoice_bill_sundry['amount']
    
    invoice_data.validate_invoice_total_amount(invoice_items_amount, invoice_bill_sundry_amount)
    invoice_data.invoice_item_ids = invoice_item_ids
    invoice_data.invoice_bill_sundry_ids = invoice_bill_sundry_ids

    try:
        invoice_data.save()
    except:
        raise HTTPException(status_code=500, detail='Invoice Not Saved')
    return {'id':invoice_data.id}
    