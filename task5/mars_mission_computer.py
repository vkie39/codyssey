import random
import time
import os
import platform
from threading import Thread

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
                current_env = self.sensor.get_env()

                for key in self.env_values.keys():
                    self.env_values[key].append(current_env[key])

                json_output = '{\n'
                json_output += '  "sensor_data": {\n'
                for i, (k, v) in enumerate(current_env.items()):
                    comma = ',' if i < len(current_env) - 1 else ''
                    json_output += f'    "{k}": {repr(v)}{comma}\n'
                json_output += '  },\n'

                try:
                    system_info = self.get_mission_computer_info()
                    load_info = self.get_mission_computer_load()
                except Exception as e:
                    system_info = {"error": str(e)}
                    load_info = {"error": str(e)}

                json_output += '  "system_info": {\n'
                for i, (k, v) in enumerate(system_info.items()):
                    json_output += f'    "{k}": {repr(v)},\n'

                json_output += '    "system_load": {\n'
                for i, (k, v) in enumerate(load_info.items()):
                    comma = ',' if i < len(load_info) - 1 else ''
                    json_output += f'      "{k}": {repr(v)}{comma}\n'
                json_output += '    }\n'
                json_output += '  }\n'

                json_output += '}'

                print(json_output)

                if time.time() - self.start_time >= 300:
                    print("5분 평균:")
                    for key, values in self.env_values.items():
                        if values:
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
        system_info = runComputer.get_mission_computer_info()
        load_info = runComputer.get_mission_computer_load()
        print("Initial system information:")
        print(system_info)
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