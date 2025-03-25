import mars_mission_computer

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

ds = mars_mission_computer.DummySensor()
ds.set_env()