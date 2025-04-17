import sys
# PyQt6의 주요 모듈들을 가져옴
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QLineEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# 계산기 UI를 정의하는 클래스 (QWidget을 상속)
class CalculatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("iPhone 스타일 계산기")  # 창의 제목 설정
        self.setFixedSize(320, 480)                # 고정된 창 크기 설정
        self.init_ui()                             # UI 초기화 함수 호출

    def init_ui(self):
        self.setStyleSheet("background-color: black;")  # 전체 배경색 검정

        # 디스플레이: 숫자/기호 표시창
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)  # 텍스트 오른쪽 정렬
        self.display.setReadOnly(True)                          # 직접 입력 막기 (읽기 전용)
        self.display.setText("0")                               # 초기 텍스트는 0
        self.display.setStyleSheet("""                          # 배경색, 글자색 등 스타일 설정
            background-color: black;
            color: white;
            border: none;
        """)
        self.display.setFont(QFont("Arial", 30))                # 글자 크기 설정
        self.display.setFixedHeight(80)                         # 디스플레이 높이 고정

        # 계산기 버튼 구성 (5행 4열 구조)
        buttons = [
            ["AC", "±", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "="]
        ]

        # 버튼을 배치할 그리드 레이아웃 생성
        grid = QGridLayout()

        # 각 버튼을 생성하고 레이아웃에 추가
        for row, texts in enumerate(buttons):
            for col, text in enumerate(texts):
                button = QPushButton(text)              # 버튼 생성
                button.setFont(QFont("Arial", 20))      # 버튼 글꼴 설정
                button.setFixedSize(70, 70)             # 버튼 크기 고정

                # 버튼 색상 스타일 지정 (기능별로 다름)
                if text in ["AC", "±", "%"]:
                    button.setStyleSheet("background-color: gray; color: black; border-radius: 35px;")
                elif text in ["÷", "×", "-", "+", "="]:
                    button.setStyleSheet("background-color: orange; color: white; border-radius: 35px;")
                else:
                    button.setStyleSheet("background-color: #222222; color: white; border-radius: 35px;")

                # 버튼 클릭 시 이벤트 연결
                button.clicked.connect(self.on_button_click)

                # 마지막 줄(0, ., =) 버튼의 특별 배치
                if row == 4:
                    if text == "0":
                        button.setFixedSize(150, 70)           # 0 버튼은 두 칸 너비
                        grid.addWidget(button, 5, 0, 1, 2)     # 5행 0열부터 2칸 차지
                    elif text == ".":
                        grid.addWidget(button, 5, 2)
                    elif text == "=":
                        grid.addWidget(button, 5, 3)
                else:
                    grid.addWidget(button, row + 1, col)       # 나머지 버튼은 기본 위치

        # 전체 레이아웃 설정 (디스플레이 + 버튼 영역)
        layout = QVBoxLayout()
        layout.addWidget(self.display)
        layout.addLayout(grid)
        layout.setSpacing(10)
        self.setLayout(layout)

    # 버튼 클릭 시 처리되는 함수
    def on_button_click(self):
        sender = self.sender()          # 어떤 버튼이 눌렸는지 가져옴
        text = sender.text()            # 버튼의 텍스트
        current = self.display.text()   # 현재 디스플레이에 있는 텍스트

        if text == "=":
            pass  # 계산은 구현하지 않음
        elif text == "±":
            # 양수/음수 전환 기능
            if current.startswith("-"):
                self.display.setText(current[1:])
            else:
                if current != "0":
                    self.display.setText("-" + current)
        else:
            # 입력 숫자가 0일 경우 덮어쓰기
            if current == "0":
                self.display.setText(text)
            else:
                self.display.setText(current + text)  # 기존 텍스트에 덧붙임

# 프로그램의 진입점 (메인 루프 실행)
if __name__ == "__main__":
    app = QApplication(sys.argv)   # 애플리케이션 인스턴스 생성
    window = CalculatorUI()        # 계산기 UI 인스턴스 생성
    window.show()                  # 창 보이기
    sys.exit(app.exec())           # 이벤트 루프 시작 및 종료 처리
