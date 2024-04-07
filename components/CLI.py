# Used each time a command is executed in the CLI 
class command():
    def __init__(self, rawCommand: str) -> None:
        self.__raw = rawCommand 
        argsSplit = rawCommand.split(" ")
        self.__command = argsSplit[0]
        
        # Command args parser
        args = {}
        filteredQuoteArgs = list(filter(lambda x: '"' in x, argsSplit))
        
        for i,arg in enumerate(filteredQuoteArgs):
            try:
                if arg.startswith('"') and filteredQuoteArgs[i+1].endswith('"') and arg != '""':
                    parsedArg1 = arg.replace('"', "")
                    parsedArg2 = filteredQuoteArgs[i+1].replace('"', "") # get 2nd part of the arg and then filter like 1st part of arg
                    parsedArg = f"{parsedArg1} {parsedArg2}" # Finally concatenate the two parts together and insert the whitespace
                    
                    for j,arg in enumerate(argsSplit):
                        try:
                            arg.index(parsedArg1) 
                            argsSplit[j] = parsedArg
                            argsSplit.pop(j+1)
                        except:
                            continue
            except IndexError: # Reached the end of the quoted args and so the parsing is almost done. Parse the last arg then break the loop to finish parsing
                parsedArg = arg.replace('"', "")
                
                for j,arg in enumerate(argsSplit):
                    try:
                        arg.index(parsedArg) 
                        argsSplit[j] = parsedArg
                        argsSplit.pop(j+1)
                    except:
                        continue
                    
                break
        
        filteredFlagArgs = filter(lambda x: '-' in x, argsSplit)
        for flag in filteredFlagArgs:
            for i,arg in enumerate(argsSplit):
                if arg == flag:
                    try:
                        flagValue = argsSplit[i+1]
                        if flagValue.startswith('-'):
                            continue
                        else:
                            args[flag] = flagValue
                    except IndexError:
                        continue
        
        self.__args = args    
        self.__argsLen = len(args)
    
    @property    
    def command(self):
        return self.__command
    
    @property
    def args(self):
        return self.__args
    
    @property
    def argsLen(self):
        return self.__argsLen

# Command is not found error
class CommandNotFound(Exception):
    def __init__(self, message):
        super().__init__(f"Command \"{message}\" is not a command!")
        
# Reminder is not found error
class ReminderNotFound(Exception):
    def __init__(self, message):
        super().__init__(f"Reminder \"{message}\" not found!")