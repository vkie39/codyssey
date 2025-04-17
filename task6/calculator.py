import sys
# PyQt6에서 필요한 모듈들을 가져옴
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QLineEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# 계산기 UI 클래스 정의 (QWidget 상속)
class CalculatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("iPhone 스타일 계산기")  # 창 제목 설정
        self.setFixedSize(320, 480)                # 창 크기 고정
        self.init_ui()                             # UI 초기화 함수 호출

    def init_ui(self):
        self.setStyleSheet("background-color: black;")  # 전체 배경을 검정색으로 설정

        # 디스플레이: 입력값/결과를 보여주는 텍스트 창
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)  # 오른쪽 정렬
        self.display.setReadOnly(True)                          # 사용자가 직접 입력하지 못하게 설정
        self.display.setText("0")                               # 초기 표시 값
        self.display.setStyleSheet("""                          # 디스플레이 스타일 (배경/글자색 등)
            background-color: black;
            color: white;
            border: none;
        """)
        self.display.setFont(QFont("Arial", 30))                # 글자 크기 설정
        self.display.setFixedHeight(80)                         # 높이 고정

        # 계산기 버튼 목록 (5줄, iPhone 계산기와 유사하게 배치)
        buttons = [
            ["AC", "±", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "="]
        ]

        # 버튼을 그리드(표) 형태로 배치하기 위한 레이아웃
        grid = QGridLayout()
        for row, texts in enumerate(buttons):  # 각 줄에 대해 반복
            for col, text in enumerate(texts):  # 각 버튼에 대해 반복
                button = QPushButton(text)             # 버튼 생성
                button.setFont(QFont("Arial", 20))     # 글꼴 크기 설정
                button.setFixedSize(70, 70)            # 기본 버튼 크기

                # 버튼 색상과 스타일 설정
                if text in ["AC", "±", "%"]:
                    button.setStyleSheet("background-color: gray; color: black; border-radius: 35px;")
                elif text in ["÷", "×", "-", "+", "="]:
                    button.setStyleSheet("background-color: orange; color: white; border-radius: 35px;")
                else:
                    button.setStyleSheet("background-color: #222222; color: white; border-radius: 35px;")

                # 클릭 시 연결할 함수 설정
                button.clicked.connect(self.on_button_click)

                # 마지막 줄 (0, ., =) 버튼 위치 조정
                if row == 4:
                    if text == "0":
                        button.setFixedSize(150, 70)           # 0 버튼은 가로로 2칸 차지
                        grid.addWidget(button, 5, 0, 1, 2)     # (행, 열, 행크기, 열크기)
                    elif text == ".":
                        grid.addWidget(button, 5, 2)
                    elif text == "=":
                        grid.addWidget(button, 5, 3)
                else:
                    grid.addWidget(button, row + 1, col)       # 나머지 버튼은 기본 위치에 배치

        # 전체 레이아웃 구성 (상단 디스플레이 + 버튼 영역)
        layout = QVBoxLayout()
        layout.addWidget(self.display)
        layout.addLayout(grid)
        layout.setSpacing(10)             # 위 아래 간격 설정
        self.setLayout(layout)

    # 버튼 클릭 시 실행되는 메서드
    def on_button_click(self):
        sender = self.sender()            # 어떤 버튼이 눌렸는지 확인
        text = sender.text()              # 버튼 위의 텍스트
        current = self.display.text()     # 현재 디스플레이에 있는 텍스트

        if text == "AC":
            self.display.setText("0")     # 모든 입력 초기화
        elif text == "=":
            try:
                # 표시된 수식을 파이썬에서 실행 가능한 수식으로 변환
                expression = current.replace("×", "*").replace("÷", "/")
                if "%" in expression:
                    expression = expression.replace("%", "/100")  # 100% → 1.0
                result = str(eval(expression))                    # eval()로 계산
                self.display.setText(result)                      # 결과 표시
            except Exception:
                self.display.setText("Error")                     # 오류 발생 시 "Error"
        elif text == "±":
            # 양수/음수 전환 처리
            if current.startswith("-"):
                self.display.setText(current[1:])                 # 음수를 양수로
            else:
                if current != "0":
                    self.display.setText("-" + current)           # 양수를 음수로
        else:
            # 현재가 0이면 새로 덮어쓰기, 아니면 이어붙이기
            if current == "0" and text not in [".", "+", "-", "×", "÷"]:
                self.display.setText(text)
            else:
                self.display.setText(current + text)

# 프로그램 실행 시작 지점
if __name__ == "__main__":
    app = QApplication(sys.argv)   # PyQt 애플리케이션 생성
    window = CalculatorUI()        # 계산기 UI 인스턴스 생성
    window.show()                  # 창 띄우기
    sys.exit(app.exec())           # 애플리케이션 실행 및 종료 시 정리
