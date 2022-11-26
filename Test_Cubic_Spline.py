import unittest
import numpy as np
import scipy
from scipy.io import wavfile
import matplotlib.pyplot as plt
from scipy.io import loadmat
from sklearn.metrics import mean_squared_error
from datetime import datetime
from time import sleep
from tqdm import tqdm
import scipy.signal
import unittest

# Import the ORGINAL wave file
samplerate_org, data_org = wavfile.read('original.wav')
length_org = data_org.shape[0] / samplerate_org
time_org = np.linspace(0., length_org, data_org.shape[0])
plt.subplot(3, 1, 1)
plt.plot(time_org, data_org)
plt.subplots_adjust(hspace=0.5)
plt.title("Original Signal")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")


# Import the DEGRADED wave file
samplerate_deg, data_deg = wavfile.read('degraded.wav')
length_deg = data_deg.shape[0] / samplerate_deg
time_deg = np.linspace(0., length_deg, data_deg.shape[0])
plt.subplot(3, 1, 2)
plt.plot(time_deg, data_deg)
plt.subplots_adjust(hspace=0.5)
plt.title("Degraded Signal")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")

# Load .mat file
degraded_files = loadmat('degraded_points.mat')

# Extract the keys of the dictionary
print(degraded_files.keys())

# Extract the array from the dictionary using the key
x = degraded_files["degraded_point"]

# Extract the click location
clicks = np.where(x == 1)

# Extract array from tuple
click_index = clicks[0]

# Number of clicks
num_clicks = len(click_index)


def CubicSplineInterpolator(data_deg, click_index):
    new_data = data_deg
    # print(len(new_data))
    index_all = np.arange(len(data_deg))
    # print(len(index_all))
    filtered_data = np.delete(new_data, click_index)
    # print(len(filtered_data))
    filtered_index = np.delete(index_all, click_index)
    # print(len(filtered_data))
    from scipy.interpolate import CubicSpline
    s = CubicSpline(filtered_index, filtered_data, bc_type='natural')
    for i in range(len(click_index)):
        new_data[click_index[i]] = s(click_index)[i]
    return new_data


start_time = datetime.now()
for i in tqdm(range(100)):
    restored_data = CubicSplineInterpolator(data_deg, click_index)
    sleep(0.3)
end_time = datetime.now()
print('Duration: {} seconds'.format(end_time - start_time))
wavfile.write("restored_cubic.wav", samplerate_org, restored_data)
length = restored_data.shape[0] / samplerate_org
time_restored = np.linspace(0., length, restored_data.shape[0])
plt.subplot(3, 1, 3)
plt.plot(time_restored, restored_data)
plt.subplots_adjust(hspace=0.5)
plt.title("Restored Signal using Cublic Spline Filter ")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()

MSE = mean_squared_error(data_org, restored_data)
print(MSE)
