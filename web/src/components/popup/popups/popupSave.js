import { useContext } from "react";
import popupContext from "../../contexts/generalContext";

function PopupSave (props) {
    const { remindersJson, setQueue, togglePopupState } = useContext(popupContext);

    function saveReminders() {
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
            .then(() => {
                setQueue([])
            })
            .catch(err => {
                console.error("Error saving reminders: " + err);
            });

    }

    return (
        <div className={"popup"} id={"savePopup"}>
            <div id={"popupInfo"}>
                <h1 id={"popupTitle"}>Save Reminders</h1>
                <p id={"popupDescription"}>Would you like to save your reminders?</p>
                <p id={"popupWarning"}>saving your reminders will clear your queue of undos and redos</p>
            </div>
            <div id={"popupActions"}>
                <button id={"popupSaveButton"} className={"important-button button"} onClick={() => {
                    togglePopupState(null)
                    saveReminders()
                }}><i
                    className={"fi fi-sr-disk"}/><span className={"important-button-text"}>Save</span></button>
                <button id={"popupCancelButton"} className={"button"} onClick={togglePopupState}><span
                    className={"important-button-text"}>Cancel</span></button>
            </div>
        </div>
    );
}

export default PopupSave;