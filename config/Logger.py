import logging


class Logger:

    @staticmethod
    def init_logger():
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s"
        )
