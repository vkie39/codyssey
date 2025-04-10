import random
import time
import os #운영체제 정보
import platform #시스템 정보
from threading import Thread #병렬 반복문

SETTING_FILE = "setting.txt" #보너스 문제

#출력을 원하는 항목들.
DEFAULT_SETTINGS = {
    "mars_base_internal_temperature": True,
    "mars_base_external_temperature": True,
    "mars_base_internal_humidity": True,
    "mars_base_external_illuminance": True,
    "mars_base_internal_co2": True,
    "mars_base_internal_oxygen": True,
    "system_info": True,
    "system_load": True
}

#설정파일 불러오기
def load_settings():
    settings = DEFAULT_SETTINGS.copy()
    #파일 없으면 생성
    if not os.path.exists(SETTING_FILE):
        with open(SETTING_FILE, 'w') as f:
            for k, v in settings.items():
                f.write(f"{k}={str(v).lower()}\n")
        print("setting.txt 파일 생성됨")
        return settings
    #파일 있으면 쓰기
    with open(SETTING_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip() #공백 제거
                value = value.strip().lower() #소문자로 변경(true, false)
                if key in settings:
                    settings[key] = value == 'true'
    return settings

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

class MissionComputer:
    def __init__(self):
        self.settings = load_settings() #사용자 설정 불러와서  self.settings에 저장
        self.env_values = {key: [] for key in DEFAULT_SETTINGS if "mars_base" in key} #"mars_base"로 시작하는 항목들만 골라서 key: [] 형태의 딕셔너리 생성
        self.sensor = DummySensor()
        self.start_time = time.time()
        self.running = True

    def get_sensor_data(self):
        try:
            while self.running:
                current_env = self.sensor.get_env()
                print("{")
                print('  "sensor_data": {')
                env_keys = list(current_env.keys())
                for i, key in enumerate(env_keys):
                    if self.settings.get(key, True):
                        value = current_env[key]
                        self.env_values[key].append(value)
                        comma = "," if i < len(env_keys) - 1 else ""
                        print(f'    "{key}": {repr(value)}{comma}')
                print("  },")

                if self.settings.get("system_info", True) or self.settings.get("system_load", True):
                    try:
                        system_info = self.get_mission_computer_info()
                        load_info = self.get_mission_computer_load()
                    except Exception as e:
                        system_info = {"error": str(e)}
                        load_info = {"error": str(e)}

                    print('  "system_info": {')
                    if self.settings.get("system_info", True):
                        for k, v in system_info.items():
                            print(f'    "{k}": "{v}",')

                    if self.settings.get("system_load", True):
                        print('    "system_load": {')
                        load_keys = list(load_info.keys())
                        for i, (k, v) in enumerate(load_info.items()):
                            comma = "," if i < len(load_keys) - 1 else ""
                            print(f'      "{k}": {v}{comma}')
                        print("    }")
                    print("  }")

                print("}")

                if time.time() - self.start_time >= 300:
                    print("5분 평균:")
                    for key, values in self.env_values.items():
                        if self.settings.get(key, True) and values:
                            avg = sum(values) / len(values)
                            print(f"  {key}: {avg:.2f}")
                            self.env_values[key] = []
                    self.start_time = time.time()

                time.sleep(5)
        except KeyboardInterrupt:
            print("System stopped...")

    def check_stop_command(self):
        while self.running:
            command = input()
            if command.lower() == "stop":
                print("program is stopping...")
                self.running = False

    def get_mission_computer_info(self):
        memory_gb = os.environ.get('PROCESSOR_ARCHITECTURE', 'Unknown')
        return {
            'os': platform.system(),
            'os version': platform.version(),
            'cpu type': platform.processor(),
            'cpu cores': os.cpu_count(),
            'Memory (GB)': memory_gb
        }

    def get_mission_computer_load(self):
        cpu_usage = random.uniform(10, 90)
        memory_usage = random.uniform(30, 80)
        return {
            'cpu_usage_percent': round(cpu_usage, 2),
            'memory_usage_percent': round(memory_usage, 2)
        }

if __name__ == "__main__":
    runComputer = MissionComputer()

    try:
        if runComputer.settings.get("system_info", True):
            system_info = runComputer.get_mission_computer_info()
            print("Initial system information:")
            print(system_info)

        if runComputer.settings.get("system_load", True):
            load_info = runComputer.get_mission_computer_load()
            print("Initial system load:")
            print(load_info)
    except Exception as e:
        print("Error retrieving system information:", e)

    data_thread = Thread(target=runComputer.get_sensor_data)
    stop_thread = Thread(target=runComputer.check_stop_command)

    data_thread.start()
    stop_thread.start()

    data_thread.join()
    stop_thread.join()
