from colorama import Fore
from python.components import CLI
import json
import sys
import os
import python.components.log as log

bold = "\033[1m"
reset = "\033[0m"

def cli(logger=None):
    commandPrefix = ">"
    
    match sys.platform:
        case "darwin":
            remindersFilePath = f"{os.path.expanduser('~')}/.config/Reminders/reminders.json"
        case "win32":
            remindersFilePath = f"{os.getenv('APPDATA')}\\Reminders\\reminders.json"
        case "linux":
            remindersFilePath = f"{os.path.expanduser('~')}/.config/Reminders/reminders.json"
            
    
    # Used for saving functionality
    with open(remindersFilePath, "r") as f:
            reminders = json.load(f)

    while True:
        commandInput = input(f"{commandPrefix} ")
        
        try:
            cmd = CLI.command(commandInput)
        except Exception as err:
            if logger == None:
                continue
            else:
                if issubclass(type(err), CLI.CLIException):
                    logger.error(f"Caught '{type(err).__name__}' CLI Error: {err}")
                    continue
                else:
                    log.logException(type(err), err, err.__traceback__, logger)
                    exit()

        # Executed after every command to get up to date json file
        with open(remindersFilePath, "r") as f:
            remindersJson = json.load(f)

        # Command Handler
        match cmd.command:
            case "exit":
                exit()

            case "reminders":
                for reminderName,reminderData in remindersJson.items():
                    reminderTitle = reminderData["title"]
                    reminderMessage = reminderData["message"]
                    reminderTime = reminderData["time"]
                    if "-advanced" in cmd.args:
                        print(f"{bold}{Fore.BLUE}{reminderName}:{reset} {Fore.BLUE}{{{Fore.RED}title=\"{reset}{reminderTitle}{Fore.RED}\", {Fore.YELLOW}message=\"{reset}{reminderMessage}{Fore.YELLOW}\", {Fore.GREEN}time=\"{reset}{reminderTime}{Fore.GREEN}\"{Fore.BLUE}}}{reset}")
                    else:
                        print(f"{bold}{Fore.BLUE}{reminderName}:{reset} {reminderMessage} {Fore.RED}@ {Fore.GREEN}{reminderTime}{Fore.RESET}")

            case "create":
                if cmd.argsLen > 0:
                    if "-name" in cmd.args and "-title" in cmd.args and "-message" in cmd.args and "-time" in cmd.args:
                        name = cmd.args["-name"][0]
                        title = cmd.args["-title"][0]
                        message = cmd.args["-message"][0]
                        time = cmd.args["-time"][0]

                        reminder = CLI.reminderJsonFormat.copy()
                        reminder["title"] = title
                        reminder["message"] = message
                        reminder["time"] = time
                        reminders[name] = reminder
                else:
                    name = input(f"Name {commandPrefix} ")
                    title = input(f"Title {commandPrefix} ")
                    message = input(f"Message {commandPrefix} ")
                    time = input(f"Time {commandPrefix} ")

                    reminder = CLI.reminderJsonFormat.copy()
                    reminder["title"] = title
                    reminder["message"] = message
                    reminder["time"] = time

                    reminders[name] = reminder

            case "delete":
                if cmd.argsLen >= 1:
                    if "-all" in cmd.args:
                        reminders.clear()
                    elif "-name" in cmd.args:
                        reminderName = cmd.args["-name"][0]
                        if reminderName in reminders:
                            reminders.pop(reminderName)
                        else:
                            raise CLI.ReminderNotFound(reminderName)
                elif cmd.argsLen == 0:
                    reminderName = input("Reminder to Delete > ")
                    if reminderName in reminders:
                        reminders.pop(reminderName)
                    else:
                        raise CLI.ReminderNotFound(reminderName)

            case "save":
                with open(remindersFilePath, "w") as f:
                    json.dump(reminders, f)
            case "":
                continue

def main():
    # Logging
    logName = __file__.split("/")[-1].removesuffix(".py")
    logFile = log.generateLogFile(logName)
    logger = log.newLogger(logName, logFile)
    log.addCounter(logger)
    sys.excepthook = lambda type, value, tb: log.logException(type, value, tb, logger) # Hook exception to log it

    cli(logger)

if __name__ == "__main__":
    main()