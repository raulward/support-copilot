import logging


def get_logger(name: str = "supportcopilot") -> logging.Logger:
    logger = logging.getLogger(name)

    # evita adicionar handlers duplicados no reload do uvicorn
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
