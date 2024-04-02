# from flask import Flask, jsonify, request
# import requests
# import math
# from datetime import datetime, timedelta
# import random

# app = Flask(__name__)

# base_url = "https://api.data.gov.sg/v1"
# endpoint_air_temperature = "/environment/air-temperature"
# endpoint_relative_humidity = "/environment/relative-humidity"

# class HeatStressDetector:
#     def __init__(self):
#         self.station_mapping = {
#             "S24": "Upper Changi Road North",
#             "S43": "Kim Chuan Road",
#             "S44": "Nanyang Avenue",
#             "S50": "Clementi Road",
#             "S60": "Sentosa",
#             "S100": "Woodlands Road",
#             "S104": "Woodlands Avenue 9",
#             "S106": "Pulau Ubin",
#             "S107": "East Coast Parkway",
#             "S108": "Marina Gardens Drive",
#             "S109": "Ang Mo Kio Avenue 5",
#             "S111": "Scotts Road",
#             "S115": "Tuas South Avenue 3",
#             "S116": "West Coast Highway",
#             "S117": "Banyan Road",
#             "S121": "Old Choa Chu Kang Road",
#             "S122": "Sembawang Road"
#         }
#         self.stations_by_region = {
#             "North": ["S100", "S104", "S106", "S109", "S122"],
#             "South": ["S60", "S116"],
#             "East": ["S24", "S43", "S106", "S107"],
#             "West": ["S44", "S50", "S117", "S115", "S116", "S121"],
#             "Central": ["S108", "S111"]
#         }

#     def calculate_wbgt(self, value_air_temperature, value_relative_humidity):
#         e = value_relative_humidity / 100 * 6.105 * math.exp(
#             17.27 * value_air_temperature / (237.7 + value_air_temperature))
#         WBGT = 0.567 * value_air_temperature + 0.393 * e + 3.94
#         return WBGT

#     def get_relative_humidity_for_station(self, data_relative_humidity, station_id):
#         for item in data_relative_humidity.get("items", []):
#             for reading in item.get("readings", []):
#                 if reading.get("station_id") == station_id:
#                     return reading.get("value")
#         return None


#     # random message generator
#     def get_random_heat_stress_tip(self):
#         heat_stress_tips = [
#             "Stay Hydrated: Drink plenty of water to stay hydrated.",
#             "Wear Appropriate Clothing: Wear loose, lightweight, and light-colored clothing to help your body stay cool.",
#             "Limit Outdoor Activities: Try to limit outdoor activities during the hottest parts of the day.",
#             "Use Sun Protection: Use sunscreen with to protect your skin from sunburn, and wear sunglasses to protect your eyes and face from the sun.",
#             "Seek Shade: Stay in the shade as much as possible when outdoors.",
#             "Use Cooling Measures: Use fans or air conditioning to cool down indoor spaces. You can also take cool showers or baths to lower your body temperature.",
#             "Monitor Your Health: Pay attention to signs of heat-related illnesses, such as dizziness, nausea, headache, rapid heartbeat, and confusion. If you experience any of these symptoms, see a doctor immediately.",
#             "Check on Vulnerable Individuals: Check on elderly family members, friends, or neighbors, as they are more susceptible to heat-related illnesses.",
#             "Never Leave Children or Pets in Cars: Temperatures inside a car can quickly reach dangerous levels, even with the windows cracked open."
#             ]
#         return random.choice(heat_stress_tips)




# @app.route('/compare-past-week', methods=['GET'])
# def compare_past_week():
#     try:
#         heat_stress_detector = HeatStressDetector()
#         today = datetime.today()
#         past_week_start = today - timedelta(days=today.weekday() + 7)
#         current_week_start = today - timedelta(days=today.weekday())

#         url_air_temperature_past_week = f"{base_url}{endpoint_air_temperature}?date={past_week_start.strftime('%Y-%m-%d')}"
#         url_relative_humidity_past_week = f"{base_url}{endpoint_relative_humidity}?date={past_week_start.strftime('%Y-%m-%d')}"

#         url_air_temperature_current_week = f"{base_url}{endpoint_air_temperature}?date={current_week_start.strftime('%Y-%m-%d')}"
#         url_relative_humidity_current_week = f"{base_url}{endpoint_relative_humidity}?date={current_week_start.strftime('%Y-%m-%d')}"

#         response_air_temperature_past_week = requests.get(url_air_temperature_past_week)
#         response_relative_humidity_past_week = requests.get(url_relative_humidity_past_week)

#         response_air_temperature_current_week = requests.get(url_air_temperature_current_week)
#         response_relative_humidity_current_week = requests.get(url_relative_humidity_current_week)

