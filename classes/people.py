from abc import ABC, abstractmethod
import re
from datetime import date
from decimal import Decimal

class GymBaseException(Exception):
    """Базовый класс для всех исключений в системе управления спортзалом"""
    
    def __init__(self, message, error_code=None, details=None):
        super().__init__(message)
        self.error_code = error_code
        self.details = details or {}
        
    def log_error(self):
        """Метод для логирования ошибки"""
        print(f"[ERROR {self.error_code}] {self.args[0]}")
        for key, value in self.details.items():
            print(f"  {key}: {value}")
    
    def get_user_friendly_message(self):
        """Метод для получения дружелюбного сообщения для пользователя"""
        return f"Произошла ошибка: {self.args[0]}"


class InvalidNameError(GymBaseException):
    """Имя или фамилия не соответствуют формату."""
    
    def __init__(self, field_name, invalid_value, reason="содержит недопустимые символы"):
        message = f"Поле '{field_name}' {reason}"
        details = {
            'field_name': field_name,
            'invalid_value': invalid_value,
            'reason': reason
        }
        super().__init__(message, error_code="NAME_001", details=details)
        
    def get_suggested_correction(self):
        """Предложить исправление имени"""
        # Удалить недопустимые символы
        cleaned_value = re.sub(r"[^А-Яа-яA-Za-z\-'\s]", "", self.details['invalid_value'])
        return f"Возможно, вы имели в виду: '{cleaned_value.strip()}'?"


class InvalidEmailError(GymBaseException):
    """Введите корректный email. Например, sergey@example.com"""
    
    def __init__(self, invalid_email):
        message = "Некорректный формат email"
        details = {
            'invalid_email': invalid_email
        }
        super().__init__(message, error_code="EMAIL_001", details=details)
        
    def get_example_format(self):
        """Получить пример корректного формата email"""
        return "Правильный формат email: username@domain.com (например, ivan@example.com)"


class InvalidPhoneError(GymBaseException):
    
    def __init__(self, phone, expected_length=11):
        actual_length = len(phone)
        message = f"Номер телефона должен содержать {expected_length} цифр, не считая +7, содержит: {actual_length}"
        details = {
            'provided_phone': phone,
            'expected_length': expected_length,
            'actual_length': actual_length
        }
        super().__init__(message, error_code="PHONE_001", details=details)
        
    def get_expected_format(self):
        """Получить ожидаемый формат телефона"""
        return "Ожидаемый формат телефона: +7XXXXXXXXXX (11 цифр)"


class Person(ABC):
    def __init__(
        self,
        id: int,
        first_name: str,
        last_name: str,
        email: str,
        phone: str
    ):
        # Валидация и присвоение с обработкой ошибок
        try:
            self.id = self._validate_id(id)
            self.first_name = self._validate_name(first_name, "first_name")
            self.last_name = self._validate_name(last_name, "last_name")
            self.email = self._validate_email(email)
            self.phone = self._validate_phone(phone)
        except (InvalidNameError, InvalidEmailError, InvalidPhoneError, ValueError) as e:
            if hasattr(e, 'log_error'):
                e.log_error()
            else:
                print(f"Ошибка при создании класса Person: {e}")
            raise

    @staticmethod
    def _validate_id(id_val: int) -> int:
        if not isinstance(id_val, int) or id_val <= 0:
            raise ValueError("ID должен быть положительным целым числом.")
        return id_val

    @staticmethod
    def _validate_name(name: str, field: str) -> str:
        if not isinstance(name, str) or not name.strip():
            raise InvalidNameError(field, name, "не может быть пустым")
        if not re.match(r"^[А-Яа-яA-Za-z\-']+$", name.strip(), re.UNICODE):
            raise InvalidNameError(field, name)
        return name.strip()

    @staticmethod
    def _validate_email(email: str) -> str:
        email = email.strip()
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email, re.UNICODE):
            raise InvalidEmailError(email)
        return email

    @staticmethod
    def _validate_phone(phone: str) -> str:
        phone_digits = re.sub(r"\D", "", phone)  # оставляем только цифры
        if len(phone_digits) != 11:
            raise InvalidPhoneError(phone_digits)
        return phone

    @abstractmethod
    def get_full_name(self) -> str:
        #Абстрактный метод, это для наследуюемых классов
        pass

    def __str__(self) -> str:
        return f"{self.get_full_name()} <{self.email}>"

class Member(Person):
    def __init__(self, id: int, first_name: str, last_name: str, email: str, phone: str, membership_start_date: date,
                 membership_end_date: date, is_active: bool=True):
        super().__init__(id, first_name, last_name, email, phone)
        self.membership_start_date = membership_start_date
        self.membership_end_date = membership_end_date
        self.is_active = is_active
    def get_full_name(self) -> str:
            return f"{self.first_name} {self.last_name}"
    def renew_membership(self, days: int = 365) -> None:
            from datetime import timedelta
            self.membership_end_date = date.today() + timedelta(days=days)
            self.is_active = True
    def cancel_membership(self) -> None:
            self.is_active = False

class Coach(Person):
    def __init__(self, id: int, first_name: str, last_name: str, email: str, phone: str, specialization: str, hourly_rate : Decimal):
        super().__init__(id, first_name, last_name, email, phone)
        self.specialization = specialization
        self.hourly_rate = hourly_rate
        self.is_active = True

    def get_full_name(self) -> str:
            return f"{self.first_name} {self.last_name} ({self.specialization})"
    def set_availability(self, available: bool) -> None:
            self.is_active = available
class Staff(Person):
    def __init__(self, id: int, first_name: str, last_name: str, email: str, phone: str, position: str, salary: Decimal, hire_date: date):
        super().__init__(id, first_name, last_name, email, phone)
        self.position = position
        self.salary = salary
        self.hire_date = hire_date

    def get_full_name(self) -> str:
            return f"{self.first_name} {self.last_name} ({self.position})"
    def perform_duty(self) -> None:
            pass