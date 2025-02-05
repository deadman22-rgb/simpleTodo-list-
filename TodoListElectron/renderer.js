const { ipcRenderer } = require('electron');

const taskInput = document.getElementById('taskInput');
const taskList = document.getElementById('taskList');
const addTaskBtn = document.getElementById('addTaskBtn');
const deleteCompletedBtn = document.getElementById('deleteCompletedBtn');
const minimizeBtn = document.getElementById('minimize');
const closeBtn = document.getElementById('close');

// Event Listeners
addTaskBtn.addEventListener('click', addTask);
taskInput.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
        addTask();
    }
});
deleteCompletedBtn.addEventListener('click', deleteCompletedTasks);

// Electron Window Controls
minimizeBtn.addEventListener('click', () => ipcRenderer.send('minimize'));
closeBtn.addEventListener('click', () => ipcRenderer.send('close'));

// Load tasks from localStorage on startup
document.addEventListener('DOMContentLoaded', loadTasks);

function addTask() {
    if (taskInput.value.trim() === "") return;

    let li = document.createElement('li');
    li.textContent = taskInput.value;
    li.addEventListener('click', toggleCompletion);
    taskList.appendChild(li);

    saveTasks();
    taskInput.value = "";
}

function toggleCompletion(event) {
    event.currentTarget.classList.toggle('completed');
    saveTasks();
}

function deleteCompletedTasks() {
    document.querySelectorAll('.completed').forEach(task => task.remove());
    saveTasks();
}

// Save tasks to localStorage
function saveTasks() {
    const tasks = [];
    document.querySelectorAll('#taskList li').forEach(li => {
        tasks.push({ text: li.textContent, completed: li.classList.contains('completed') });
    });
    localStorage.setItem('tasks', JSON.stringify(tasks));
}

// Load tasks from localStorage
function loadTasks() {
    const savedTasks = JSON.parse(localStorage.getItem('tasks')) || [];
    savedTasks.forEach(task => {
        let li = document.createElement('li');
        li.textContent = task.text;
        if (task.completed) li.classList.add('completed');
        li.addEventListener('click', toggleCompletion);
        taskList.appendChild(li);
    });
}
