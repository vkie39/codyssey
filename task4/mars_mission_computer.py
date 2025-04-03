import random
import time

# DummySensor 클래스 정의
class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': None,
            'mars_base_external_temperature': None,
            'mars_base_internal_humidity': None,
            'mars_base_external_illuminance': None,
            'mars_base_internal_co2': None,
            'mars_base_internal_oxygen': None
        }
    
    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = random.randint(18, 30)
        self.env_values['mars_base_external_temperature'] = random.randint(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.randint(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.randint(500, 715)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 4)
        self.env_values['mars_base_internal_oxygen'] = random.randint(4, 7)
    
    def get_env(self):
        self.set_env()
        return self.env_values

# MissionComputer 클래스 정의
class MissionComputer:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': [],
            'mars_base_external_temperature': [],
            'mars_base_internal_humidity': [],
            'mars_base_external_illuminance': [],
            'mars_base_internal_co2': [],
            'mars_base_internal_oxygen': []
        }
        self.sensor = DummySensor()
        self.start_time = time.time()
        self.running = True
    
    def get_sensor_data(self):
        try:
            while self.running:
                # 센서 데이터 가져오기
                current_env = self.sensor.get_env()
                
                # 평균 계산용 데이터 추가
                for key in self.env_values.keys():
                    self.env_values[key].append(current_env[key])
                
                # JSON 출력
                json_output = "{\n"
                for idx, (key, value) in enumerate(current_env.items()):
                    json_output += f'    "{key}": {value}'
                    if idx < len(current_env) - 1:
                        json_output += ',\n'
                json_output += '\n}'
                print(json_output)
                
                # 5분 평균 출력
                if time.time() - self.start_time >= 300:  # 300초 == 5분
                    print("5분 평균:")
                    for key, values in self.env_values.items():
                        if values:
                            avg = sum(values) / len(values)
                            print(f"  {key}: {avg:.2f}")
                        # 데이터를 초기화하여 새로운 5분 간 평균 계산
                        self.env_values[key] = []
                    self.start_time = time.time()

                # 5초 대기
                time.sleep(5)
        except KeyboardInterrupt:
            print("System stopped...")

    def check_stop_command(self):
        # 터미널에서 입력을 받아서 stop을 입력하면 실행 중지
        while self.running:
            command = input()
            if command.lower() == "stop":
                print("program is stopping...")
                self.running = False

# MissionComputer 인스턴스화 및 데이터 수집 실행
RunComputer = MissionComputer()

# 두 작업을 동시에 처리하기 위해 병렬로 실행 (threading 없이 간단한 순차 흐름 사용)
from threading import Thread
data_thread = Thread(target=RunComputer.get_sensor_data)
stop_thread = Thread(target=RunComputer.check_stop_command)

data_thread.start()
stop_thread.start()

data_thread.join()
stop_thread.join()
