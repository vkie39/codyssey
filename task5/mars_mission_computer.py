import random
import time
import os
import platform

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
                
                # 센서 데이터 + 시스템 정보 합치기
                # 수동으로 JSON 문자열 구성
                json_output = '{\n'
                
                # 센서 데이터
                json_output += '  "sensor_data": {\n'
                for i, (k, v) in enumerate(current_env.items()):
                    comma = ',' if i < len(current_env) - 1 else ''
                    json_output += f'    "{k}": {repr(v)}{comma}\n'
                json_output += '  },\n'
    
                # 시스템 정보
                json_output += '  "system_info": {\n'
                for i, (k, v) in enumerate(system_info.items()):
                    comma = ',' if i < len(system_info) - 1 else ''
                    json_output += f'    "{k}": {repr(v)}{comma}\n'
                json_output += '  }\n'
    
                json_output += '}'
    
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
              
    # 시스템 정보 가져옴
    def get_mission_computer_info(self):
        system_info = {
            'os': platform.system(), 
            'os version': platform.version(), 
            'cpu type': platform.processor(), 
            'cpu cores': os.cpu_count(), 
            'Memory (in GB)': round(os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') / (1024. ** 3), 2)
        }
        return system_info
                                           

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

이 에서 
미션 컴퓨터의 부하를 가져오는 코드를 get_mission_computer_load() 메소드로 만들고 MissionComputer 클래스에 추가한다
get_mission_computer_load() 메소드의 경우 다음과 같은 정보들을 가져 올 수 있게한다. 
CPU 실시간 사용량
메모리 실시간 사용량 
get_mission_computer_load()에 해당 결과를 JSON 형식으로 출력하는 코드를 추가한다. 
이 부분은 챗gpt의 센서 데이터 JSON출력에 적혀있음. 확인 요망
