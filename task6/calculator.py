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

    def on_button_click(self):
        sender = self.sender()
        text = sender.text()
        current = self.display.text()

        print(f"버튼 눌림: {text}")  # 콘솔 확인용

        if text == "AC":
            self.display.setText("0")
        elif text == "=":
            try:
                # ×, ÷ 기호를 *, /로 바꿔서 파이썬 수식으로 변환
                expression = current.replace("×", "*").replace("÷", "/")

                # % 기호 처리: 100% → 1.0 으로
                if "%" in expression:
                    expression = expression.replace("%", "/100")

                result = eval(expression)  # 계산 실행
                self.display.setText(str(result))
            except Exception:
                self.display.setText("Error")  # 계산 오류 시 표시
        elif text == "±":
            if current.startswith("-"):
                self.display.setText(current[1:])
            else:
                if current != "0":
                    self.display.setText("-" + current)
        else:
            if current == "0" and text not in [".", "+", "-", "×", "÷"]:
                self.display.setText(text)
            else:
                self.display.setText(current + text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalculatorUI()
    window.show()
    sys.exit(app.exec())