#         data_air_temperature_past_week = response_air_temperature_past_week.json()
#         data_relative_humidity_past_week = response_relative_humidity_past_week.json()
#         data_air_temperature_current_week = response_air_temperature_current_week.json()
#         data_relative_humidity_current_week = response_relative_humidity_current_week.json()

#         total_wbgt_past_week = 0
#         station_count_past_week = 0
#         for item in data_air_temperature_past_week.get("items", []):
#             for reading in item.get("readings", []):
#                 station_id = reading.get("station_id")
#                 if station_id in heat_stress_detector.stations_by_region.get("North", []):
#                     air_temperature = reading.get("value")
#                     relative_humidity = heat_stress_detector.get_relative_humidity_for_station(data_relative_humidity_past_week, station_id)
#                     if relative_humidity is not None:
#                         wbgt = heat_stress_detector.calculate_wbgt(air_temperature, relative_humidity)
#                         total_wbgt_past_week += wbgt
#                         station_count_past_week += 1
#         average_wbgt_past_week = total_wbgt_past_week / station_count_past_week if station_count_past_week > 0 else 0

#         total_wbgt_current_week = 0
#         station_count_current_week = 0
#         for item in data_air_temperature_current_week.get("items", []):
#             for reading in item.get("readings", []):
#                 station_id = reading.get("station_id")
#                 if station_id in heat_stress_detector.stations_by_region.get("North", []):
#                     air_temperature = reading.get("value")
#                     relative_humidity = heat_stress_detector.get_relative_humidity_for_station(data_relative_humidity_current_week, station_id)
#                     if relative_humidity is not None:
#                         wbgt = heat_stress_detector.calculate_wbgt(air_temperature, relative_humidity)
#                         total_wbgt_current_week += wbgt
#                         station_count_current_week += 1
#         average_wbgt_current_week = total_wbgt_current_week / station_count_current_week if station_count_current_week > 0 else 0

#         if average_wbgt_current_week > average_wbgt_past_week:
#             difference_percentage = ((average_wbgt_current_week - average_wbgt_past_week) / average_wbgt_past_week) * 100
#             message = f"Temperature this week is {difference_percentage:.2f}% higher than the past week."
#             # ===
#             random_tip = heat_stress_detector.get_random_heat_stress_tip()
#             random_tip_response = random_tip
#         else:
#             message = "Temperature this week is not higher than the past week."


#         response = {
#             "average_wbgt_past_week": average_wbgt_past_week,
#             "average_wbgt_current_week": average_wbgt_current_week,
#             "message": message,
#             "random_tip": random_tip_response
#         }

#         return jsonify(response), 200

#     except requests.RequestException as e:
#         return jsonify({"error": "Error fetching data from API"}), 500

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, jsonify, render_template
import requests
import threading
import math
from datetime import datetime, timedelta
import random


app = Flask(__name__)

base_url = "https://api.data.gov.sg/v1"
endpoint_air_temperature = "/environment/air-temperature"
endpoint_relative_humidity = "/environment/relative-humidity"

class HeatStressDetector:
    def __init__(self):
        self.station_mapping = {
            "S24": "Upper Changi Road North",
            "S43": "Kim Chuan Road",
            "S44": "Nanyang Avenue",
            "S50": "Clementi Road",
            "S60": "Sentosa",
            "S100": "Woodlands Road",
            "S104": "Woodlands Avenue 9",
            "S106": "Pulau Ubin",
            "S107": "East Coast Parkway",
            "S108": "Marina Gardens Drive",
            "S109": "Ang Mo Kio Avenue 5",
            "S111": "Scotts Road",
            "S115": "Tuas South Avenue 3",
            "S116": "West Coast Highway",
            "S117": "Banyan Road",
            "S121": "Old Choa Chu Kang Road",
            "S122": "Sembawang Road"
        }
        self.stations_by_region = {
            "North": ["S100", "S104", "S106", "S109", "S122"],
            "South": ["S60", "S116"],
            "East": ["S24", "S43", "S106", "S107"],
            "West": ["S44", "S50", "S117", "S115", "S116", "S121"],
            "Central": ["S108", "S111"]
        }

    def calculate_wbgt(self, value_air_temperature, value_relative_humidity):
        e = value_relative_humidity / 100 * 6.105 * math.exp(
            17.27 * value_air_temperature / (237.7 + value_air_temperature))
        WBGT = 0.567 * value_air_temperature + 0.393 * e + 3.94
        return WBGT

    def get_relative_humidity_for_station(self, data_relative_humidity, station_id):
        for item in data_relative_humidity.get("items", []):
            for reading in item.get("readings", []):
                if reading.get("station_id") == station_id:
                    return reading.get("value")
        return None

    def get_random_heat_stress_tip(self):
        heat_stress_tips = [
            "Stay Hydrated: Drink plenty of water to stay hydrated.",
            "Wear Appropriate Clothing: Wear loose, lightweight, and light-colored clothing to help your body stay cool.",
            "Limit Outdoor Activities: Try to limit outdoor activities during the hottest parts of the day.",
            "Use Sun Protection: Use sunscreen with to protect your skin from sunburn, and wear sunglasses to protect your eyes and face from the sun.",
            "Seek Shade: Stay in the shade as much as possible when outdoors.",
            "Use Cooling Measures: Use fans or air conditioning to cool down indoor spaces. You can also take cool showers or baths to lower your body temperature.",
            "Monitor Your Health: Pay attention to signs of heat-related illnesses, such as dizziness, nausea, headache, rapid heartbeat, and confusion. If you experience any of these symptoms, see a doctor immediately.",
            "Check on Vulnerable Individuals: Check on elderly family members, friends, or neighbors, as they are more susceptible to heat-related illnesses.",
            "Never Leave Children or Pets in Cars: Temperatures inside a car can quickly reach dangerous levels, even with the windows cracked open."
        ]
        return random.choice(heat_stress_tips)


