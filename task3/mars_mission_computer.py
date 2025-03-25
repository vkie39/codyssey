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
        return self.env_values

#인스턴스 생성
ds = DummySensor()
ds.set_env()
print('----------출력----------')
print('env_value 출력: ', ds.env_values) #클래스 인스턴스의 딕셔너리 참조
print('\nset_env 값: ', ds.set_env()) #리턴값 지정 안 해서 None 출력    
print('\ngt_env 값: ', ds.get_env()) #랜덤으로 생성된 값 출력

