import logging


def setup_logger(log_file="insurance_api.log"):

    # Создаем логгер
    logger = logging.getLogger("insurance_api")
    logger.setLevel(logging.DEBUG)

    # Обработчик для записи логов в файл
    log_handler = logging.FileHandler(log_file)
    log_handler.setLevel(logging.DEBUG)

    # Форматтер для задания формата логов
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_handler.setFormatter(log_formatter)

    # Добавляем обработчик к логгеру
    logger.addHandler(log_handler)

    return logger


# Инициализируем логгер
logger = setup_logger()
