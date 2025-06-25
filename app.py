import argparse
from tinydb import TinyDB, Query
import re
from datetime import datetime
import sys


def init_db():
    db = TinyDB('db.json')
    db.insert({'name': 'Contact', 'mail': 'email', 'tel': 'phone'})
    db.insert({'name': 'Order', 'date_order': 'date', 'order_type': 'text'})
    return db


def detect_field_type(value: str) -> str:
    date_formats = ["%d.%m.%Y", "%Y-%m-%d"]
    for fmt in date_formats:
        try:
            datetime.strptime(value, fmt)
            return "date"
        except ValueError:
            pass

    phone_pattern = r'^\+7 \d{3} \d{3} \d{2} \d{2}$'
    if re.fullmatch(phone_pattern, value.strip()):
        return "phone"

    if re.fullmatch(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', value):
        return "email"

    return "text"


def get_tpl(db, **kwargs):
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


def main():
    parser = argparse.ArgumentParser(description='Определение формы по переданным полям')
    subparsers = parser.add_subparsers(dest='command', required=True)

    get_tpl_parser = subparsers.add_parser('get_tpl')
    get_tpl_parser.add_argument('fields', nargs='*')

    args, unknown = parser.parse_known_args()

    if args.command == 'get_tpl':
        all_args = args.fields + unknown

        fields_dict = {}
        for arg in all_args:
            if '=' not in arg:
                print(f"Ошибка: аргумент '{arg}' должен быть в формате field=value")
                sys.exit(1)
            key, value = arg.split('=', 1)
            fields_dict[key] = value

        db = init_db()
        result = get_tpl(db, **fields_dict)
        print(result)


if __name__ == '__main__':
    main()