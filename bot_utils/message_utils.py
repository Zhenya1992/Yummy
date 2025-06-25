def text_for_caption(name, description, price):
    """Текст для подписи изображения."""
    return (
        f"{name}\n"
        f"Описание: {description}\n"
        f"Стоимость: {price:.2f} BYN"
    )