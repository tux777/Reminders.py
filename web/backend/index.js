const express = require('express');
const cors = require('cors');
const fs = require('fs').promises;
const os = require('os');
const process = require('process');
const path = require('path');

const app = express();

var corsOptions = {
    origin: 'https://localhost:3000',
    optionsSuccessStatus: 200 // some legacy browsers (IE11, various SmartTVs) choke on 204
}

app.use(cors());
app.use(express.json());

const osName = os.platform();

switch (osName) {
    case "linux":
        var remindersFilePath = path.join(os.homedir(), '.config', 'Reminders', 'reminders.json')
        break;
    case "darwin":
        var remindersFilePath = path.join(os.homedir(), '.config', 'Reminders', 'reminders.json')
        break;
    case "win32":
        var remindersFilePath = path.join(path.join(os.homedir(), "AppData", "local"), 'Reminders', 'reminders.json')
        break;
    default:
        console.error(`Unsupported OS: ${os}`)
        break;
}

let reminders;

const loadReminders = async () => {
    try {
        const data = await fs.readFile(remindersFilePath, 'utf8');
        reminders = JSON.parse(data);
    } catch (err) {
        console.error(err);
    }
}

const writeReminders = async() => {
    try {
        await fs.writeFile(remindersFilePath, JSON.stringify(reminders));
    } catch (err) {
        console.error(err);
    }
}

const port = 4000
const server = app.listen(port, () => {
    console.log(`Server running on port ${port}`)
})

app.get('/reminders', (req, res) => {
    loadReminders().then(r => {
        res.json(reminders);
    });
})

app.post('/remindersWrite', (req, res) => {
    reminders = req.body;

    writeReminders().then(r => {
        res.send('Reminders saved');
    });
})