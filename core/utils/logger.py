import logging
import colorlog

def get_logger(name: str) -> logging.Logger:
    """
    Создает и возвращает настроенный логгер с цветным выводом в консоль.

    :param name: Имя логгера.
    :return: Экземпляр настроенного логгера.
    """

    handler = colorlog.StreamHandler()

    formatter = colorlog.ColoredFormatter(
        fmt="%(log_color)s%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            "DEBUG":    "cyan",
            "INFO":     "green",
            "WARNING":  "yellow",
            "ERROR":    "red",
            "CRITICAL": "bold_red",
        }
    )

    handler.setFormatter(formatter)

    logger = colorlog.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger
