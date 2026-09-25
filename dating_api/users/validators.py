from django.core.exceptions import ValidationError
import re


def validate_age(value):
    if value < 18:
        raise ValidationError("Регистрация доступна с 18 лет.")
    if value > 120:
        raise ValidationError("Возраст не может быть больше 120.")


def validate_no_contacts(text):
    pattern = r"(\+?\d[\d\s\-\(\)]{8,})|([\w\.-]+@[\w\.-]+\.\w+)"
    if re.search(pattern, text):
        raise ValidationError("Контакты (телефон, email) нельзя указывать в этом поле.")