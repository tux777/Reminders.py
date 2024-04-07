import os
import uuid
import logging
import sys
import json
import traceback
import types

# Logging config

settings_path = "./components/settings.json"
with open(settings_path, "r") as f:
    settings = json.load(f)

logging_settings = settings["logging"]
match logging_settings["level"]:
    case "debug":
        logging_level = logging.DEBUG
    case "info":
        logging_level = logging.INFO
    case "warn":
        logging_level = logging.WARN
    case "error":
        logging_level = logging.ERROR
    case "critical":
        logging_level = logging.CRITICAL
    case _:
        logging_level = logging.INFO

logFormat = "[%(levelname)s:%(asctime)s] %(message)s"
logging.basicConfig(
    level=logging_level, 
    filemode="w", 
    format= logFormat
)

# Log filesystem functions

def generateLogFile(runningFilePath: str):
    # Check if Reminders directory exists in appdata location, respective to the OS
    if sys.platform == "darwin":
        logsFilePath = f"{os.path.expanduser('~')}/Library/Caches/Reminders/"
        prefix = runningFilePath.split("/")[-1].removesuffix(".py")
    elif sys.platform == "win32":
        logsFilePath = f"{os.getenv('LOCALAPPDATA')}\\Reminders\\"
        prefix = runningFilePath.split("\\")[-1].removesuffix(".py")
    elif sys.platform == "linux":
        logsFilePath = "/var/log/Reminders/"
        prefix = runningFilePath.split("/")[-1].removesuffix(".py")
    
    if os.path.isdir(logsFilePath) == False:
        os.mkdir(logsFilePath)
    
    with open(f"{logsFilePath}{prefix}-{str(uuid.uuid4()).replace('-', '')}.log", "w") as f:
        f.write("")
        return f.name

def retrieveLog(fName: str):
    if os.path.isfile(f"logging/{fName}") == True:
        with open(f"logging/{fName}", "r") as f:
            return f.read()
        
def flushLogs():
    os.removedirs("logging")
    os.mkdir("logging")
    
# Logger object functions

def newLogger(runningFilePath: str, logFile: str):
    if sys.platform == "darwin":
        loggerName = runningFilePath.split("/")[-1].removesuffix(".py")
    elif sys.platform == "win32":
        loggerName = runningFilePath.split("\\")[-1].removesuffix(".py")
    elif sys.platform == "linux":
        loggerName = runningFilePath.split("/")[-1].removesuffix(".py")
    logger = logging.getLogger(loggerName)
    loggerHandler = logging.FileHandler(logFile)
    loggerHandler.setFormatter(logging.Formatter("[%(levelname)s:%(asctime)s] %(message)s"))
    logger.addHandler(loggerHandler)
    
    return logger

def addCounter(logger: logging.Logger):
    logger.error_count = 0
    logger.info_count = 0
    logger.warn_count = 0
    logger.critical_count = 0
    
    # Clone unmodified methods to prevent recursion loop
    original_error = logger.error
    original_info = logger.info
    original_warn = logger.warn
    original_critical = logger.critical

    def errorIncrement(msg: str):
        original_error(msg)
        logger.error_count += 1

    def infoIncrement(msg: str):
        original_info(msg)
        logger.info_count += 1

    def warnIncrement(msg: str):
        original_warn(msg)
        logger.warn_count += 1

    def criticalIncrement(msg: str):
        original_critical(msg)
        logger.critical_count += 1
        
    logger.error = errorIncrement
    logger.info = infoIncrement
    logger.warn = warnIncrement
    logger.critical = criticalIncrement
    
def logException(type, value: str, tb: types.TracebackType, logger: logging.Logger) -> None:
    tbList = traceback.format_tb(tb)
    logger.error(f"Caught '{type.__name__}' exception: {value}")
    logger.debug(f"{tbList}")