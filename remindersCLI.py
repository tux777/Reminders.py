from components.logging import newLogger, addCounter, generateLogFile, flushLogs
from colorama import Fore
import json
import sys
import os

commandPrefix = ">"
commands = ["exit", "reminders", "clear"]
remindersFilePath = "components/reminders.json"
reminderObjFormat = {"title": "", "message": "", "time": ""}

bold = "\033[1m"
reset = "\033[0m"

def main():
    # Logging
    logName = __file__.split("/")[-1].removesuffix(".py")
    logFile = generateLogFile(logName)
    logger = newLogger(logName, logFile)
    addCounter(logger)
    sys.excepthook = lambda type, value, tb: logger.error(f"Caught '{type.__name__}' exception: {value}") # Hook exception to log it
    
    with open(remindersFilePath, "r") as f:
            reminders = json.load(f)
    
    
    while True:
        commandInput = input(f"{commandPrefix} ")
        command = commandInput.split(" ")
        commandName = command[0]
        commandArgs = command.pop(0)
        
        # Executed after every command to get up to date json file 
        with open(remindersFilePath, "r") as f:
            remindersJson = json.load(f)
        
        match commandName:
            case "exit":
                exit()
            case "reminders":
                for reminderName,reminderData in remindersJson.items():
                    reminderTitle = reminderData["title"]
                    reminderMessage = reminderData["message"]
                    reminderTime = reminderData["time"]
                    print(f"{bold}{Fore.BLUE}{reminderName}:{reset} {Fore.BLUE}{{{Fore.RED}title=\"{reset}{reminderTitle}{Fore.RED}\", {Fore.YELLOW}message=\"{reset}{reminderMessage}{Fore.YELLOW}\", {Fore.GREEN}time=\"{reset}{reminderTime}{Fore.GREEN}\"{Fore.BLUE}}}{reset}")
            case "clear":
                os.system("clear")
            case "create":
                name = input(f"Name {commandPrefix} ")
                title = input(f"Title {commandPrefix} ")
                message = input(f"Message {commandPrefix} ")
                time = input(f"Time {commandPrefix} ")
                
                newReminder = reminderObjFormat
                newReminder["title"] = title
                newReminder["message"] = message
                newReminder["time"] = time
                
                reminders[name] = newReminder
            case "save":
                with open(remindersFilePath, "w") as f:
                    json.dump(reminders, f)
            case _:
                logger.error(f"Command \"{commandInput}\" is not a command.")
                
if __name__ == "__main__":
    main()