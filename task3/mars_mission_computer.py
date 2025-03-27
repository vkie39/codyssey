import random

class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature' : None,
            'mars_base_external_temperature' : None,
            'mars_base_internal_humidity' : None,
            'mars_base_external_illuminance' : None,
            'mars_base_internal_co2' : None,
            'mars_base_internal_oxygen' : None
        }
    
    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = random.randint(18, 30)
        self.env_values['mars_base_external_temperature'] = random.randint(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.randint(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.randint(500, 715)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 4)
        self.env_values['mars_base_internal_oxygen'] = random.randint(4, 7)
    
    def get_env(self, timestamp):
        with open('task3/env_log.txt', 'a') as log_file:
            log_file.write(f"[{timestamp}] {self.env_values}\n")
        return self.env_values

def get_user_timestamp():
    print("날짜와 시간을 입력하세요.")
    year = input("연도 (예: 2025): ")
    month = input("월 (예: 03): ")
    day = input("일 (예: 27): ")
    hour = input("시 (예: 16): ")
    minute = input("분 (예: 20): ")
    return f"{year}-{month}-{day} {hour}:{minute}"

# 실행
ds = DummySensor()
ds.set_env()
timestamp = get_user_timestamp()

print('----------출력----------')
print('env_value 출력: ', ds.env_values)
print('\nget_env 값: ', ds.get_env(timestamp))
