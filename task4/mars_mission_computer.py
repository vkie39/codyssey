import random

#클래스 생성
class DummySensor:
    def __init__(self):
        #딕셔너리를 담고 있는 인스턴스 변수(사전 객체)
        self.env_values = {
            'mars_base_internal_temperature' : None,
            'mars_base_external_temperature' : None,
            'mars_base_internal_humidity' : None,
            'mars_base_external_illuminance' : None,
            'mars_base_internal_co2' : None,
            'mars_base_internal_oxygen' : None
        }
    
    #랜덤으로 값 생성하는 메서드 생성
    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = random.randint(18, 30)
        self.env_values['mars_base_external_temperature'] = random.randint(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.randint(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.randint(500, 715)
        self.env_values['mars_base_internal_co2'] = random.uniform(0.02, 0.1)
        self.env_values['mars_base_internal_oxygen'] = random.randint(4, 7)
    
    #값 반환하는 메서드 생성
    def get_env(self):
        #딕셔너리 값 로그 파일에 저장
        with open('task3\env_log.txt', 'a') as log_file:
            log_file.write(str(self.env_values) + '\n')
        return self.env_values

#인스턴스 생성
ds = DummySensor()
ds.set_env()

#//3주차

class MissionComputer:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature' : None,
            'mars_base_external_temperature' : None,
            'mars_base_internal_humidity' : None,
            'mars_base_external_illuminance' : None,
            'mars_base_internal_co2' : None,
            'mars_base_internal_oxygen' : None
        }
    def get_sensor_data():
        env_values = DummySensor()

ds = DummySensor()
