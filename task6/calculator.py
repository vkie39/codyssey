# PyQt6의 핵심 위젯 및 레이아웃 클래스들 가져오기
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QLineEdit
from PyQt6.QtCore import Qt  # 정렬 등 다양한 Qt 상수들 포함
from PyQt6.QtGui import QFont  # 폰트 설정에 사용

# 계산기 UI를 정의하는 클래스
class CalculatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("iPhone 스타일 계산기")  # 창 제목 설정
        self.setFixedSize(320, 480)  # 고정 창 크기
        self.init_ui()  # UI 초기화 메서드 호출

    def init_ui(self):
        self.setStyleSheet("background-color: black;")  # 배경색 검정으로 설정

        # 디스플레이 부분 설정 (숫자/기호가 표시되는 부분)
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)  # 오른쪽 정렬
        self.display.setReadOnly(True)  # 사용자가 직접 입력 못하게 설정
        self.display.setText("0")  # 기본값 0으로 설정
        self.display.setStyleSheet("""
            background-color: black;
            color: white;
            border: none;
        """)  # 스타일 설정 (배경, 글자색 등)
        self.display.setFont(QFont("Arial", 30))  # 폰트 크기 및 스타일 설정
        self.display.setFixedHeight(80)  # 디스플레이 높이 고정

        # 계산기 버튼 배열 정의
        buttons = [
            ["AC", "±", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "="]
        ]

        grid = QGridLayout()  # 버튼 그리드 레이아웃

        # 버튼 생성 및 배치
        for row, texts in enumerate(buttons):
            for col, text in enumerate(texts):
                button = QPushButton(text)
                button.setFont(QFont("Arial", 20))
                button.setFixedSize(70, 70)

                # 버튼 색상 및 스타일 지정
                if text in ["AC", "±", "%"]:
                    button.setStyleSheet("background-color: gray; color: black; border-radius: 35px;")
                elif text in ["÷", "×", "-", "+", "="]:
                    button.setStyleSheet("background-color: orange; color: white; border-radius: 35px;")
                else:
                    button.setStyleSheet("background-color: #222222; color: white; border-radius: 35px;")

                # 버튼 클릭 시 이벤트 연결
                button.clicked.connect(self.on_button_click)

                # 0, ., = 버튼은 마지막 줄에서 특별한 위치에 배치
                if row == 4:
                    if text == "0":
                        button.setFixedSize(150, 70)  # 0은 두 칸 차지
                        grid.addWidget(button, 5, 0, 1, 2)
                    elif text == ".":
                        grid.addWidget(button, 5, 2)
                    elif text == "=":
                        grid.addWidget(button, 5, 3)
                else:
                    grid.addWidget(button, row + 1, col)  # 일반 버튼은 그대로 배치

        # 전체 레이아웃 설정
        layout = QVBoxLayout()
        layout.addWidget(self.display)  # 디스플레이 위쪽에 배치
        layout.addLayout(grid)  # 버튼 그리드 아래쪽에 배치
        layout.setSpacing(10)  # 간격 설정
        self.setLayout(layout)

    # 버튼 클릭 시 실행되는 함수
    def on_button_click(self):
        sender = self.sender()
        text = sender.text()  # 클릭된 버튼의 텍스트 가져오기
        current = self.display.text()  # 현재 디스플레이에 표시된 텍스트

        print(f"버튼 눌림: {text}")  # 디버깅용 콘솔 출력

        if text == "AC":
            self.display.setText("0")  # AC는 초기화
        elif text == "=":
            try:
                # 연산 기호 변환: ×, ÷ → *, /
                expression = current.replace("×", "*").replace("÷", "/")
                # % 기호 처리: 퍼센트를 나누기로 변환
                if "%" in expression:
                    expression = expression.replace("%", "/100")
                result = eval(expression)  # 파이썬 eval로 계산 실행
                self.display.setText(str(result))  # 결과 표시
            except Exception:
                self.display.setText("Error")  # 에러 발생 시 표시
        elif text == "±":
            # ± 기호 처리: 음수 전환
            if current.startswith("-"):
                self.display.setText(current[1:])  # 음수 제거
            else:
                if current != "0":
                    self.display.setText("-" + current)  # 음수 추가
        else:
            # 숫자 또는 연산자 입력 처리
            if current == "0" and text not in [".", "+", "-", "×", "÷"]:
                self.display.setText(text)  # 0에서 다른 숫자로 대체
            else:
                self.display.setText(current + text)  # 기존 텍스트에 추가

# 프로그램 실행 진입점
if __name__ == "__main__":
    app = QApplication([])  # sys 없이 QApplication 생성 (빈 리스트 사용)
    window = CalculatorUI()  # 계산기 UI 인스턴스 생성
    window.show()  # 창 표시
    app.exec()  # 앱 실행 루프 진입
