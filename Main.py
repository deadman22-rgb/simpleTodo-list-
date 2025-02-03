import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QMouseEvent

class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedHeight(28)  # Reduced height for better proportions
        self.setStyleSheet("background: transparent; color: white;")  # Transparent to blend with gradient
        
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 0, 10, 0)
        
        self.title_label = QLabel("To-Do List")
        self.title_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.title_label)
        layout.addStretch()
        
        self.minimize_btn = QPushButton("−")
        self.minimize_btn.clicked.connect(parent.showMinimized)
        
        self.maximize_btn = QPushButton("⬜")
        self.maximize_btn.clicked.connect(self.toggle_maximize)
        
        self.close_btn = QPushButton("✕")
        self.close_btn.clicked.connect(parent.close)
        
        for btn in [self.minimize_btn, self.maximize_btn, self.close_btn]:
            btn.setFixedSize(25, 25)
            btn.setStyleSheet("background: transparent; color: white; border: none;")
            layout.addWidget(btn)
        
        self.setLayout(layout)
        self.old_pos = None
        self.parent_window = parent
        self.is_maximized = False
    
    def toggle_maximize(self):
        if self.is_maximized:
            self.parent_window.showNormal()
        else:
            self.parent_window.showMaximized()
        self.is_maximized = not self.is_maximized
    
    def mousePressEvent(self, event: QMouseEvent):
        self.old_pos = event.globalPosition().toPoint()
    
    def mouseMoveEvent(self, event: QMouseEvent):
        if self.old_pos is not None and not self.is_maximized:
            delta = QPoint(event.globalPosition().toPoint() - self.old_pos)
            self.parent().move(self.parent().x() + delta.x(), self.parent().y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        self.old_pos = None

class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setGeometry(100, 100, 400, 500)
        
        self.layout = QVBoxLayout()
        self.title_bar = CustomTitleBar(self)
        self.layout.addWidget(self.title_bar)
        
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter a new task...")
        self.layout.addWidget(self.task_input)
        
        self.add_button = QPushButton("Add Task")
        self.add_button.clicked.connect(self.add_task)
        self.layout.addWidget(self.add_button)
        
        self.task_list = QListWidget()
        self.task_list.setStyleSheet("QScrollBar:vertical { width: 6px; background: transparent; border-radius: 3px; }")  # Minimalist scrollbar
        self.layout.addWidget(self.task_list)
        
        self.delete_button = QPushButton("Delete Completed Tasks")
        self.delete_button.clicked.connect(self.delete_task)
        self.layout.addWidget(self.delete_button)
        
        self.setLayout(self.layout)
        self.setStyleSheet(self.get_styles())
    
    def add_task(self):
        task_text = self.task_input.text().strip()
        if task_text:
            item = QListWidgetItem(task_text)
            item.setCheckState(Qt.CheckState.Unchecked)
            item.setFont(self.bold_font())
            self.task_list.addItem(item)
            self.task_input.clear()
    
    def delete_task(self):
        for i in range(self.task_list.count() - 1, -1, -1):
            item = self.task_list.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                self.task_list.takeItem(i)
    
    def get_styles(self):
        return """
        QWidget {
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #0D1117, stop:1 #121826);
            color: white;
        }
        QLineEdit, QListWidget {
            background-color: rgba(255, 255, 255, 0.12);
            border-radius: 8px;
            padding: 5px;
        }
        QPushButton {
            background-color: #2563EB;
            border-radius: 8px;
            padding: 6px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #1E40AF;
        }
        QListWidget::item {
            background-color: rgba(255, 255, 255, 0.12);
            border-radius: 8px;
            font-weight: bold;
            padding: 6px;
        }
        """
    
    def bold_font(self):
        font = self.font()
        font.setBold(True)
        return font

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToDoApp()
    window.show()
    sys.exit(app.exec())
