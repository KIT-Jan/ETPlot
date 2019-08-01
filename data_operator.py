"""Get the data from database"""

import requests
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

        if measurement_type == "R_int_ramp":
            print("R_int_ramp to be implemented!")
            return False

        parameters = self.measurement_definitions[measurement_type]
        if "1/C**2" in parameters:
            parameters.remove("1/C**2")
            parameters.append("capacitance")

        request = requests.get(f"http://192.168.13.33:8000/"
                               f"measurement/{probe_id}/json")
        answer = request.json()
        sensor_name = answer["header"]["sensorname"]
        data = answer["data"]

        # data_dict = {"first_parameter": [], "second_parameter: [], ... "}
        data_dict = {parameters[i]: [] for i in range(len(parameters))}

        try:
            for entry in data:
                for parameter in parameters:
                    data_dict[parameter].append(entry[parameter]["value"])
        except:
            print("Measurement parameters:", *parameters)
            print("Measurement parameters and keys in database are different!")
            raise

        if measurement_type == "CV":
            capacitance_data = data_dict["capacitance"]
            converted_data = []
            for item in capacitance_data:
                converted_data.append(float(1/item**2))
            data_dict["1/C**2"] = converted_data
            del data_dict["capacitance"]

        if save_data:
            with open(f"data/{sensor_name}_{probe_id}_"
                      f"{measurement_type}.txt",
                      "w") as file:

                value_list = []
                for key in data_dict.keys():
                    value_list.append(data_dict[key])

                for i in range(len(value_list[0])):
                    string = ""
                    for item in range(len(parameters)):
                        if item == 0:
                            string += str(value_list[item][i])
                        else:
                            string += "\t" + str(value_list[item][i])
                    string[-2:]
                    string += "\n"
                    file.write(string)

        data_dict["sensorname"] = sensor_name
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
