import {useContext} from "react";
import popupContext from "../../contexts/generalContext";

function PopupDeleteConfirm (props) {
    const { reminders, setReminders, addToQueue, remindersJson, setRemindersJson, togglePopupState } = useContext(popupContext);

    function deleteReminder() {
        addToQueue({type: "delete", reminder: props.reminderToDelete.id});

        setReminders(reminders.filter(reminder => reminder.props.reminderId !== props.reminderToDelete.id));
        setRemindersJson(Object.fromEntries(Object.entries(remindersJson).filter(([key, value]) => key !== props.reminderToDelete.name)));
        togglePopupState(null);
    }

    return (
        <div className={"popup"} id={"deletePopup"}>
            <div id={"popupInfo"}>
                <h1 id={"popupTitle"}>Delete Confirmation</h1>
                <p id={"popupDescription"}>Are you sure you want to delete <span id={"reminderToDeleteName"}>{props.reminderToDelete.name}</span>?</p>
            </div>
            <div id={"popupActions"}>
                <button id={"popupDeleteButton"} className={"important-button button"} onClick={deleteReminder}>
                    <span className={"important-button-text"}>Delete</span></button>
                <button id={"popupCancelButton"} className={"button"} onClick={() => togglePopupState(null)}><span
                    className={"important-button-text"}>Cancel</span></button>
            </div>
        </div>
    );
}

export default PopupDeleteConfirm;