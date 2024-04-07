from colorama import Fore
from components import CLI
import json
import sys
import os

valid_flags = {
    "exit": None, 
    "reminders": ["-advanced"], 
    "create": ["-name", "-title", "-message", "-time"],
    "delete": ["-name","-all"],
}
remindersFilePath = "components/reminders.json"
reminderObjFormat = {"title": "", "message": "", "time": ""}

bold = "\033[1m"
reset = "\033[0m"

def cli(logger=None):
    commandPrefix = ">"
    
    # Used for saving functionality
    with open(remindersFilePath, "r") as f:
            reminders = json.load(f)
    
    while True:
        commandInput = input(f"{commandPrefix} ")
        cmd = CLI.command(commandInput)
        
        # Executed after every command to get up to date json file 
        with open(remindersFilePath, "r") as f:
            remindersJson = json.load(f)
        
        # Command Handler
        try:
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
                            name = cmd.args["-name"]
                            title = cmd.args["-title"]
                            message = cmd.args["-message"]
                            time = cmd.args["-time"]
                            
                            reminder = reminderObjFormat.copy()
                            reminder["title"] = title
                            reminder["message"] = message
                            reminder["time"] = time
                            reminders[name] = reminder
                        else:
                            for i,v in cmd.args.items():
                                logger.debug(f"{i} | {v}")
                    else:
                        name = input(f"Name {commandPrefix} ")
                        title = input(f"Title {commandPrefix} ")
                        message = input(f"Message {commandPrefix} ")
                        time = input(f"Time {commandPrefix} ")
                        
                        reminder = reminderObjFormat.copy()
                        reminder["title"] = title
                        reminder["message"] = message
                        reminder["time"] = time
                        
                        reminders[name] = reminder
                        
                case "delete":
                    if cmd.argsLen >= 1:
                        if "-all" in cmd.args:
                            reminders.clear()
                        elif "-name" in cmd.args:
                            reminderName = cmd.args["-name"]
                            if reminderName in reminders:
                                reminders.pop(cmd.args["-name"])
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
                case _:
                    if cmd.command == "":
                        continue
                    else:
                        raise CLI.CommandNotFound(cmd.command)
        except Exception as err:
            if logger == None:
                continue
            else:
                logger.error(f"Caught '{type(err).__name__}' CLI error: {err}")
            
                
def main():
    # Logging
    import components.log as log
    logName = __file__.split("/")[-1].removesuffix(".py")
    logFile = log.generateLogFile(logName)
    logger = log.newLogger(logName, logFile)
    log.addCounter(logger)
    sys.excepthook = lambda type, value, tb: log.logException(type, value, tb, logger) # Hook exception to log it
    
    cli(logger)

if __name__ == "__main__":
    main()