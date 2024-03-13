import os
import uuid
import logging

# Logging config

logFormat = "[%(levelname)s:%(asctime)s] %(message)s"
logging.basicConfig(
    level=logging.INFO, 
    filemode="w", 
    format= logFormat
)

# Log filesystem functions

def generateLogFile(prefix):
    with open(f"logs/{prefix}-{str(uuid.uuid4()).replace('-', '')}.log", "w") as f:
        f.write("")
        return f.name

def retrieveLog(fName):
    if os.path.isfile(f"logging/{fName}") == True:
        with open(f"logging/{fName}", "r") as f:
            return f.read()
        
def flushLogs():
    os.removedirs("logging")
    os.mkdir("logging")
    
# Logger object functions

def newLogger(logFile: str):
    logger = logging.getLogger(__name__)
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