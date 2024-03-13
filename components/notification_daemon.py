from components.logging import generateLogFile, newLogger, addCounter
from plyer import notification
import datetime
import time

def startDaemon():
    # Logging
    logFile = generateLogFile(__name__)
    logger = newLogger(__name__, logFile)
    addCounter(logger)

    logger.info("Notification daemon started!")

    notifications = []
    for notificationData in notifications:
        oldTime = notificationData["time"]
        oldTime = oldTime.split(":")
        oldTimeH = oldTime[0]
        oldTimeM = oldTime[1]
        
        if oldTimeH[0] == 0:
            oldTimeH.pop(0)
            
        if len(oldTimeH) > 1:
            newTimeH = f"{oldTimeH[0]}{oldTimeH[1]}"
        else:
            newTimeH = f"{oldTimeH[0]}"
        
        if oldTimeM[0] == 0:
            oldTimeM.pop(0)
        
        if len(oldTimeM) > 1:
            newTimeM = f"{oldTimeM[0]}{oldTime[1]}"
        else:
            newTimeM = f"{oldTimeM[0]}"
        
    
    while True:
        # Check if notification needs to be sent
        for notificationData in notifications:
            if notificationData["time"] == f"{datetime.datetime.now().hour}:{datetime.datetime.now().minute}":
                logger.info("Sending notification...")
                notification.notify(
                    title = notificationData["title"],
                    message = notificationData["message"],
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

if __name__ == "__main___":
    main()