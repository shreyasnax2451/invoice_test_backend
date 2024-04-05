from pydantic import BaseModel
from peewee import *

class CreateInvoiceItems(BaseModel):
    item_name: str
    quantity: float
    price: float
    amount: float

class CreateInvoiceBillSundry(BaseModel):
    bill_sundry_name: str
    amount: float

class CreateInvoice(BaseModel):
    invoice_number: int
    customer_name: str
    billing_address: str
    shipping_address: str
    GSTIN: str
    invoice_items: list[CreateInvoiceItems] = None
    invoice_bill_sundry: list[CreateInvoiceBillSundry] = None
    total_amount: float

class DeleteInvoice(BaseModel):
    id: str