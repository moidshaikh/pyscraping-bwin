import logging
from datetime import datetime
import pathlib
from dotenv import dotenv_values

config = dotenv_values(".env")
# creating output dir, if not exists
pathlib.Path("./output").mkdir(parents=True, exist_ok=True)


def loggerConfig(loggername: str, logfile: str, filemode: str) -> logging.Logger:
    logging.basicConfig(
        filename=logfile,
        filemode=filemode,
        format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
        level=logging.INFO,
    )
    logger = logging.getLogger(loggername)
    return logger


def getLogger(loggername: str) -> logging.Logger:
    log_folder = "./logs"
    todays_date = datetime.today().strftime("%Y-%m-%d")
    # creating folder if not exists
    log_path = f"./{log_folder}/{todays_date}"
    pathlib.Path(log_path).mkdir(parents=True, exist_ok=True)
    logfile = pathlib.Path(
        log_path, f"log_{datetime.today().strftime('%b%d_%H')}hr.log"
    )
    mode = "a" if logfile.is_file() else "w"
    lgr = loggerConfig(loggername, logfile, mode)
    lgr.addHandler(logging.StreamHandler())
    return lgr


if __name__ == "__main__":
    ...
