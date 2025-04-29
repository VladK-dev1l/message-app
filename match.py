import random
import string
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QLabel, QScrollArea, QFrame, QSizePolicy, QStackedLayout, QCheckBox
)
from PyQt6.QtCore import Qt


def generate_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))


class ChatBubble(QFrame):
    def __init__(self, sender, message, is_user=True):
        super().__init__()
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {'#2196F3' if is_user else '#1565C0'};
                border-radius: 20px;
                padding: 10px;
            }}
            QLabel {{
                color: white;
                font-size: 14px;
            }}
        """)
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(3)

        sender_label = QLabel(f"<b>{sender}</b>")
        message_label = QLabel(message)
        message_label.setWordWrap(True)

        layout.addWidget(sender_label)
        layout.addWidget(message_label)
        self.setLayout(layout)

        self.setSizePolicy(QSizePolicy.Policy.Maximum,
                           QSizePolicy.Policy.Minimum)


class LoginScreen(QWidget):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success
        self.setStyleSheet("background-color: #121212;")
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 100, 50, 50)
        layout.setSpacing(20)

        title = QLabel("Create Account")
        title.setStyleSheet("color: white; font-size: 20px;")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border-radius: 10px;
                background-color: #1e1e1e;
                color: white;
                border: 1px solid #333;
            }
        """)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.show_password_checkbox = QCheckBox("Show Password")
        self.show_password_checkbox.setStyleSheet("color: white;")
        self.show_password_checkbox.stateChanged.connect(
            self.toggle_password_visibility)
        self.password_input.setStyleSheet(self.username_input.styleSheet())
        self.suggest_button = QPushButton("Suggest Password")
        self.suggest_button.setStyleSheet("""
            QPushButton {
                background-color: #333;
                color: white;
                padding: 8px;
                border-radius: 10px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #444;
            }
        """)
        self.suggest_button.clicked.connect(self.suggest_password)

        self.login_button = QPushButton("Create Account")
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d7;
                color: white;
                padding: 10px;
                border-radius: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #005bb5;
            }
        """)
        self.login_button.clicked.connect(self.handle_login)

        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.show_password_checkbox)
        layout.addWidget(self.login_button)
        layout.addWidget(self.suggest_button)

        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if username and password:
            self.on_login_success(username)

    def suggest_password(self):
        suggested = generate_password()
        self.password_input.setText(suggested)

    def toggle_password_visibility(self, state):
        if state == Qt.CheckState.Checked.value:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)


class MessagingApp(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setStyleSheet("background-color: #121212;")
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: none;")

        self.chat_widget = QWidget()
        self.chat_layout = QVBoxLayout()
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.chat_widget.setLayout(self.chat_layout)

        self.scroll_area.setWidget(self.chat_widget)
        main_layout.addWidget(self.scroll_area)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type your message...")
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: #1e1e1e;
                color: white;
                padding: 12px;
                border-radius: 20px;
                border: 1px solid #333;
                font-size: 14px;
            }
        """)
        self.input_field.returnPressed.connect(self.send_message)

        self.send_button = QPushButton("Send")
        self.send_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d7;
                color: white;
                padding: 12px 20px;
                border-radius: 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #005bb5;
            }
        """)
        self.send_button.clicked.connect(self.send_message)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)

        main_layout.addLayout(input_layout)
        self.setLayout(main_layout)

    def send_message(self):
        message = self.input_field.text().strip()
        if not message:
            return

        self.add_chat_bubble(self.username, message, is_user=True)
        self.input_field.clear()

        bot_reply = f"Echo: {message}"
        self.add_chat_bubble("Bot", bot_reply, is_user=False)

    def add_chat_bubble(self, sender, message, is_user=True):
        bubble = ChatBubble(sender, message, is_user)
        container = QHBoxLayout()

        # Flip: user = left, bot = right
        if is_user:
            container.setAlignment(Qt.AlignmentFlag.AlignLeft)
            container.addWidget(bubble)
            container.addStretch()
        else:
            container.setAlignment(Qt.AlignmentFlag.AlignRight)
            container.addStretch()
            container.addWidget(bubble)

        wrapper = QWidget()
        wrapper.setLayout(container)

        self.chat_layout.addWidget(wrapper)
        self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum())


class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat App with Account Creation")
        self.setGeometry(100, 100, 500, 600)

        self.stack = QStackedLayout()
        self.setLayout(self.stack)

        self.login_screen = LoginScreen(self.start_chat)
        self.stack.addWidget(self.login_screen)

    def start_chat(self, username):
        self.chat_window = MessagingApp(username)
        self.stack.addWidget(self.chat_window)
        self.stack.setCurrentWidget(self.chat_window)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
