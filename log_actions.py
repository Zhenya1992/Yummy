from log_settings import logger


def log_register_user(username, phone_number):
    """"Добавляет в лог регистрацию пользователя"""

    if phone_number:
        logger.info(f"Пользователь {username} зарегистрировался с номером телефона {phone_number}")
    else:
        logger.info(f"Пользователь {username} номер телефона не предоставил")
