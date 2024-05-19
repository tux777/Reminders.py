import { v4 } from "uuid";
import { useState, useEffect } from 'react';
import './App.css';
import Navbar from './components/navbar/navbar';
import Reminder from './components/reminder/reminder';
import Popup from './components/popup/popup';
import NoReminders from "./components/reminder/noReminders";
import GeneralContext from "./components/contexts/generalContext";

function App() {
    const [remindersJson, setRemindersJson] = useState([]); // [name: message
    const [reminders, setReminders] = useState([]);
    const [popupState, setPopupState] = useState(false);
    const [popupType, setPopupType] = useState("confirmation");
    const [reminderToDelete, setReminderToDelete] = useState("");
    const [queue, setQueue] = useState([]);
    const [okDisabled, setOkDisabled] = useState(false);
    const [errorMsg, setErrorMsg] = useState("");

    function addToQueue(item) {
        let newQueue = queue;
        newQueue.push(item);
        setQueue(newQueue);
    }

    function togglePopupState(popupType) {
        setPopupType(popupType)
        setPopupState(!popupState);
    }

    function convertJSONToReminders(jsonObj) {
        let reminders = [];

        Object.keys(jsonObj).forEach((key, i) => {
            const name = key;
            const dataValues = Object.values(jsonObj)[i];
            const id = v4();
            reminders.push(<Reminder reminderName={name} reminderId={id} key={id} reminderDescription={dataValues.message}/>);
        })

        return reminders;
    }

    function error(errMsg, okIsDisabled) {
        console.error(errMsg);
        setOkDisabled(okIsDisabled);
        setErrorMsg(errMsg);
        togglePopupState("error");
    }

    function fetchReminders() {
        return fetch('http://localhost:4000/reminders')
            .then(response => {
                return response.json().then(data => {
                    return data;
                }).catch(err => {
                    error("Error parsing JSON: " + err, false);
                });
            })
    }

    useEffect(() => {
        fetchReminders().then(data => {
            setRemindersJson(data);
            setReminders(convertJSONToReminders(data));
        }).catch(err => {
            error("Error fetching reminders: " + err, true);
        });
    }, []);

    useEffect(() => {
        setReminders(convertJSONToReminders(remindersJson));
    }, [remindersJson])

    window.onbeforeunload = () => {
        if (queue.length > 0) {
            return "You have unsaved changes. Are you sure you want to leave?";
        } else {

        }
    }

    return (
        <GeneralContext.Provider value={{popupState, setPopupState, popupType, setPopupType, reminderToDelete, setReminderToDelete, addToQueue, setQueue, queue, reminders, setReminders, remindersJson, setRemindersJson, togglePopupState, okDisabled, errorMsg}}>
            <div className="App">
                <div id={"main"}>
                    <Navbar/>
                    <NoReminders/>
                    <ul id={"remindersWrapper"}>
                        {reminders}
                    </ul>
                </div>
                <Popup/>
            </div>
        </GeneralContext.Provider>

    );
}

export default App;