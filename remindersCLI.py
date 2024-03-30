from components.log import newLogger, addCounter, generateLogFile, flushLogs
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

def cli():
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
        command.pop(0)
        commandArgs = command # just an alias
        
        try:
            commandArgIndicies = []
            for i,commandArg in enumerate(commandArgs):
                if commandArg.startswith("\"") and commandArgs[i+1].endswith("\"") and commandArg != "\"\"": # If command argument 1 exists and starts with " and the if a command argument after that ends with ", 
                    commandArgIndicies.append(i)
                    
            if len(commandArgIndicies) >= 1:
                for i in commandArgIndicies:
                    commandArgPart1 = commandArgs[i]
                    commandArgPart2 = commandArgs[i+1]

                    commandArgs.pop(commandArgIndicies[i])
                    commandArgs.pop(commandArgIndicies[i])
                    
                    joinedCommandArg = f"{commandArgPart1} {commandArgPart2}".replace("\"", "")
                    commandArgs.insert(i, joinedCommandArg)
            else:
                pass
        except IndexError:
            pass
        
        commandArgsLen = len(commandArgs)
        
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
                if commandArgsLen >= 1:
                    name = commandArgs[0]
                    title = commandArgs[1]
                    message = commandArgs[2]
                    time = commandArgs[3]
                    
                    newReminder = reminderObjFormat.copy()
                    newReminder["title"] = title
                    newReminder["message"] = message
                    newReminder["time"] = time
                    
                    reminders[name] = newReminder
                elif commandArgsLen == 0:
                    name = input(f"Name {commandPrefix} ")
                    title = input(f"Title {commandPrefix} ")
                    message = input(f"Message {commandPrefix} ")
                    time = input(f"Time {commandPrefix} ")
                    
                    newReminder = reminderObjFormat.copy()
                    newReminder["title"] = title
                    newReminder["message"] = message
                    newReminder["time"] = time
                    
                    reminders[name] = newReminder
                    
            case "delete":
                if commandArgsLen >= 1:
                    reminderName = commandArgs[0]
                    if reminderName in reminders:
                        reminders.pop(reminderName)
                    elif reminderName == "all":
                        reminders.clear()
                    else:
                        logger.error(f"Reminder \"{reminderName}\" not found!")
                elif commandArgsLen == 0:
                    reminderName = input("Reminder to Delete > ")
                    if reminderName in reminders:
                        reminders.pop(reminderName)
                    else:
                        logger.error(f"Reminder \"{reminderName}\" not found!")
                        
            case "save":
                with open(remindersFilePath, "w") as f:
                    json.dump(reminders, f)
            case _:
                logger.error(f"Command \"{commandInput}\" is not a command.")
                
def main():
    cli()

if __name__ == "__main__":
    main()