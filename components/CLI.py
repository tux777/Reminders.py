commands = {
    "exit": {"needsFlags": False, "flags": None},
    
    "save": {"needsFlags": False, "flags": None},
    
    "reminders": {"needsFlags": False, "flags": {
        "-advanced": {"minArgAmount": 0, "maxArgAmount": 0}
    }},
    
    "create": {"needsFlags": False, "flags": {
        "-name": {"minArgAmount": 1, "maxArgAmount": 1}, 
        "-title": {"minArgAmount": 1, "maxArgAmount": 1}, 
        "-message": {"minArgAmount": 1, "maxArgAmount": 1}, 
        "-time": {"minArgAmount": 1, "maxArgAmount": 1}
    }},
    
    "delete": {"needsFlags": False, "flags": {
        "-name": {"minArgAmount": 1, "maxArgAmount": 1},
        "-all": {"minArgAmount": 0, "maxArgAmount": 0}
    }},
}

# Command class errors

class CLIException(Exception):
    pass

class CommandNotFound(CLIException):
    def __init__(self, cmd):
        super().__init__(f"Command \"{cmd}\" is not a command!")

# Reminder is not found error
class ReminderNotFound(CLIException):
    def __init__(self, reminder):
        super().__init__(f"Reminder \"{reminder}\" not found!")

class InvalidArgument(CLIException):
    def __init__(self, reason):
        super().__init__(f"Argument is not valid! {reason}")

class NoFlagArgumentLink(CLIException):
    def __init__(self, flag):
        super().__init__(f"Flag \"{flag}\" has no argument linked to it!")

class InvalidFlag(CLIException):
    def __init__(self, flag):
        super().__init__(f"Flag \"{flag}\" is not a valid flag!")
        
class maxFlagArgsExceded(CLIException):
    def __init__(self, flag, maxArgAmount):
        super().__init__(f"Flag \"{flag}\" can only take {maxArgAmount} arguments!")

# Used each time a command is executed in the CLI
class command():
    def __init__(self, rawCommand: str) -> None:
        argsSplit = rawCommand.split(" ")
        self.__raw = rawCommand
        self.__command = argsSplit[0]
        argsSplit.pop(0) # Get rid of the command, just the args.

        if self.__command not in commands:
            raise CommandNotFound(self.__command)
        
        # Command args parser
        args = {}
        
        # Cannot use for loop because argsSplit is being modified after each iteration, I can't set the iterator in a for loop.
        i = 0
        n = len(argsSplit)
        while i < n:
            arg = argsSplit[i]
            if arg.startswith('"') and arg != '""':
                if arg.endswith('"'): # If arg is just one word with quotes
                    argsSplit[i] = arg.replace('"', "")
                    i += 1
                    continue
                else:  # else if arg is multiple words with spaces
                    foundEndOfArgs = False
                    onArg = i
                    argsFound = {}
                    while foundEndOfArgs == False:
                        try:
                            if onArg == i:
                                argsFound[f"{onArg}"] = argsSplit[onArg]
                                onArg += 1
                                continue
                            else:
                                if argsSplit[onArg].endswith('"'):
                                    argsFound[f"{onArg}"] = argsSplit[onArg]
                                    foundEndOfArgs = True
                                elif argsSplit[onArg].startswith('"'):
                                    raise InvalidArgument(f"Could not find end of argument {i}!")
                                else:
                                    argsFound[f"{onArg}"] = argsSplit[onArg]
                                    onArg+=1
                            
                        except Exception:
                            raise InvalidArgument(f"Could not find end of argument {i}!")
                    
                    argsSplit = argsSplit[:i+1] + argsSplit[int(list(argsFound.keys())[-1])+1:] # Slice everything past the first arg (with quote) and then slice everything, including the last arg (with quote) and before. Then join the list together to make a new list of argsSplit
                    argsSplit[i] = " ".join(argsFound.values()).replace('"', "") # Set the first arg (with quote) to the joined values of the argsFound, then remove the quotes surrounding them
                    n -= (int(list(argsFound.keys())[-1])+1) - (i+1) # Subtract the amount of args removed from the total amount of args to give the new length of argsSplit
            else:
                i += 1

        
        # Flag parser
        for i,arg in enumerate(argsSplit):
            if arg.startswith("-"):
                flag = arg      
                if flag not in commands[self.__command]["flags"]:
                    raise InvalidFlag(flag)
                else:
                    args[flag] = []
                    if commands[self.__command]["flags"][flag]["minArgAmount"] > 0:
                        # if next arg doesn't exist and flag requires one ore more arguments, raise error
                        try:
                            if argsSplit[i+1].startswith("-"): # if flag requires one ore more argument and next arg is a flag, raise error
                                raise NoFlagArgumentLink(flag)
                            else:
                                for j in range(argsSplit.index(flag)+1, len(argsSplit)):  # loop through argsSplit starting from the index of the flag to get all the arguments for the flag
                                    if argsSplit[j].startswith("-"):
                                        break # finished, got all args for flag
                                    else:
                                        args[flag].append(argsSplit[j])
                                        
                                if len(args[flag]) > commands[self.__command]["flags"][flag]["maxArgAmount"]: # if the amount of arguments for the flag is greater than the max amount of arguments the flag can take, raise error
                                    raise InvalidArgument(f"Flag \"{flag}\" can only take {commands[self.__command]['flags'][flag]['maxArgAmount']} arguments!")
                        except IndexError:
                            raise NoFlagArgumentLink(flag)    
                    else:
                        try:
                            invalidFlagArg = argsSplit[i+1]
                            if invalidFlagArg.startswith("-"):
                                args[flag] = None
                            else:
                                raise InvalidArgument(f"Flag \"{flag}\" doesn't take any arguments!")
                        except IndexError:
                            args[flag] = None
                        
                                
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