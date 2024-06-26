import sys
import os
import json
import threading
import time
import subprocess
import python.components.log as log
from python.components.notification_daemon import startDaemon

def main(logger):
    # * System Checks
    # * OS Check
    osName = sys.platform
    match osName:
        case "darwin":
            logger.debug("OS is Darwin")
            settingsFilePath = f"{os.path.expanduser('~')}/.config/Reminders/"
        case "win32":
            logger.debug("OS is Win32")
            settingsFilePath = f"{os.getenv('LOCALAPPDATA')}\\Reminders\\"
        case "linux":
            logger.debug("OS is Linux")
            settingsFilePath = f"{os.path.expanduser('~')}/.config/Reminders/"
        case _:
            logger.critical('OS is not supported!')
            exit()
            
    # Settings file check
    if os.path.isdir(settingsFilePath) == False:
        logger.debug("Settings file not found, creating one...")
        try:
            os.mkdir(settingsFilePath)
            with open(f'{settingsFilePath}settings.json', "w") as f:
                json.dump({"mode": None, "logging": {"level": "info"}}, f)
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
        if os.path.isfile(f"{settingsFilePath}reminders.json") == False:
            logger.debug("Settings file not found, creating one...")
            try:
                with open(f'{settingsFilePath}reminders.json', "w") as f:
                    json.dump({}, f)
            except (OSError, PermissionError) as err:
                if type(err) == OSError:
                    logger.critical(f"Generic OSError exception thrown: {err}")
                elif type(err) == PermissionError:
                    logger.critical(f"PermissionError exception thrown: {err}\nIf you're on MacOS be sure to give your terminal Full Disk Access")
    
    with open(f'{settingsFilePath}settings.json', "r") as f:
        settings = json.load(f)
    
    # PIP requirements checks
    with open("python/support/requirements.txt", "r") as f:
        requirements = f.read().split("\n")

    i = 0
    for req in requirements:
        i+=1
        if i >= 4:
            logger.critical("Failed to download requirements successfully. Check your internet connection and try again.")
            exit()
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

    # Reminders Mode

    try:
        match settings["mode"]:
            
            case "python":
                logger.info("Starting python mode...")
                startDaemon()
            
            case "web":
                match osName:
                    case "win32":
                        shellEnabled = True
                    case _:
                        shellEnabled = False
                        
                logger.info("Starting web mode...")
                logger.info("Checking if npm dependencies are installed at web...")
                    
                
                react_prefix = os.path.join(os.getcwd(), "web")
                react_backend_prefix = os.path.join(os.getcwd(), "web/backend")
                react_modules = os.path.join(os.getcwd(), "web/node_modules")
                react_backend_modules = os.path.join(os.getcwd(), "web/backend/node_modules")
                
                working_dir = os.getcwd()
                
                if os.path.isdir(react_modules):
                    logger.info("NPM dependencies are already installed!")
                else:
                    logger.info("NPM dependencies are not installed, installing them now...")
                    os.chdir(react_prefix)
                    subprocess.run(["npm", "install"], shell=shellEnabled)
                    os.chdir(working_dir)
                    
                logger.info("Checking if npm dependencies are installed at web/backend...")
                
                if os.path.isdir(react_backend_modules):
                    logger.info("NPM dependencies are already installed!")
                else:
                    logger.info("NPM dependencies are not installed, installing them now...")
                    os.chdir(react_backend_prefix)
                    subprocess.run(["npm", "install"], shell=shellEnabled)
                    os.chdir(working_dir)
                    
                cmd_react = ["npm", "--prefix", react_prefix, "start"]
                cmd_react_backend = ["npm", "--prefix", react_backend_prefix, "start"]
                
                thread_react = threading.Thread(target=subprocess.run, args=(cmd_react,), kwargs={"shell": shellEnabled}, daemon=True)
                thread_react_backend = threading.Thread(target=subprocess.run, args=(cmd_react_backend,), kwargs={"shell": shellEnabled}, daemon=True)
                thread_notification_daemon = threading.Thread(target=startDaemon, daemon=True)
                
                thread_react.start()
                thread_react_backend.start()
                thread_notification_daemon.start()
                
                while True:
                    time.sleep(1)
    except KeyError:
        print("1) Python Mode")
        print("2) Web Mode")
            
        mode = input("No mode set, select a mode and press enter to continue. > ")
        match mode:
            case "1":
                settings["mode"] = "python"
            case "2":
                settings["mode"] = "web"
            case _:
                while True:
                    mode = input("Invalid mode selected. Please select a valid mode. > ")
                    match mode:
                        case "1":
                            settings["mode"] = "python"
                            break
                        case "2":
                            settings["mode"] = "web"
                            break
                        case _:
                            continue
                            
        with open(f'{settingsFilePath}settings.json', "w") as f:
                json.dump(settings, f)

if __name__ == "__main__":
    # Logging
    filePath = __file__
    logFile = log.generateLogFile(filePath)
    logger = log.newLogger(__file__, logFile)
    log.addCounter(logger)
    sys.excepthook = lambda type, value, tb: log.logException(type, value, tb, logger) # Hook exception to log it
    
    main(logger)