from classes.people import Member, InvalidNameError, InvalidEmailError, InvalidPhoneError
from datetime import date


print("Демонстрация улучшенных пользовательских исключений\n")

# Пример 1: InvalidNameError с дополнительной логикой
print("1. InvalidNameError:")
try:
    member = Member(1, "John123", "Doe", "john@example.com", "+71234567890", date.today(), date.today())
except InvalidNameError as e:
    e.log_error()
    print(f"Дружелюбное сообщение: {e.get_user_friendly_message()}")
    print(f"Предложенное исправление: {e.get_suggested_correction()}")
    print(f"Код ошибки: {e.error_code}\n")

# Пример 2: InvalidEmailError с дополнительной логикой
print("2. InvalidEmailError:")
try:
    member = Member(2, "John", "Doe", "invalid-email", "+71234567890", date.today(), date.today())
except InvalidEmailError as e:
    e.log_error()
    print(f"Дружелюбное сообщение: {e.get_user_friendly_message()}")
    print(f"Пример корректного формата: {e.get_example_format()}")
    print(f"Код ошибки: {e.error_code}\n")

# Пример 3: InvalidPhoneError с дополнительной логикой
print("3. InvalidPhoneError:")
try:
    member = Member(3, "John", "Doe", "john@example.com", "123", date.today(), date.today())
except InvalidPhoneError as e:
    e.log_error()
    print(f"Дружелюбное сообщение: {e.get_user_friendly_message()}")
    print(f"Ожидаемый формат: {e.get_expected_format()}")
    print(f"Код ошибки: {e.error_code}\n")

# Пример 4: Создание с корректными данными
print("4. Создание Member с корректными данными:")
try:
    member = Member(4, "Иван", "Петров", "ivan@example.com", "+71234567890", date.today(), date.today())
    print(f"   Успешно создан: {member}")
except Exception as e:
    print(f"   Неожиданная ошибка: {e}")
