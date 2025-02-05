const { app, BrowserWindow, ipcMain } = require('electron');

let mainWindow;

app.whenReady().then(() => {
    mainWindow = new BrowserWindow({
        width: 400,
        height: 550,
        frame: false, // Removes Electron's default window frame
        transparent: true, // Enables full UI control
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    mainWindow.loadFile('index.html');
});

// Listen for minimize & close events from renderer
ipcMain.on('minimize', () => {
    if (mainWindow) mainWindow.minimize();
});

ipcMain.on('close', () => {
    if (mainWindow) mainWindow.close();
});
