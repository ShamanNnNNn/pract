import re
from datetime import datetime

def detect_field_type(value: str) -> str:
    if not isinstance(value, str):
        return "text"
    
    date_formats = ["%d.%m.%Y", "%Y-%m-%d"]
    for fmt in date_formats:
        try:
            datetime.strptime(value, fmt)
            return "date"
        except ValueError:
            pass

    cleaned_phone = re.sub(r'[^\d+]', '', value)
    if re.fullmatch(r'^(\+7)?\d{10}$', cleaned_phone):
        return "phone"

    if re.fullmatch(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', value):
        return "email"

    return "text"

def main():
    test_cases = [
        ("01.01.2023", "date"),
        ("31.12.2022", "date"),
        ("2022-12-31", "date"),
        ("31-12-2022", "text"),
        ("2022.12.31", "text"),
        ("20221231", "text"),
        ("31.13.2022", "text"),
        ("32.01.2022", "text"),
        ("01.01.99", "text"),
        ("not_a_date", "text"),
        ("+7 912 345 67 89", "phone"),
        ("+7(912)345-67-89", "phone"),
        ("89123456789", "phone"),
        ("+79123456789", "phone"),
        ("7 912 345 67 89", "phone"),
        ("8-912-345-67-89", "phone"),
        ("+71234567890", "phone"),
        ("phone_number", "text"),
        ("test@example.com", "email"),
        ("user.name+tag@domain.co.uk", "email"),
        ("user@localhost", "text"),
        ("user@.com", "text"),
        ("@example.com", "text"),
        ("user@domain", "text"),
        ("regular string", "text"),
        ("12345", "text"),
        ("special_chars!@#", "text"),
        ("", "text"),
        (12345, "text"),
        (None, "text")
    ]

    print("Результаты определения типа поля:\n")
    print("{:<20} {:<10} {:<10}".format("Входное значение", "Ожидается", "Получено"))
    print("-" * 45)
    
    for value, expected in test_cases:
        result = detect_field_type(value)
        status = "✓" if result == expected else "✗"
        print("{:<20} {:<10} {:<10} {}".format(
            repr(str(value)[:18]), 
            expected, 
            result, 
            status
        ))

if __name__ == "__main__":
    main()