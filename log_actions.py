from log_settings import logger


def log_register_user(username: str, phone_number: str | None=None):
    """"Добавляет в лог регистрацию пользователя"""

    if phone_number:
        logger.info(f"Пользователь {username} зарегистрировался с номером телефона {phone_number}")
    else:
        logger.info(f"Пользователь {username} номер телефона не предоставил")


def log_phone_number(username, phone_number):
    """Добавляет в лог номер телефона"""

    logger.info(f"Пользователь {username} добавил номер телефона {phone_number}")