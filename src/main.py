from fastapi import FastAPI, Depends
from database.db_support import get_db
from services.invoices.invoice_router import invoice_router


app = FastAPI()

app.include_router(prefix='/invoice', dependencies=[Depends(get_db)], router=invoice_router, tags = ['Invoices'])

@app.get('/')
def read_root():
    return 'Backend'