# initial page loading
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare-past-week', methods=['GET'])
def compare_past_week():
    try:
        heat_stress_detector = HeatStressDetector()
        today = datetime.today()
        past_week_start = today - timedelta(days=today.weekday() + 7)
        current_week_start = today - timedelta(days=today.weekday())

        urls = [
            f"{base_url}{endpoint_air_temperature}?date={past_week_start.strftime('%Y-%m-%d')}",
            f"{base_url}{endpoint_relative_humidity}?date={past_week_start.strftime('%Y-%m-%d')}",
            f"{base_url}{endpoint_air_temperature}?date={current_week_start.strftime('%Y-%m-%d')}",
            f"{base_url}{endpoint_relative_humidity}?date={current_week_start.strftime('%Y-%m-%d')}"
        ]

        threads = []
        data = []
        for url in urls:
            thread = threading.Thread(target=lambda u=url: data.append(requests.get(u).json()))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        past_temp_data, past_humidity_data, current_temp_data, current_humidity_data = data

        total_wbgt_past_week = 0
        station_count_past_week = 0
        for item in past_temp_data.get("items", []):
            for reading in item.get("readings", []):
                station_id = reading.get("station_id")
                if station_id in heat_stress_detector.stations_by_region.get("North", []):
                    air_temperature = reading.get("value")
                    relative_humidity = heat_stress_detector.get_relative_humidity_for_station(past_humidity_data, station_id)
                    if relative_humidity is not None:
                        wbgt = heat_stress_detector.calculate_wbgt(air_temperature, relative_humidity)
                        total_wbgt_past_week += wbgt
                        station_count_past_week += 1
        average_wbgt_past_week = total_wbgt_past_week / station_count_past_week if station_count_past_week > 0 else 0

        total_wbgt_current_week = 0
        station_count_current_week = 0
        for item in current_temp_data.get("items", []):
            for reading in item.get("readings", []):
                station_id = reading.get("station_id")
                if station_id in heat_stress_detector.stations_by_region.get("North", []):
                    air_temperature = reading.get("value")
                    relative_humidity = heat_stress_detector.get_relative_humidity_for_station(current_humidity_data, station_id)
                    if relative_humidity is not None:
                        wbgt = heat_stress_detector.calculate_wbgt(air_temperature, relative_humidity)
                        total_wbgt_current_week += wbgt
                        station_count_current_week += 1
        average_wbgt_current_week = total_wbgt_current_week / station_count_current_week if station_count_current_week > 0 else 0

        if average_wbgt_current_week > average_wbgt_past_week:
            difference_percentage = ((average_wbgt_current_week - average_wbgt_past_week) / average_wbgt_past_week) * 100
            message = f"Temperature this week is {difference_percentage:.2f}% higher than the past week."
            random_tip_response = heat_stress_detector.get_random_heat_stress_tip()
        else:
            message = "Temperature this week is not higher than the past week."
            random_tip_response = heat_stress_detector.get_random_heat_stress_tip()

        response = {
            "average_wbgt_past_week": average_wbgt_past_week,
            "average_wbgt_current_week": average_wbgt_current_week,
            "message": message,
            "random_tip": random_tip_response
        }

        return jsonify(response), 200

    except requests.RequestException as e:
        return jsonify({"error": "Error fetching data from API"}), 500

if __name__ == '__main__':
    app.run(debug=True)

