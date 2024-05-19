import { useContext } from "react";
import popupContext from "../../contexts/generalContext";

function PopupCreate() {
    const { remindersJson, setRemindersJson, togglePopupState } = useContext(popupContext);

    function createReminder(reminderName, notificationTitle, notificationMessage, time) {
        const reminderJson = {
            [reminderName]: {"title": notificationTitle, "message": notificationMessage, "time": time}
        }

        setRemindersJson({...remindersJson, ...reminderJson});

        const options = {
            'method': 'POST',
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': JSON.stringify(remindersJson)
        }

        fetch('http://localhost:4000/remindersWrite', options)
            .then(response => {
                togglePopupState(null);
            })
            .catch(err => {
                console.error("Error saving reminders: " + err);
            });

        togglePopupState(null)
    }

    return (
        <div className={"popup"} id={"createPopup"}>
            <div id={"popupInfo"}>
                <h1 id={"popupTitle"}>Create Reminder</h1>
                <input className={"input popupInput"} id={"reminderName"} placeholder={"Reminder Name"}></input>
                <input className={"input popupInput"} id={"notificationTitle"} placeholder={"Notification Title"}></input>
                <input className={"input popupInput"} id={"notificationMessage"} placeholder={"Notification Message (reminder message)"}></input>
                <input className={"input popupInput"} id={"time"} placeholder={"Time"}></input>
            </div>
            <div id={"popupActions"}>
            <button id={"popupCreateButton"} className={"important-button button"} onClick={() => {
                    createReminder(document.getElementById("reminderName").value, document.getElementById("notificationTitle").value, document.getElementById("notificationMessage").value, document.getElementById("time").value)
                }}><i
                    className={"fi fi-br-plus"}/><span className={"important-button-text"}>Create</span></button>
                <button id={"popupCancelButton"} className={"button"} onClick={togglePopupState}><span
                    className={"important-button-text"}>Cancel</span></button>
            </div>
        </div>
    );

}

export default PopupCreate;