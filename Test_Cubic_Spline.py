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
from playsound import playsound
from scipy.interpolate import CubicSpline

# Import the ORGINAL wave file
samplerate_org, data_org = wavfile.read('original.wav')
#Plotting the original signal
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
#Plotting the degraded signal
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
    '''
    Takes the degraded signal, click indexes, number of clicks and window size, returns signal without clicks

    Args:
        data_deg[array] : Degraded data signal with clicks

        click_index[array] : Position of the clicks in the data_deg

    Returns:
        data_new[array] : Returns a new signal passed through median filter and  mostly free from clicks

    '''
    new_data = data_deg
    # Array of all index value
    index_all = np.arange(len(data_deg))
    # Filtering all data points except the clicks
    filtered_data = np.delete(new_data, click_index)
    # Filtering all indexes except the indexes of the click
    filtered_index = np.delete(index_all, click_index)
    # Using inbuilt CubicSpline function and passing filtered index and data to get a new trained function
    cs = CubicSpline(filtered_index, filtered_data, bc_type='natural')
    # Passing the click index through the new trained function
    new_data[click_index] = cs(click_index)
    return new_data

# Measure the start time
start_time = datetime.now()

# Adding progress bar
for i in tqdm(range(100)):
    restored_data = CubicSplineInterpolator(data_deg, click_index)
    sleep(0.005)

# Measure the end time
end_time = datetime.now()
print('Duration: {} seconds'.format(end_time - start_time))

# Write the restored audio file
wavfile.write("restored_cubic.wav", samplerate_org, restored_data)

#Plotting the restored signal
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

# playsound('degraded.wav')

playsound('restored_cubic.wav')
