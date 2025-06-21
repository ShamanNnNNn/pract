pip install tinydb

from tinydb import TinyDB, Query
import re
import sys
from datetime import datetime
db = TinyDB('db.json')

Users = Query()

db.insert({
    'Form': 'Contact',
    'name': 'Vasiliy',
    'email': 'vasia@gmail.com',
    'phone': '7 800 555 35 35',
})
db.insert({
    'Form': 'Order',
    'name': 'Petr',
    'date': '27.09.2025',
    'order_type': 'Order_N'
})

def detect_field_type(value):
    if isinstance(value, str):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            return "date"
        except ValueError:
            pass
        
        if "@" in value and "." in value.split("@")[-1]:
            return "email"
        
        cleaned_phone = "".join(filter(str.isdigit, value))
        if 7 <= len(cleaned_phone) <= 15:
            return "phone"

def get_tpl(**kwargs):
    Form = Query()
    
    query = None
    for field, value in kwargs.items():
        if query is None:
            query = (Form[field] == value)
        else:
            query &= (Form[field] == value)
    
    results = db.search(query)
    
    if results:
        return f"Form: '{results[0]['Form']}'"
    
    else:
        field_types = {field: detect_field_type(value) for field, value in kwargs.items()}
        return field_types
print(get_tpl(date='27.09.2025', order_type='Order_N'))


