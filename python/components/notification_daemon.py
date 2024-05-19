from plyer import notification
import datetime
import time
import sys
import json
import os

match sys.platform:
    case "darwin":
        remindersFilePath = os.path.join(os.path.expanduser("~"), ".config", "Reminders", "reminders.json")
    case "win32":
        remindersFilePath = os.path.join(os.getenv("LOCALAPPDATA"), "Reminders", "reminders.json")
    case "linux":
        remindersFilePath = os.path.join(os.path.expanduser("~"), ".config", "Reminders", "reminders.json")
        

if __name__ == "__main__":
    import log
else:
    import python.components.log as log



def fixNotificationsTime(notifications):
        for notificationData in notifications:
            oldTime = notificationData["time"]
            oldTime = oldTime.split(":")
            oldTimeH = oldTime[0]
            oldTimeM = oldTime[1]
            
            if oldTimeH[0] == "0":
                oldTimeH = oldTimeH[1]
                
            if len(oldTimeH) > 1:
                newTimeH = f"{oldTimeH[0]}{oldTimeH[1]}"
            else:
                newTimeH = f"{oldTimeH[0]}"
            
            if oldTimeM[0] == "0":
                oldTimeM = oldTimeM[1]
            
            if len(oldTimeM) > 1:
                newTimeM = f"{oldTimeM[0]}{oldTime[1]}"
            else:
                newTimeM = f"{oldTimeM[0]}"
                
            newTime = f"{newTimeH}:{newTimeM}"
            notificationData["time"] = newTime
    

def startDaemon():
    # Logging
    logName = __file__.split("/")[-1].removesuffix(".py")
    logFile = log.generateLogFile(logName)
    logger = log.newLogger(logName, logFile)
    log.addCounter(logger)
    sys.excepthook = lambda type, value, tb: logger.error(f"Caught '{type.__name__}' exception: {value}") # Hook exception to log it

    logger.info("Notification daemon started!")
    
    while True:
        # Loops every minute
        # Update reminders every minute
        with open(remindersFilePath, "r") as f:
            reminders = json.load(f)
        # Check if notification needs to be sent
        for reminderData in reminders.values():
            if reminderData["time"] == f"{datetime.datetime.now().hour}:{datetime.datetime.now().minute}":
                logger.info("Sending notification...")
                notification.notify(
                    title = reminderData["title"],
                    message = reminderData["message"],
                    app_name = "",
                    timeout = 10
                )
            else:
                continue
        
        # Sync time to minute
        timeNow = datetime.datetime.now()
        timeS = timeNow.second
        if timeS != 0:
            time.sleep(60 - timeS)
        else:
            time.sleep(60)
            
def main():
    startDaemon()

if __name__ == "__main__":
    main()