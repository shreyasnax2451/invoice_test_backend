from peewee import *
from database.db_session import db
import datetime
from playhouse.postgres_ext import *
from fastapi import HTTPException

class BaseModel(Model):
    class Meta:
        database = db
        save_only_dirty = True

class Invoice(BaseModel):
    id = UUIDField(constraints=[SQL('DEFAULT gen_random_uuid()')], primary_key = True)
    invoice_number = BigIntegerField(constraints=[SQL("DEFAULT nextval('invoices_invoice_number_seq'::regclass)")])
    customer_name = CharField()
    billing_address = TextField()
    shipping_address = TextField()
    GSTIN = TextField() 
    total_amount = FloatField()
    created_at = DateTimeField(default = datetime.datetime.now)
    updated_at = DateTimeField(default = datetime.datetime.now)
    is_active = BooleanField(default=True)

    class Meta:
        table_name = 'invoices'
    
    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super(Invoice, self).save(*args, **kwargs)

    def validate_invoice_total_amount(self, items_total, bill_sundry_total):
        if self.total_amount != (items_total + bill_sundry_total):
            raise HTTPException(status_code = 400, detail="Total Amount doesn't match with items and bill sundry")