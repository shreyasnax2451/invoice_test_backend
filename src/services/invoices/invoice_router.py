from fastapi import APIRouter, HTTPException
from services.invoices.invoice_params import *
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from services.invoices.interaction.create_invoice import create_invoice
from services.invoices.interaction.get_invoice import get_invoice
from services.invoices.interaction.delete_invoice import delete_invoice
from services.invoices.interaction.list_invoices import list_invoices

invoice_router = APIRouter()

@invoice_router.post('/invoice')
def create_invoice_api(request: CreateInvoice):
    try:
        response = create_invoice(request.dict())
        return JSONResponse(status_code=200, content=jsonable_encoder(response))
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(status_code=500, content={'success':False, 'error':str(e)})

@invoice_router.get('/invoice')
def get_invoice_data(
    invoice_number: int
):
    try:
        request = {
            'invoice_number':invoice_number
        }
        response = get_invoice(request)
        return JSONResponse(status_code=200, content=jsonable_encoder(response))
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(status_code=500, content={'success':False, 'error':str(e)})

@invoice_router.delete('/invoice')
def delete_invoice_data(request: DeleteInvoice):
    try:
        response = delete_invoice(request.dict())
        return JSONResponse(status_code=200, content=jsonable_encoder(response))
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(status_code=500, content={'success':False, 'error':str(e)})
    
@invoice_router.get('/list_invoices')
def list_invoices_data(
    filters: str = {},
    sort_by: str = 'created_at',
    sort_type: str = 'desc',
    pagination_required: bool = True,
    page_limit: int = 10, 
    page: int = 1,
    ):
    try:
        response = list_invoices(filters, sort_by, sort_type, pagination_required, page_limit, page)
        return JSONResponse(status_code=200, content=jsonable_encoder(response))
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(status_code=500, content={'success':False, 'error':str(e)})