from peewee import *
from database.db_session import db
import datetime
from services.invoices.models.invoice import Invoice

class BaseModel(Model):
    class Meta:
        database = db
        save_only_dirty = True

class InvoiceBillSundry(BaseModel):
    id = UUIDField(constraints=[SQL('DEFAULT gen_random_uuid()')], primary_key = True)
    bill_sundry_name = CharField(index = True)
    amount = FloatField()
    created_at = DateTimeField(default = datetime.datetime.now)
    updated_at = DateTimeField(default = datetime.datetime.now)

    class Meta:
        table_name = 'invoice_bill_sundry'

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super(InvoiceBillSundry, self).save(*args, **kwargs)