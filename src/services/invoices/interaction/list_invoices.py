from services.invoices.models.invoice import Invoice
from peewee import prefetch
from services.invoices.models.invoice_items import InvoiceItems
from services.invoices.models.invoice_billsundry import InvoiceBillSundry
from playhouse.shortcuts import model_to_dict
import json
from libs.get_filters import get_filters
from math import ceil

possible_filters = ['id', 'invoice_number', 'customer_name', 'GSTIN', 'continent_id', 'trade_type', 'is_active']

def list_invoices(filters, sort_by, sort_type, pagination_required, page_limit, page):
    query = get_query(sort_by, sort_type, page, page_limit)
    if filters:
        if type(filters) != dict:
            filters = json.loads(filters)

        query = get_filters(filters, query, Invoice)

    data = get_data(query)
    if pagination_required:
        pagination_data = get_pagination_data(query, page, page_limit)
        return {'list': data } | pagination_data
    return {'list': data }

def get_query(sort_by, sort_type, page, page_limit):
  query = Invoice.select().where(Invoice.is_active == True).order_by(eval('Invoice.{}.{}()'.format(sort_by,sort_type))).paginate(page, page_limit)
  return query

def get_data(query):
    only = [
            Invoice.id,
            Invoice.invoice_number,
            Invoice.GSTIN,
            Invoice.invoice_items,
            Invoice.invoice_bill_sundry,
            InvoiceItems.id,
            InvoiceBillSundry.id
        ]
        
    invoice_data = [model_to_dict(row, only=only, recurse=True, backrefs=True, max_depth=1) for row in prefetch(query,InvoiceItems,InvoiceBillSundry)]
    return invoice_data

def get_pagination_data(query, page, page_limit):
    total_count = query.count()
    pagination_data = {
        'page': page,
        'total': ceil(total_count/page_limit),
        'total_count': total_count,
        'page_limit': page_limit
        }
    return pagination_data