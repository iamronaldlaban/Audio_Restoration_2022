import unittest
import numpy as np
import scipy
from scipy.io import wavfile
import matplotlib.pyplot as plt
from scipy.io import loadmat
from sklearn.metrics import mean_squared_error
from datetime import datetime
import time
from time import sleep
from tqdm import tqdm
import scipy.signal
import unittest
from playsound import playsound

import sys


# Import the ORGINAL wave file
samplerate_org, data_org = wavfile.read('original.wav')

# Plotting the original signal
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

# Plotting the degraded signal
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

# Window Size
win_len = int(input('Enter the window size : '))
#win_len = x = range(1, 50, 2)

# Check wheather the filter window size is ODD or EVEN
if win_len % 2 == 1:
    print('The window size is ODD')
else:
    print('The window size is EVEN')
    print('CHANGE WINDOW SIZE TO ODD NUMBER')
    sys.exit()


def median_filter(data_deg, click_index, num_clicks, win_len):
    '''
    Takes the degraded signal, click indexes, number of clicks and window size, returns signal without clicks

    Args:
        data_deg[array] : Degraded data signal with clicks

        click_index[array] : Position of the clicks in the data_deg

        num_clicks[int] : Number of click indexes

        win_len[int] : Window Length for the median filter

    Returns:
        data_new[array] : Returns a new signal passed through median filter and  mostly free from clicks

    '''
    data_new = data_deg
    for i in range(num_clicks):
        # Number of padded zeros required
        pad_num = int((win_len - 1) / 2)

        # Extract data around clicks
        inputVar = data_new[click_index[i] -
                            pad_num: click_index[i] + pad_num + 1]
        N = len(inputVar)

        # Add padded zeros
        padded_input = np.pad(inputVar, (pad_num, pad_num),
                              'constant', constant_values=(0, 0))

        new_mat = np.zeros(N)
        for j in range(N):
            # Reading values according to the window length
            a = padded_input[j:win_len+j]
            # Sorting the data
            b = np.sort(a)
            # Selecting the median value and add to the new matrix
            new_mat[j] = b[int((win_len - 1) / 2)]
        #  Replace the area around click with new values obtained from median filter
        data_new[click_index[i] -
                 pad_num: click_index[i] + pad_num + 1] = new_mat
    return data_new


# Measure the start time
start_time = time.time()

# Adding progress bar
for i in tqdm(range(100)):
    restored_data = median_filter(data_deg, click_index, num_clicks, win_len)
    sleep(0.03)

# Measure the end time
end_time = time.time()
print('Execution Time for Median Filter : {} seconds'.format(end_time - start_time))

# Write the restored audio file
wavfile.write("restored_median.wav", samplerate_org, restored_data)

# Plotting the restored signal
length = restored_data.shape[0] / samplerate_org
time_restored = np.linspace(0., length, restored_data.shape[0])
plt.subplot(3, 1, 3)
plt.plot(time_restored, restored_data)
plt.subplots_adjust(hspace=0.5)
plt.title("Restored Signal using Median Filter ")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()

# MSE = mean_squared_error(data_org, restored_data)
MSE = np.square(data_org - restored_data).mean()
print('The Mean Squared Error for Median Filter  :', MSE)

'''Unit Test to User Defined Median Filter'''


class TestMyCode(unittest.TestCase):
    def test_my_median_filter(self):
        data_test = data_deg
        for i in range(num_clicks):
            pad_num = int((win_len - 1) / 2)
            inputVar = data_test[click_index[i] -
                                 pad_num: click_index[i] + pad_num + 1]
            # Using inbuilt scipy median filter
            output2 = scipy.signal.medfilt(inputVar, kernel_size=win_len)
            data_test[click_index[i] -
                      pad_num: click_index[i] + pad_num + 1] = output2
        comparison = restored_data == data_test
        equal_arrays = comparison.all()
        if equal_arrays == True:
            print('The user defined median filter IS proper')
        else:
            print('The user defined median filter IS NOT proper')

    def test_my_mse_finction(self):
        MSE_inbuilt = mean_squared_error(data_org, restored_data)
        comparison = MSE == MSE_inbuilt
        equal_mse = comparison.all()
        if equal_mse == True:
            print('The user defined MSE function IS proper')
        else:
            print('The user defined MSE function IS NOT proper')


        


# run the test
if __name__ == "__main__":
    unittest.main()

''' Playing the aus=dio signal'''
# Playing the degraded signal
playsound('degraded.wav')

# Playing the restored signal
playsound('restored_median.wav')
