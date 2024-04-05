from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from database.db_support import get_db
from services.invoices.invoice_router import invoice_router
from database.create_tables import create_tables
from services.invoices.models.invoice import Invoice
from services.invoices.models.invoice_items import InvoiceItems
from services.invoices.models.invoice_billsundry import InvoiceBillSundry

app = FastAPI()

app.include_router(prefix='/invoice', dependencies=[Depends(get_db)], router=invoice_router, tags = ['Invoices'])

@app.get('/')
def read_root():
    return 'Backend'