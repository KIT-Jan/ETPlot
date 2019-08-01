"""Get the data from database"""

import requests
import numpy as np
import sys
import yaml


class DataOperator():

    def __init__(self):
        with open("cfg/measurements.yml", 'r') as stream:
            try:
                self.measurement_definitions = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        print("DataOperator initialised - measurements.yml read")

    def get_data(self, probe_id, measurement_type, save_data, **kwargs):
        """ Request the data and save it (or not) """

        if measurement_type == "CV":
            return self.handle_CV_measurement(probe_id, save_data)
        if measurement_type == "R_int_ramp":
            print("R_int_ramp to be implemented!")
            return False

        x_para = self.measurement_definitions[measurement_type]["x"]
        y_para = self.measurement_definitions[measurement_type]["y"]

        request = requests.get(f"http://192.168.13.33:8000/"
                               f"measurement/{probe_id}/json")
        answer = request.json()
        sensor_name = answer["header"]["sensorname"]
        data = answer["data"]
        data_dict = {x_para: [], y_para: []}

        if save_data:
            with open(f"data/{sensor_name}_{probe_id}_"
                      f"{measurement_type}.txt",
                      "w") as file:

                for entry in data:
                    x_value = entry[x_para]["value"]
                    y_value = entry[y_para]["value"]
                    data_dict[x_para].append(x_value)
                    data_dict[y_para].append(y_value)
                    file.write(f"{x_value}\t{y_value}\n")

        if not save_data:
            for entry in data:
                data_dict[x_para].append(entry[x_para]["value"])
                data_dict[y_para].append(entry[y_para]["value"])

        return data_dict

    def handle_CV_measurement(self, probe_id, save_data):
        """ Standard CV measurements are calculated by 1/C**2"""

        request = requests.get(f"http://192.168.13.33:8000/"
                               f"measurement/{probe_id}/json")
        answer = request.json()
        sensor_name = answer["header"]["sensorname"]
        data = answer["data"]
        data_dict = {"voltage": [], "1/C**2": []}

        if save_data:
            with open(f"data/{sensor_name}_{probe_id}_CV.txt",
                      "w") as file:

                for entry in data:
                    x_value = entry["voltage"]["value"]
                    y_value = 1/float(entry["capacitance"]["value"])**2
                    data_dict["voltage"].append(x_value)
                    data_dict["1/C**2"].append(y_value)
                    file.write(f"{x_value}\t{y_value}\n")

        if not save_data:
            for entry in data:
                x_value = entry["voltage"]["value"]
                data_dict["voltage"].append(x_value)
                y_value = 1/float(entry["capacitance"]["value"])**2
                data_dict["1/C**2"].append(y_value)

        return data_dict


def main():
    probe_id = sys.argv[1]
    measurement_type = sys.argv[2]
    db = DataOperator()
    data = db.get_data(probe_id=probe_id,
                       measurement_type=measurement_type,
                       save_data=True)


if __name__ == "__main__":
    main()
