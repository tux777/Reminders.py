import {useContext} from "react";
import generalContext from "../contexts/generalContext";

function NoReminders() {
    const { reminders } = useContext(generalContext);

    if (reminders.length === 0) {
        return (
            <div id={"noReminders"}>
                <h1 id={"noRemindersText"}>No Reminders</h1>
            </div>
        )
    } else {
        return null;
    }
}

export default NoReminders;