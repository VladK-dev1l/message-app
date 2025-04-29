import sys
import string
import random
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QFrame, QCheckBox, QScrollArea, QHBoxLayout
)
from PyQt6.QtCore import Qt


def generate_strong_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))


class ChatBubble(QWidget):
    def __init__(self, message, is_user=True):
        super().__init__()

        layout = QHBoxLayout()
        layout.setAlignment(
            Qt.AlignmentFlag.AlignLeft if is_user else Qt.AlignmentFlag.AlignRight)

        # Create the bubble and set the message
        bubble = QLabel(message)
        bubble.setWordWrap(True)

        # Set background colors for user and bot
        # Blue for user, Green for bot
        background_color = '#0a84ff' if is_user else '#2e8b57'
        bubble.setStyleSheet(f"""
            background-color: {background_color};
            color: white;
            padding: 12px;
            border-radius: 16px;
            font-size: 14px;
            font-family: 'Helvetica Neue', sans-serif;
        """)

        # Adjust the layout to allow flexible width
        # Limit width to 380px to fit the window size
        bubble.setMaximumWidth(380)

        layout.addWidget(bubble)
        self.setLayout(layout)


class ChatScreen(QWidget):
    def __init__(self, username):
        super().__init__()
        self.setStyleSheet("background-color: #0d0d0d;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll.setWidget(self.chat_container)

        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type a message...")
        self.message_input.setStyleSheet("""
            background-color: #2c2c2e;
            color: white;
            padding: 14px;
            border-radius: 14px;
            font-size: 15px;
            border: 1px solid #3a3a3c;
        """)
        self.message_input.returnPressed.connect(self.send_message)

        layout.addWidget(
            QLabel(f"<span style='color:white;'>Welcome, {username}!</span>"))
        layout.addWidget(self.scroll)
        layout.addWidget(self.message_input)

    def send_message(self):
        message = self.message_input.text().strip()  # Make sure this is the first line

        if not message:
            return

        # User message (now left side)
        user_bubble = ChatBubble(message, is_user=True)
        self.chat_layout.addWidget(user_bubble)

        # Simulate bot reply (right side)
        reply = f"Echo: {message}"
        bot_bubble = ChatBubble(reply, is_user=False)
        self.chat_layout.addWidget(bot_bubble)

        self.message_input.clear()
        self.scroll.verticalScrollBar().setValue(
            self.scroll.verticalScrollBar().maximum())


class LoginScreen(QWidget):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success
        self.setStyleSheet("background-color: #0d0d0d;")
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setContentsMargins(20, 40, 20, 20)

        header = QLabel("🕒 9:41     🔋100%")
        header.setStyleSheet(
            "color: #aaa; background-color: #1c1c1e; font-size: 12px; padding: 4px;")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header)

        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #1c1c1e;
                border-radius: 20px;
                padding: 30px;
                border: 1px solid #2a2a2c;
            }
        """)
        layout = QVBoxLayout(card)
        layout.setSpacing(20)

        title = QLabel("Create Account")
        title.setStyleSheet(
            "color: white; font-size: 22px; font-weight: bold; font-family: 'Helvetica Neue';")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet(self.input_style())
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet(self.input_style())
        layout.addWidget(self.password_input)

        self.show_password_checkbox = QCheckBox("Show Password")
        self.show_password_checkbox.setStyleSheet(
            "color: #bbb; font-size: 13px; font-family: 'Helvetica Neue';")
        self.show_password_checkbox.stateChanged.connect(
            self.toggle_password_visibility)
        layout.addWidget(self.show_password_checkbox)

        self.suggest_button = QPushButton("🔐 Suggest Strong Password")
        self.suggest_button.setStyleSheet(self.secondary_button_style())
        self.suggest_button.clicked.connect(self.suggest_password)
        layout.addWidget(self.suggest_button)

        self.login_button = QPushButton("✅ Create Account")
        self.login_button.setStyleSheet(self.primary_button_style())
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

        main_layout.addWidget(card)

    def input_style(self):
        return """
            QLineEdit {
                background-color: #2c2c2e;
                color: white;
                padding: 14px;
                border-radius: 14px;
                font-size: 16px;
                border: 1px solid #3a3a3c;
                font-family: 'Helvetica Neue';
            }
            QLineEdit:focus {
                border: 1px solid #007aff;
            }
        """

    def primary_button_style(self):
        return """
            QPushButton {
                background-color: #0a84ff;
                color: white;
                padding: 14px;
                border-radius: 14px;
                font-size: 16px;
                font-family: 'Helvetica Neue';
            }
            QPushButton:hover {
                background-color: #0060df;
            }
        """

    def secondary_button_style(self):
        return """
            QPushButton {
                background-color: #2a2a2c;
                color: #ddd;
                padding: 12px;
                border-radius: 12px;
                font-size: 14px;
                font-family: 'Helvetica Neue';
            }
            QPushButton:hover {
                background-color: #3a3a3c;
            }
        """

    def toggle_password_visibility(self, state):
        if state == 2:  # 2 means Checked
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

    def suggest_password(self):
        self.password_input.setText(generate_strong_password())

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        if username and password:
            self.on_login_success(username)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("iPhone Style Chat App")
        self.setFixedSize(390, 844)  # iPhone 13 aspect ratio
        self.setCentralWidget(LoginScreen(self.open_chat))

    def open_chat(self, username):
        self.setCentralWidget(ChatScreen(username))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
