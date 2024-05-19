import {useContext} from "react";
import generalContext from "../../contexts/generalContext";

function PopupError() {
    const { togglePopupState, okDisabled, errorMsg } = useContext(generalContext);
    let okButton;
    let okDisabledClass;

    if (okDisabled === true) {
        okButton = <button id={"popupOkButton"} className={"important-button button okDisabled"} disabled>
            <span className={"important-button-text"}>Ok</span></button>
    } else {
        okButton = <button id={"popupOkButton"} className={"important-button button"} onClick={() => togglePopupState(null)}>
            <span className={"important-button-text"}>Ok</span></button>
    }

    return (
        <div className={`popup`} id={"errorPopup"}>
            <div id={"popupInfo"}>
                <h1 id={"popupTitle"}>Error</h1>
                <p id={"popupDescription"}>{errorMsg}</p>
            </div>
            <div id={"popupActions"}>
                {okButton}
            </div>
        </div>
    );
}

export default PopupError;