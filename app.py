import argparse
from tinydb import TinyDB, Query
import re
from datetime import datetime

# Инициализация базы данных
db = TinyDB('db.json')

# Предопределенные формы
if not db.all():
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


def detect_field_type(value: str) -> str:
    if not isinstance(value, str):
        return "text"

    # Проверка даты в формате DD.MM.YYYY
    try:
        datetime.strptime(value, "%d.%m.%Y")
        return "date"
    except ValueError:
        pass

    # Проверка даты в формате YYYY-MM-DD
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return "date"
    except ValueError:
        pass

    # Нормализация телефона
    cleaned_phone = re.sub(r'[^\d+]', '', value)
    phone_pattern = re.compile(r'^(\+7|7|8)?\d{10}$')

    if phone_pattern.fullmatch(cleaned_phone):
        return "phone"

    # Проверка email
    if re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', value):
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
        return possible_forms[0]['name']
    else:
        return query_field_types


def main():
    parser = argparse.ArgumentParser(description='Определение шаблона формы по введенным полям')
    parser.add_argument('command', help='Команда (get_tpl)')
    parser.add_argument('fields', nargs='+', help='Поля формы в формате --имя=значение')

    args = parser.parse_args()

    if args.command != 'get_tpl':
        print("Неизвестная команда. Используйте 'get_tpl'")
        return

    # Парсинг полей
    fields = {}
    for field in args.fields:
        if field.startswith('--'):
            field = field[2:]
            if '=' in field:
                key, value = field.split('=', 1)
                fields[key] = value
            else:
                print(f"Некорректный формат поля: {field}")
                return

    result = get_tpl(**fields)

    if isinstance(result, str):
        print(f"Форма: '{result}'")
    else:
        print("Совпадающая форма не найдена. Типы полей:")
        for field, field_type in result.items():
            print(f"{field}: {field_type}")


if __name__ == '__main__':
    main()
