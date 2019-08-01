""" Test the data_operator module"""

from data_operator import DataOperator
import matplotlib.pyplot as plt

db = DataOperator()
data = db.get_data(probe_id=10515, measurement_type="IV", save_data=True)
print(data)
plt.plot(data["voltage"], data["current"])
plt.show()
