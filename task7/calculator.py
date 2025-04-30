import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QLineEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class CalculatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("iPhone 스타일 계산기")
        self.setFixedSize(320, 480)
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: black;")

        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.display.setText("0")
        self.display.setStyleSheet("""
            background-color: black;
            color: white;
            border: none;
        """)
        self.display.setFont(QFont("Arial", 30))
        self.display.setFixedHeight(80)

        buttons = [
            ["AC", "±", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "="]
        ]

        grid = QGridLayout()
        for row, texts in enumerate(buttons):
            for col, text in enumerate(texts):
                button = QPushButton(text)
                button.setFont(QFont("Arial", 20))
                button.setFixedSize(70, 70)

                if text in ["AC", "±", "%"]:
                    button.setStyleSheet("background-color: gray; color: black; border-radius: 35px;")
                elif text in ["÷", "×", "-", "+", "="]:
                    button.setStyleSheet("background-color: orange; color: white; border-radius: 35px;")
                else:
                    button.setStyleSheet("background-color: #222222; color: white; border-radius: 35px;")

                # 버튼별 메소드 연결
                if text == "AC":
                    button.clicked.connect(self.reset)
                elif text == "±":
                    button.clicked.connect(self.toggle_sign)
                elif text == "%":
                    button.clicked.connect(self.percent)
                elif text == "+":
                    button.clicked.connect(self.add)
                elif text == "-":
                    button.clicked.connect(self.subtract)
                elif text == "×":
                    button.clicked.connect(self.multiply)
                elif text == "÷":
                    button.clicked.connect(self.divide)
                elif text == "=":
                    button.clicked.connect(self.equal)  # 여기만 변경됨
                else:
                    button.clicked.connect(self.on_button_click)

                if row == 4:
                    if text == "0":
                        button.setFixedSize(150, 70)
                        grid.addWidget(button, 5, 0, 1, 2)
                    elif text == ".":
                        grid.addWidget(button, 5, 2)
                    elif text == "=":
                        grid.addWidget(button, 5, 3)
                else:
                    grid.addWidget(button, row + 1, col)

        layout = QVBoxLayout()
        layout.addWidget(self.display)
        layout.addLayout(grid)
        layout.setSpacing(10)
        self.setLayout(layout)

    # 숫자 및 소수점 처리
    def on_button_click(self):
        sender = self.sender()
        text = sender.text()
        current = self.display.text()

        if text == ".":
            import re
            tokens = re.split(r"[+\-×÷]", current)
            last_token = tokens[-1]
            if "." in last_token:
                return
            else:
                self.display.setText(current + ".")
        else:
            if current == "0" and text not in ["."]:
                self.display.setText(text)
            else:
                self.display.setText(current + text)

    # "=" 버튼 계산
    def equal(self):
        try:
            expression = self.display.text().replace("×", "*").replace("÷", "/")
            if "%" in expression:
                expression = expression.replace("%", "/100")
            result = eval(expression)
            self.display.setText(str(result))
        except Exception:
            self.display.setText("Error")

    # 사칙 연산
    def add(self):
        self._append_operator("+")

    def subtract(self):
        self._append_operator("-")

    def multiply(self):
        self._append_operator("×")

    def divide(self):
        self._append_operator("÷")

    def _append_operator(self, op):
        current = self.display.text()
        if current[-1] not in "+-×÷":
            self.display.setText(current + op)

    # 초기화
    def reset(self):
        self.display.setText("0")

    # ± 전환
    def toggle_sign(self):
        current = self.display.text()
        if current.startswith("-"):
            self.display.setText(current[1:])
        else:
            if current != "0":
                self.display.setText("-" + current)

    # 백분율
    def percent(self):
        try:
            current = self.display.text()
            value = float(current)
            self.display.setText(str(value / 100))
        except Exception:
            self.display.setText("Error")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalculatorUI()
    window.show()
    sys.exit(app.exec())
