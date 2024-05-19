import GeneralContext from '../contexts/generalContext'
import { useContext } from 'react';
import './navbar.css';

function Navbar() {
    const { togglePopupState } = useContext(GeneralContext);

    return (
        <header className="navbar" id="top_navbar">
            <div id="top_navbar_left">
                <div id={"title_wrapper"}>
                    <h1 id="title">Reminders.py</h1>
                    <p className={"unimportant-text"}>but it's built in react?</p>
                </div>
            </div>
            <div id={"top_navbar_center"}>
                <div id={"pages"}>
                </div>
            </div>
            <div id="top_navbar_right">
                <button className="button important-button" onClick={() => {
                    togglePopupState("save")

                }}><i className={"fi fi-sr-disk icon"}/></button>
                <button className="button important-button" onClick={() => {
                    togglePopupState("create")
                }}><i
                    className={"fi fi-br-plus icon"}/> <span className={"important-button-text"}>New Reminder</span>
                </button>
            </div>
        </header>
    );
}

export default Navbar;