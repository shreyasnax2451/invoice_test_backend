from peewee import *
from database.db_session import db
import datetime
from fastapi import HTTPException, status
from services.invoices.models.invoice import Invoice

class BaseModel(Model):
    class Meta:
        database = db
        save_only_dirty = True

class InvoiceItems(BaseModel):
    id = UUIDField(constraints=[SQL('DEFAULT gen_random_uuid()')], primary_key = True)
    item_name = CharField(index = True)
    quantity = FloatField()
    price = FloatField()
    amount = FloatField()
    invoice_id = ForeignKeyField(Invoice, backref='invoice_items')
    created_at = DateTimeField(default = datetime.datetime.now)
    updated_at = DateTimeField(default = datetime.datetime.now)

    class Meta:
        table_name = 'invoice_items'

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super(InvoiceItems, self).save(*args, **kwargs)

    def validate_invoice_items(self):
        if self.price > 0 and self.quantity > 0:
            if not (self.amount == self.price * self.quantity):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Amount Doesnt match with price and quantity')
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Price And Quantity should be greater than 0')