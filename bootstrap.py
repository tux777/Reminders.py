import sys
import os
from components.logging import generateLogFile, newLogger, addCounter

def main():
    # Logging
    logFile = generateLogFile(__name__)
    logger = newLogger(__name__, logFile)
    addCounter(logger)

    # System Checks
    # OS Check
    osName = sys.platform
    match osName:
        case "darwin":
            logger.info("OS is darwin")
        case "win32":
            logger.info("OS is win32")
        case "linux":
            logger.info("OS is linux")
        case _:
            logger.error('OS is not supported!')
            
    # PIP requirements checks
    with open("support/requirements.txt", "r") as f:
        requirements = f.read().split("\n")

    for req in requirements:
        try:
            __import__(req)
        except ModuleNotFoundError:
            logger.error(f"Module {req} not found!")
            logger.info("Installing modules...")
            try:
                pyInterpreter = sys.executable
                os.system(f"{pyInterpreter} -m pip install -r support/requirements.txt")
                logger.info("Installed modules!")
            except Exception as err:
                logger.error(f"{err}")

    if logger.error_count > 0:
        logger.critical(f"Aborting due to {logger.error_count} error(s). Check {logger.handlers[0].baseFilename} for error reference")
    else:
        logger.info("Starting notification daemon...")
        from components.notification_daemon import startDaemon
        startDaemon()
        logger.info("Daemon exited. Shutting down bootstrap.")

if __name__ == "__main__":
    main()