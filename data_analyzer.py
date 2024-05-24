from pymongo import MongoClient
from statistics import mean

class DataAnalyzer:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['factory']
        self.collection = self.db['state']

    def analyze(self):
        data = self.collection.find()
        average_temperatures = {}
        max_temperatures = {}
        min_temperatures = {}
        light_durations = {}
        alarm_count = 0
        fire_alarm_count = 0

        for entry in data:
            if 'room_name' in entry:
                room_name = entry['room_name']
                temperature = entry['temperature']
                light = entry['light']

                if room_name in average_temperatures:
                    average_temperatures[room_name].append(temperature)
                else:
                    average_temperatures[room_name] = [temperature]

                if room_name in max_temperatures:
                    max_temperatures[room_name] = max(max_temperatures[room_name], temperature)
                else:
                    max_temperatures[room_name] = temperature

                if room_name in min_temperatures:
                    min_temperatures[room_name] = min(min_temperatures[room_name], temperature)
                else:
                    min_temperatures[room_name] = temperature

                if light:
                    if room_name in light_durations:
                        light_durations[room_name] += 1
                    else:
                        light_durations[room_name] = 1

            if 'alarm_on' in entry:
                if entry['alarm_on']:
                    alarm_count += 1

            if 'fire_detected' in entry:
                if entry['fire_detected']:
                    fire_alarm_count += 1

        analysis_result = {
            'average_temperatures': {room: mean(temp) for room, temp in average_temperatures.items()},
            'max_temperatures': max_temperatures,
            'min_temperatures': min_temperatures,
            'light_durations': {room: duration * 60 for room, duration in light_durations.items()},
            'alarm_count': alarm_count,
            'fire_alarm_count': fire_alarm_count
        }

        return analysis_result