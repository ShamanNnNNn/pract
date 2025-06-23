pip install tinydb

from tinydb import TinyDB, Query
import re
import sys
from datetime import datetime
db = TinyDB('db.json')

Users = Query()

db.insert({
    'name': 'Contact',
    'mail': 'email',
    'tel': 'phone',
})
db.insert({
    'name': 'Order',
    'date_order': 'date',
    'order_type': 'text'
})

def detect_field_type(value):
    if isinstance(value, str):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            return "date"
        except ValueError:
            pass
        cleaned_phone = "".join(filter(str.isdigit, value))
        if 7 <= len(cleaned_phone) <= 15:
            return "phone"
        if "@" in value and "." in value.split("@")[-1]:
            return "email" 
        
        
        return "text"
def get_tpl(**kwargs):
    Form = Query()
    
    query_field_types = {field: detect_field_type(value) for field, value in kwargs.items()}
    
    possible_forms = []
    for form in db.all():
        form_fields = set(form.keys()) - {'name'}
        query_fields = set(kwargs.keys())
        
        if query_fields.issubset(form_fields):
            match = True
            for field in query_fields:
                if form[field] != query_field_types[field]:
                    match = False
                    break
            if match:
                possible_forms.append(form)
    
    if possible_forms:
        return f"Form: '{possible_forms[0]['name']}'"
    else:
        return query_field_types

print(get_tpl(tumba='vasia@gmail.com', youmba='7 800 555 35 35'))  
print(get_tpl(mail='vasia@gmail.com', tel='7 800 555 35 35'))   
print(get_tpl(date_order='27.09.2025', order_type='Order_N'))
print(get_tpl(mail='vasia@gmail.com'))   
print(get_tpl(date_order='27.09.2025'))   
print(get_tpl(pupa='27.09.2025', lupa='Order_N'))   
