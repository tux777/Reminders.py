import {v4} from "uuid";
import popupContext from "../contexts/generalContext";
import './reminder.css';
import {useContext} from "react";

function Reminder (props) {
    const { setPopupState, setPopupType, setReminderToDelete } = useContext(popupContext);
    const reminderName = props.reminderName;
    const reminderId = props.reminderId;

    return (
        <li className={"reminder"} key={reminderId}>
            <div className={"reminderInfo"}>
                <h2 className={"reminderTitle"}>{reminderName}</h2>
                <p className={"reminderDescription"}><span className={"descriptionPrefix unimportant-text"}>Remind me to:</span> {props.reminderDescription}</p>
            </div>
            <div className={"reminderActions"}>
                <button className={"button"} onClick={() => {
                    setPopupType("delete");
                    setReminderToDelete({name: reminderName, id: reminderId});
                    setPopupState(true);
                }}><i className={"fi fi-sr-trash icon"}></i></button>
                <button className={"button"}><i className={"fi fi-br-menu-burger icon"}></i></button>
            </div>
        </li>
    );
}

export default Reminder;