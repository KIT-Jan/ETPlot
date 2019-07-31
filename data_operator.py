"""Get the data from database"""

import requests
import numpy as np
import sys


class DataOperator():

    def __init__(self):
        print("initialised")

    def get_data(self, probe_id, data_conversion, save_data, **kwargs):
        """ Request the data and save it (or not) """

        request = requests.get(f"http://192.168.13.33:8000/"
                               f"measurement/{probe_id}/json")
        answer = request.json()
        header = answer["header"]
        data = answer["data"]
        data_dict = {"x_values": [], "y_values": []}

        if save_data:
            with open(f"data/{probe_id}_{data_conversion}.txt", "w") as file:
                for entry in data:
                    bias_voltage = entry["voltage"]["value"]
                    current = entry["current"]["value"]
                    data_dict["x_values"].append(bias_voltage)
                    data_dict["y_values"].append(current)
                    file.write(f"{bias_voltage}\t{current}\n")

        if not save_data:
            for entry in data:
                data_dict["x_values"].append(entry["voltage"]["value"])
                data_dict["y_values"].append(entry["current"]["value"])

        return data_dict
