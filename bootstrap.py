import sys
import os
import components.log as log

def main():
    # Logging
    filePath = __file__
    logFile = log.generateLogFile(filePath)
    logger = log.newLogger(__file__, logFile)
    log.addCounter(logger)
    sys.excepthook = lambda type, value, tb: log.logException(type, value, tb, logger) # Hook exception to log it

    # System Checks
    # OS Check
    osName = sys.platform
    match osName:
        case "darwin":
            logger.info("OS is Darwin")
        case "win32":
            logger.info("OS is Win32")
        case "linux":
            logger.info("OS is Linux")
        case _:
            logger.error('OS is not supported!')
            
    # PIP requirements checks
    with open("support/requirements.txt", "r") as f:
        requirements = f.read().split("\n")

    for req in requirements:
        try:
            if req == "pyobjus":
                if osName == "darwin":
                    __import__(req)
                else:
                    continue
            else:
                __import__(req)
        except ModuleNotFoundError:
            logger.error(f"Module {req} not found!")
            logger.info("Installing modules...")
            try:
                pyInterpreter = sys.executable
                os.system(f"{pyInterpreter} -m pip install {req}")
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