import sys
import os
import json
import components.log as log
import threading

def main(logger):
    # System Checks
    # OS Check
    osName = sys.platform
    match osName:
        case "darwin":
            logger.debug("OS is Darwin")
        case "win32":
            logger.debug("OS is Win32")
        case "linux":
            logger.debug("OS is Linux")
        case _:
            logger.error('OS is not supported!')

    # File requirements check
    match osName:
        case "darwin":
            settingsFilePath = f"{os.path.expanduser('~')}/.config/Reminders/"
        case "win32":
            settingsFilePath = f"{os.getenv('APPDATA')}\\Reminders\\"
        case "linux":
            settingsFilePath = f"{os.path.expanduser('~')}/.config/Reminders/"

    if os.path.isdir(settingsFilePath) == False:
        logger.debug("Settings file not found, creating one...")
        try:
            os.mkdir(settingsFilePath)
            with open(f'{settingsFilePath}settings.json', "w") as f:
                json.dump({"logging": {"level": "info"}}, f)
        except (OSError, PermissionError) as err:
            if type(err) == OSError:
                logger.critical(f"Generic OSError exception thrown: {err}")
            elif type(err) == PermissionError:
                logger.critical(f"PermissionError exception thrown: {err}\nIf you're on MacOS be sure to give your terminal Full Disk Access")
    else:
        if os.path.isfile(f"{settingsFilePath}settings.json") == False:
            logger.debug("Settings file not found, creating one...")
            try:
                with open(f'{settingsFilePath}settings.json', "w") as f:
                    json.dump({"logging": {"level": "info"}}, f)
            except (OSError, PermissionError) as err:
                if type(err) == OSError:
                    logger.critical(f"Generic OSError exception thrown: {err}")
                elif type(err) == PermissionError:
                    logger.critical(f"PermissionError exception thrown: {err}\nIf you're on MacOS be sure to give your terminal Full Disk Access")
    
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

    if logger.error_count > 0 or logger.critical_count > 0:
        logger.critical(f"Aborting due to {logger.error_count} error(s). Check {logger.handlers[0].baseFilename} for error reference")
    else:
        logger.info("Starting notification daemon...")
        from components.notification_daemon import startDaemon
        startDaemon()
        logger.info("Daemon exited. Shutting down bootstrap.")

if __name__ == "__main__":
    # Logging
    filePath = __file__
    logFile = log.generateLogFile(filePath)
    logger = log.newLogger(__file__, logFile)
    log.addCounter(logger)
    sys.excepthook = lambda type, value, tb: log.logException(type, value, tb, logger) # Hook exception to log it
    
    logger.debug("Starting bootstrap...")
    logger.info("Press enter to exit.")
    threading.Thread(target=main, args=[logger], daemon=True).start()
    input("")