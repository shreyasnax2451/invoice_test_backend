from database.db_session import db
from services.invoices.models.invoice import Invoice
from fastapi import HTTPException

def delete_invoice(request):
    with db.atomic():
        return execute_transaction_code(request)

def execute_transaction_code(request):
    query = Invoice.select().where(
        Invoice.id == request['id']
    ).get()

    if not query:
        raise HTTPException(status_code=400, detail='Invoice Not Found')
    query.is_active = False

    try:
        query.save()
    except:
        raise HTTPException(status_code=500, detail='Invoice Not Deleted')
    return {'id':query.id}