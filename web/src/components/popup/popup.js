import './popup.css'
import popupContext from "../contexts/generalContext";
import PopupSave from "./popups/popupSave";
import PopupDeleteConfirm from "./popups/popupDeleteConfirm";
import PopupCreate from "./popups/popupCreate";
import PopupError from "./popups/popupError";
import {useContext} from "react";

function Popup() {
    const { popupState, setPopupState, popupType, reminderToDelete } = useContext(popupContext);

    if (popupState === false) {
        return null;
    } else {
        switch (popupType) {
            default:
                return null
            case 'create':
                return (
                    <div id={"popupWrapper"}>
                        <PopupCreate />
                    </div>
                );
            case 'save':
                return (
                    <div id={"popupWrapper"}>
                        <PopupSave popupState={popupState} setPopupState={setPopupState}/>
                    </div>
                );
            case 'delete':
                return (
                    <div id={"popupWrapper"}>
                        <PopupDeleteConfirm reminderToDelete={reminderToDelete}/>
                    </div>
                );
            case 'error':
                return (
                    <div id={"popupWrapper"}>
                        <PopupError/>
                    </div>
                );
        }
    }
}

export default Popup;