import random

class DummySensor:
    def __init__(self):
        self.env_values = {
            'marse_base_internal_tempreature' = random.uniform(18, 30),
            'marse_base_external_tempreature' = random.uniform(0, 21), 
            'maese_base_internal_humidity' = random.uniform(50, 60),
            'marse_base_external_illuminance' = random.uniform(500, 715),
            'marse_base_internal_co2' = random.uniform(0.02, 0.1), 
            'marse_base_internal_oxygen' = random.uniform(4, 7)          
            }
        
        

